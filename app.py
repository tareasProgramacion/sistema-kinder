from flask import Flask, render_template, request 
from flask import redirect, session
import uuid
from os import path

from modelos import Administrador, Docente

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

administrador = Administrador()
docente = Docente()

@app.route('/', methods=['GET', 'POST'])
def login():
  if request.method == 'GET':
    if 'usuario' in session:
      if session['usuario']['rol'] == 'administrador':
        return redirect('/admin')
      return redirect('/docente')
    return render_template('login.html')
  try:
    usuario = administrador.login(request.form['email'], request.form['password'])
    usuario['_id'] = str(usuario['_id'])
    session['usuario'] = usuario
    if usuario['rol'] == 'administrador':
      return redirect('/admin')
    return redirect('/docente')
  except Exception as error:
    return render_template('login.html',data={'error':error.__str__()})

@app.route('/registro', methods=['GET','POST'])
def registro():
  if request.method == 'GET':
    return render_template('registro.html')
  try:
    administrador.agregarAdministrador(
      request.form['nombre'],
      request.form['email'],
      request.form['password']
    )
    return redirect('/')
  except Exception as error:
    return render_template('registro.html',data={'error':error.__str__()})


@app.route('/salir',methods=['GET'])
def salir():
  session.pop('usuario',None)
  session.pop('estudiante',None)
  return redirect('/')


@app.route('/admin',methods=['GET'])
def admin():
  if administradorLogueado() == False:
    return redirect('/')

  return render_template('panel_admin.html',data={'usuario':session['usuario']})


@app.route('/admin/curso',methods=['GET','POST'])
def adminCurso():
  if administradorLogueado() == False:
    return redirect('/')

  if request.method == 'POST':
    administrador.agregarCurso(request.form['nombre'])
  cursos = administrador.obtenerCursos()
  return render_template('panel_admin_curso.html',data={'cursos':cursos})
  

@app.route('/admin/curso/eliminar/<id>',methods=['GET'])
def adminCursoEliminar(id):
  if administradorLogueado() == False:
    return redirect('/')

  administrador.eliminarCurso(id)
  return redirect('/admin/curso')
  
  
@app.route('/admin/curso/actualizar/<id>',methods=['GET','POST'])
def adminCursoActualizar(id):
  if administradorLogueado() == False:
    return redirect('/')

  data = {}
  if request.method == 'GET':
    data['curso'] = administrador.obtenerCurso(id)
    data['cursos'] = administrador.obtenerCursos()
    return render_template('panel_admin_curso.html',data=data)
  else:
    administrador.actualizarCurso(id,request.form['nombre'])
    return redirect('/admin/curso')

  
@app.route('/admin/docente',methods=['GET','POST'])
def adminDocente():
  if administradorLogueado() == False:
    return redirect('/')

  data = {}
  if request.method == 'POST':
    try:
      administrador.agregarDocente(request.form['nombre'], request.form['email'], request.form['password'])
    except Exception as error:
      data['error'] = error.__str__()

  data['docentes'] = administrador.obtenerDocentes()
  return render_template('panel_admin_docente.html',data=data)

@app.route('/admin/docente/eliminar/<id>',methods=['GET'])
def adminDocenteEliminar(id):
  if administradorLogueado() == False:
    return redirect('/')

  administrador.eliminarDocente(id)
  return redirect('/admin/docente')


@app.route('/admin/paralelo', methods=['GET','POST'])
def adminParalelo():
  if administradorLogueado() == False:
    return redirect('/')

  data = {}

  if request.method == 'POST':
    try:
      administrador.agregarParalelo(
        request.form['nombre'],
        request.form['curso'],
        request.form['docente']
      )
    except Exception as error:
      data['error'] = error.__str__()
  data['cursos'] = administrador.obtenerCursos()
  data['docentes'] = administrador.obtenerDocentes()
  data['paralelos'] = administrador.obtenerParalelos()
  return render_template('panel_admin_paralelo.html',data=data)

@app.route('/admin/paralelo/eliminar/<id>',methods=['GET'])
def adminParaleloEliminar(id):
  if administradorLogueado() == False:
    return redirect('/')

  administrador.eliminarParalelo(id)
  return redirect('/admin/paralelo')

@app.route('/admin/estudiante',methods=['GET','POST'])
def adminEstudiante():
  if administradorLogueado() == False:
    return redirect('/')

  data = {}

  if request.method == 'POST':
    foto = request.files['foto']
    raiz,extension = path.splitext(foto.filename)
    nuevoNombreFoto = f'{uuid.uuid4()}{extension}'
    foto.save(f'./static/{nuevoNombreFoto}')
    administrador.agregarEstudiante(
      request.form['nombre'],
      request.form['paralelo'],
      nuevoNombreFoto
    )

  data['estudiantes'] = administrador.obtenerEstudiantes()
  data['paralelos'] = administrador.obtenerParalelos()
  return render_template('panel_admin_estudiante.html',data=data)
  
@app.route('/admin/estudiante/eliminar/<id>',methods=['GET'])
def adminEstudianteEliminar(id):
  if administradorLogueado() == False:
    return redirect('/')

  administrador.eliminarEstudiante(id)
  return redirect('/admin/estudiante')

@app.route('/docente',methods=['GET'])
def panelDocente():
  if docenteLogueado() == False:
    return redirect('/')
  data = {'paralelos': docente.obtenerParalelos(session['usuario']['_id'])}
  data['usuario'] = session['usuario']
  return render_template('panel_docente.html',data=data)

@app.route('/docente/<_paralelo>',methods=['GET'])
def panelDocenteEstudiantes(_paralelo):
  if docenteLogueado() == False:
    return redirect('/')
  data = {'paralelos': docente.obtenerParalelos(session['usuario']['_id'])}
  data['estudiantes'] = docente.obtenerEstudiantes(_paralelo)
  return render_template('panel_docente_estudiante.html',data=data)



def administradorLogueado():
  if 'usuario' not in session:
    return False
  if session['usuario']['rol'] != 'administrador':
    return False
  return True

def docenteLogueado():
  if 'usuario' not in session:
    return False
  if session['usuario']['rol'] != 'docente':
    return False
  return True

if __name__ == "__main__":
  app.run(debug=True, port=5000)