from flask import Flask, render_template, request 
from flask import redirect, session

from modelos import Administrador

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

administrador = Administrador()

@app.route('/', methods=['GET', 'POST'])
def login():
  if request.method == 'GET':
    if 'usuario' in session:
      if session['usuario']['rol'] == 'administrador':
        return redirect('/admin')
    return render_template('login.html')
  try:
    usuario = administrador.login(request.form['email'], request.form['password'])
    usuario['_id'] = str(usuario['_id'])
    session['usuario'] = usuario
    if usuario['rol'] == 'administrador':
      return redirect('/admin')
    return 'Panel de docente'
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

  return render_template('panel_admin.html')


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




def administradorLogueado():
  if 'usuario' not in session:
    return False
  if session['usuario']['rol'] != 'administrador':
    return False
  return True

if __name__ == "__main__":
  app.run(debug=True, port=5000)