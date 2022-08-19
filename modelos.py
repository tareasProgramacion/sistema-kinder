from pymongo import MongoClient
from bson.objectid import ObjectId

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

  def obtenerCursos(self):
    lista = []
    for i in mongo.dbkinder.cursos.find():
      i['_id'] = str(i['_id'])
      lista.append(i)
    return lista

  def obtenerCurso(self, id):
    return mongo.dbkinder.cursos.find_one({'_id':ObjectId(id)})

  def agregarCurso(self, nombre:str):
    return mongo.dbkinder.cursos.insert_one({'nombre':nombre.capitalize()})

  def actualizarCurso(self, id:str, nombre:str):
    return mongo.dbkinder.cursos.update_one({'_id':ObjectId(id)},{'$set':{'nombre':nombre.capitalize()}})
  
  def eliminarCurso(self, id:str):
    return mongo.dbkinder.cursos.delete_one({'_id':ObjectId(id)})
  

  def obtenerDocentes(self):
    lista = []
    for i in mongo.dbkinder.usuarios.find({'rol':'docente'}):
      i['_id'] = str(i['_id'])
      lista.append(i)
      
    return lista

  def agregarDocente(self, nombre, email, password):
    existeEmail = mongo.dbkinder.usuarios.find_one({'email':email})
    if existeEmail:
      raise Exception('El email ya está registrado!')

    if len(password) < 8:
      raise Exception('El password debe tener al menos 8 dígitos')
    
    docente = {'nombre':nombre,'email':email,'password':password,'rol':'docente'}
    return mongo.dbkinder.usuarios.insert_one(docente)

  def eliminarDocente(self, id:str):
    return mongo.dbkinder.usuarios.delete_one({'_id':ObjectId(id)})

  def obtenerParalelos(self):
    lista = []
    for i in mongo.dbkinder.paralelos.find():
      i['_id'] = str(i['_id'])
      i['_curso'] = str(i['_curso'])
      i['_docente'] = str(i['_docente'])
      lista.append(i)

    return lista

  