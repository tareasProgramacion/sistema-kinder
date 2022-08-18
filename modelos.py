from pymongo import MongoClient

mongo = MongoClient("mongodb+srv://admin:admin@cluster0.zk7c2.mongodb.net/dbkinder?retryWrites=true&w=majority")

class Administrador:
  def agregarDocente(self, nombre, email, password):
    existeEmail = mongo.dbkinder.usuarios.find_one({'email':email})
    if existeEmail:
      raise Exception('El email ya está registrado!')

    if len(password) < 8:
      raise Exception('El password debe tener al menos 8 dígitos')

    return mongo.dbkinder.usuarios.insert_one({
      "nombre": nombre,
      "email": email,
      "password":  password,
      "rol": "docente"
    })
  
  def login(self, email, password):
    usuario = mongo.dbkinder.usuarios.find_one({'email':email,'password':password},{password:0})
    
    if usuario == None:
      raise Exception('Las credenciales son incorrectas!')
    
    return usuario

  def agregarAdministrador(self, nombre, email, password):
    existeEmail = mongo.dbkinder.usuarios.find_one({'email':email})
    if existeEmail:
      raise Exception('El email ya está registrado!')

    if len(password) < 8:
      raise Exception('El password debe tener al menos 8 dígitos')
    
    administrador = mongo.dbkinder.usuarios.find_one({'rol':'administrador'})
    if administrador:
      raise Exception('Solo se puede registrar un administrador!')

    return mongo.dbkinder.usuarios.insert_one({
      "nombre": nombre,
      "email": email,
      "password":  password,
      "rol": "administrador"
    })


