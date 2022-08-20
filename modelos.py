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
      curso = mongo.dbkinder.cursos.find_one({'_id':i['_curso']})
      docente = mongo.dbkinder.usuarios.find_one({'_id':i['_docente']})
      lista.append({
        '_id':i['_id'],
        'nombre': i['nombre'],
        'curso':curso['nombre'],
        'docente':docente['nombre']
      })
    return lista

  def agregarParalelo(self,nombre, _curso, _docente):
    existe = mongo.dbkinder.paralelos.find_one({'nombre':nombre,'_curso':ObjectId(_curso)})
    if existe:
      raise Exception('Ya existe un paralelo con ese nombre')
    
    return mongo.dbkinder.paralelos.insert_one({
      'nombre':nombre,
      '_curso':ObjectId(_curso),
      '_docente':ObjectId(_docente)
    })

  def eliminarParalelo(self, id):
    return mongo.dbkinder.paralelos.delete_one({'_id':ObjectId(id)})
  
  def obtenerEstudiantes(self):
    lista = []
    for i in mongo.dbkinder.estudiantes.find():
      i['_id'] = str(i['_id'])
      paralelo = mongo.dbkinder.paralelos.find_one({'_id':i['_paralelo']})
      curso = mongo.dbkinder.cursos.find_one({'_id':paralelo['_curso']})
      lista.append({
        '_id':i['_id'],
        'nombre':i['nombre'],
        'foto':i['foto'],
        'paralelo':f'{curso["nombre"]} - {paralelo["nombre"]}'
      })

    return lista

  def agregarEstudiante(self, nombre:str, _paralelo, foto):
    return mongo.dbkinder.estudiantes.insert_one({
      'nombre':nombre.capitalize(),
      '_paralelo':ObjectId(_paralelo),
      'foto':foto,
      'notas':[]
    })

  def eliminarEstudiante(self, id):
    return mongo.dbkinder.estudiantes.delete_one({'_id':ObjectId(id)})

class Docente:
  def obtenerParalelos(self, _docente):
    lista = []
    for i in mongo.dbkinder.paralelos.find({'_docente':ObjectId(_docente)}):
      curso = mongo.dbkinder.cursos.find_one({'_id':i['_curso']})
      lista.append({
        '_id': str(i['_id']),
        'nombre': f'{curso["nombre"]} - {i["nombre"]}'
      })
    return lista

  def obtenerEstudiantes(self, _paralelo):
    lista = []
    for i in mongo.dbkinder.estudiantes.find({'_paralelo':ObjectId(_paralelo)}):
      promedio = 0
      if len(i['notas']) > 0:
        promedio = round(sum(i['notas'])/len(i['notas']), 2)
      lista.append({
        'nombre':i['nombre'],
        'foto':i['foto'],
        'promedio': promedio
      })
    return lista

