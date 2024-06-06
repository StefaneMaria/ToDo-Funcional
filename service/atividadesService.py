from db_connection import getDBConnection 
from flask import jsonify
import json, re

sql_allUserAtividade = lambda user_id : "SELECT a.id_atividade, a.nome, a.descricao, a.data_vencimento, a.status, p.tipo AS tipo_prioridade, p.nivel AS nivel_prioridade FROM atividade AS a JOIN prioridade AS p ON a.id_prioridade = p.id_prioridade WHERE a.id_usuario = " + user_id
sql_findAtividade = lambda atv_id : "SELECT a.id_atividade, a.nome, a.descricao, a.data_vencimento, a.status, p.tipo AS tipo_prioridade, p.nivel AS nivel_prioridade FROM atividade AS a JOIN prioridade AS p ON a.id_prioridade = p.id_prioridade WHERE a.id_atividade = " + atv_id
sql_insertAtividade = lambda nome: lambda descricao: lambda data_vencimento: lambda tipo_prioridade: lambda id_usuario: "INSERT INTO atividade (`nome`, `descricao`, `data_vencimento`, `status`, `id_prioridade`, `id_usuario`) VALUES ('"+nome+"', " +format_value(descricao) + format_value(data_vencimento) + " 0 , (SELECT id_prioridade FROM prioridade WHERE tipo = '" +tipo_prioridade+ "'), "+id_usuario+")"
sql_deleteAtividade = lambda atv_id: "DELETE FROM atividade WHERE `id_atividade` = " + atv_id

dbConnection = getDBConnection()

format_value = lambda value: "NULL," if value is None or not value else "'" + value + "',"

format_date = lambda date_str: '/'.join(reversed(date_str.split('/')))
valid_date = lambda date_str: None if not date_str else format_date(date_str)

check_nome = lambda nome: True if nome is None else False
check_string = lambda str : str is None or not str or str == ""


def map_atividade(atividade_tuple):
  atividade_dict = {
      "id": atividade_tuple[0],
      "nome": atividade_tuple[1] if atividade_tuple[1] is not None else "",
      "descricao": atividade_tuple[2]  if atividade_tuple[2] is not None else "",
      "data_vencimento": atividade_tuple[3].strftime("%d/%m/%Y") if atividade_tuple[3] is not None else "",
      "status": atividade_tuple[4],
      "prioridade": atividade_tuple[5],
      "nivel_prioridade": atividade_tuple[6]
  }

  return atividade_dict

def getAtividades(user_id):
  dbConnection.execute(sql_allUserAtividade(user_id))
  allUserAtividadeTuple = dbConnection.fetchall()
  lista_dicionarios = [map_atividade(atividade) for atividade in allUserAtividadeTuple]
  atv_pendentes = list(filter(lambda x: x['status'] == 0, lista_dicionarios))
  return atv_pendentes

def findUserAtividade(user_id):
  atividades = getAtividades(user_id)
  return jsonify({"atividades": atividades}), 200

def findAtividade(atv_id):
  dbConnection.execute(sql_findAtividade(atv_id))
  atividade = map_atividade(dbConnection.fetchall()[0])
  return atividade, 200

def ordenaPrioridade(user_id):
  atividades = getAtividades(user_id)
  atividades_ordenadas = sorted(atividades, key=lambda x: x["nivel_prioridade"], reverse=True)
  return jsonify({"atividades": atividades_ordenadas}), 200 

def ordenaData(user_id):
  atividades = getAtividades(user_id)
  atividades_ordenadas = sorted(atividades, key=lambda x: x["data_vencimento"], reverse=True)
  return jsonify({"atividades": atividades_ordenadas}), 200

def insertAtividade(atividade, user_id):
  if check_nome(atividade["nome"]):
    return "Atividade sem nome", 400
  check_prioridade = lambda str: atividade["prioridade"] if not check_string(atividade["prioridade"]) else ""
  sql = sql_insertAtividade(atividade["nome"])(atividade["descricao"])(valid_date(atividade["data_vencimento"]))(check_prioridade(atividade["prioridade"]))(user_id)
  dbConnection.execute(sql)
  return jsonify({"message": "Atividade criada com sucesso"}), 200

def formatar_atualizacao(coluna, valor, validar):
    if not validar(valor):
      return f"`{coluna}` = '{valor}', "
    else:
      return ""

def updateAtividade(atividade, id_atv):
  nome = atividade["nome"]
  descricao = atividade["descricao"]
  data_vencimento = valid_date(atividade["data_vencimento"])
  prioridade = atividade["prioridade"]
  status = atividade["status"]
  p_id = lambda prioridade : "1 " if prioridade == "baixa" else "2 " if prioridade == "media" else "3 "
  
  sql_nome = lambda nome: formatar_atualizacao("nome", nome, check_string)
  sql_descricao = lambda descricao: formatar_atualizacao("descricao", descricao, check_string)
  sql_data_vencimento = lambda data_vencimento: formatar_atualizacao("data_vencimento", data_vencimento, check_string)
  sql_prioridade = lambda prioridade: "" if check_string(prioridade) else " `id_prioridade` = " + p_id(prioridade)
  sql_status = lambda status: "" if status == 0 else ", `status` = 1 "
  sql_where = lambda: "WHERE `id_atividade` = "+ id_atv + " "

  consulta = "UPDATE atividade SET " + sql_nome(nome) + sql_descricao(descricao) + sql_data_vencimento(data_vencimento) + sql_prioridade(prioridade) + sql_status(status) + sql_where()
  correcao = r',\s*WHERE'
  consulta_corrigida = re.sub(correcao, ' WHERE', consulta)
  print(consulta_corrigida)
  dbConnection.execute(consulta_corrigida)
  return jsonify({"message": "Sucesso"}), 200

def deleteAtividade(atv_id):
  dbConnection.execute(sql_deleteAtividade(atv_id))
  return "Atividade removida", 200