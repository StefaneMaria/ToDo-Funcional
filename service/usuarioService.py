from db_connection import getDBConnection 
from encrypt import encrypt, checkPassword
from flask import jsonify
import re

sql_AllUsuarios = "SELECT * FROM usuario"
sql_EmailUsuarios = "SELECT email FROM usuario"
sql_InsertUsario = lambda nome, email, senha : "INSERT INTO usuario (nome, email, senha) VALUES ( '"+ nome +"', '"+ email +"', '" + senha +"')"

dbConnection = getDBConnection()

def map_usuario(usuario_tuple):
  usuario_dict = {
      "id": usuario_tuple[0],
      "nome": usuario_tuple[1],
      "email": usuario_tuple[2],
      "senha": usuario_tuple[3]
  }

  return usuario_dict

def findAllUsuarios():
  dbConnection.execute(sql_AllUsuarios)
  allUserTuple = dbConnection.fetchall()
  lista_dicionarios = [map_usuario(usuario) for usuario in allUserTuple]
  return lista_dicionarios

def findUser(user_login):
  usuarios = findAllUsuarios()

  valid_user = lambda : next(((usuario["id"], usuario["nome"], 200) for usuario in usuarios if usuario["email"] == user_login["email"] and checkPassword(usuario["senha"], user_login["senha"])), (None, None, 400))

  return valid_user()

def verifyUser(user):
  if(not verifyEmail(user["email"])):
    if(verifyPassword(user["senha"])):
      crypt_pass = encrypt(user["senha"])
      dbConnection.execute(sql_InsertUsario(user["nome"], user["email"], crypt_pass.decode()))
      return jsonify({"message": "Usuario criado com sucesso"}), 200
    return jsonify({"message": "Senha inválida"}), 400
  return jsonify({"message": "E-mail já cadastrado"}), 400

def verifyEmail(email):
  dbConnection.execute(sql_EmailUsuarios)
  allEmails = [row[0] for row in dbConnection.fetchall()]
  return email in allEmails

def verifyPassword(password):
  has_alpha = bool(re.search(r'[a-zA-Z]', password))  # Verifica se há pelo menos uma letra
  has_digit = bool(re.search(r'\d', password))        # Verifica se há pelo menos um número
  has_special = bool(re.search(r'[!@#$%^&*()-_+=]', password))  # Verifica se há pelo menos um caractere especial
  
  return has_alpha and has_digit and has_special