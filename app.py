from flask import Flask, render_template, request 
from flask import redirect, session

from modelos import Administrador

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

administrador = Administrador()

@app.route('/', methods=['GET', 'POST'])
def login():
  if request.method == 'GET':
    return render_template('login.html')
  try:
    usuario = administrador.login(request.form['email'], request.form['password'])
    session['usuario'] = usuario
    if usuario['rol'] == 'administrador':
      return 'Panel de administrador'
    return 'Panel de docente'
  except Exception as error:
    return render_template('login.html',error=error.__str__())

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
    return render_template('registro.html',error = error.__str__())


@app.route('/salir',methods=['GET'])
def salir():
  session.pop('usuario',None)
  return redirect('/')

if __name__ == "__main__":
  app.run(debug=True, port=5000)