from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from flask_mysqldb import MySQL


app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'bdpython'
app.config['SECRET_KEY'] = 'codigoCualquiera-HEX_SEC_KEY'

#conexion de mysql y app
conexion = MySQL(app)

#cosas
#crt+k y crt+c

@app.route('/')
def index():
    #lista
    Listacursos=['java','php','visual','c++','python']
    #diccionario
    data={
        'titulo':'Index',
        'Bienvenida':'Saludos',
        'cursos':Listacursos, #lista dentro de diccionario
        'numeroCursos':len(Listacursos) #numero de cursos
    }
    return render_template('signIn.html', data=data)


###login
@app.route('/login', methods=['POST'])
def login():
    data = {}
    data2={
        'titulo':'Usuarios',
        'Bienvenida':'USUARIOS'
    }
    usuario= request.form['txtUsuario']
    password= request.form['txtPassword']

    cursor = conexion.connection.cursor()
    sql = "SELECT * FROM usuario where nombre=%s and password=%s"
    cursor.execute(sql,(usuario,password))
    usuarios = cursor.fetchone()
    print("llego al try login")
    if usuarios is not None and usuarios!=():#si encontro datos
        print("llego al if login")
        print(usuario)
        print(password)
        print(usuarios)
        session['usuario'] = usuario
        session['password'] = password
        return redirect(url_for('menu'))#va a la funcion menu
    else:
        return render_template('signIn.html', message="Las credenciales no son correctas")


@app.route('/logout')
def logout():
    print("se cierra sesion")
    session.clear()
    return redirect(url_for('index'))



###Menu principal
@app.route('/menu', methods=['GET'])
def menu():
    data2={
        'titulo':'Menu',
        'Bienvenida':'Menu'
    }
    return render_template('Menu.html', data2=data2)



### USUARIOS

@app.route('/usuarios', methods=['GET','POST'])
def listar_usuario():
    data = {}
    data2={
        'titulo':'Usuarios',
        'Bienvenida':'USUARIOS',
        'counter':1
    } #filtro
    if request.method== 'POST': 
        nombre= request.form['txtNombre']
        print(request.form['txtNombre'])
        try:
            cursor = conexion.connection.cursor()
            sql = "SELECT * FROM usuario where nombre=%s"
            cursor.execute(sql,(nombre,))
            usuarios = cursor.fetchall()#usar fetchall, fetchone da error
            data=[]        
            columName=[columna[0] for columna in cursor.description]
            for record in usuarios:
                data.append(dict(zip(columName, record)))
                print("llego al for")
        except Exception as ex:
            data['mensaje'] = 'Error...'
        return render_template('usuarios.html', data=data, data2=data2)
    else:#listar normal
        try:
            cursor = conexion.connection.cursor()
            sql = "SELECT * FROM usuario"
            cursor.execute(sql)
            usuarios = cursor.fetchall()#usar fetchall, fetchone da error
            data=[]        
            columName=[columna[0] for columna in cursor.description]
            for record in usuarios:
                data.append(dict(zip(columName, record)))
        except Exception as ex:
            data['mensaje'] = 'Error...'
        return render_template('usuarios.html', data=data, data2=data2)


#url for es el app route


@app.route('/ordenar_usuario/<string:ord>')
def ordenar_usuario(ord):
    data = {}
    data2={
        'titulo':'Usuarios',
        'Bienvenida':'USUARIOS'
    }
    try:
        cursor = conexion.connection.cursor()
        #nuevo
        if ord:
            print(ord)
            sql = f"SELECT * FROM usuario ORDER BY {ord}"
        cursor.execute(sql)
        usuarios = cursor.fetchall()#usar fetchall, fetchone da error
        data=[]        
        columName=[columna[0] for columna in cursor.description]
        for record in usuarios:
            data.append(dict(zip(columName, record)))
    except Exception as ex:
        data['mensaje'] = 'Error...'
    return render_template('usuarios.html', data=data, data2=data2)

@app.route('/guardar', methods=['POST'])
def guardar():
    data2={
        'titulo':'Usuarios',
        'Bienvenida':'USUARIOS',
        'counter':1
    }
    usuario= request.form['txtUsuario']
    password= request.form['txtPassword']
    if usuario and password:
        #nuevo
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM usuario where nombre=%s"
        cursor.execute(sql,(usuario,))
        usuarios = cursor.fetchall()#usar fetchall, fetchone da error
        if usuarios is None or usuarios==():#si no encontro datos
            print("usuario nuevo")
            print(usuarios)
            cursor = conexion.connection.cursor()
            sql = "INSERT INTO usuario(nombre, password) VALUES (%s, %s)"
            data=(usuario,password)
            cursor.execute(sql, data)
            conexion.connection.commit()
            flash('Datos guardados ok','alert-success')
        else:
            flash('ERROR: El usuario ya existe','alert-danger')
    return redirect(url_for('listar_usuario'))

@app.route('/delete/<string:id>')
def delete(id):
    cursor = conexion.connection.cursor()
    sql = "DELETE FROM usuario WHERE codigo=%s"
    data=(id,)
    cursor.execute(sql, data)
    conexion.connection.commit()
    flash('Datos eliminados ok','alert-success')
    return redirect(url_for('listar_usuario'))

@app.route('/update/<string:codigo>', methods=['POST'])
def update(codigo):
    nombre= request.form['txtUsuario']
    password= request.form['txtPassword']
    if nombre and password:
        cursor = conexion.connection.cursor()
        sql = "UPDATE usuario SET nombre=%s, password=%s where codigo=%s"
        #si no se pone codigo da error
        #si sepone codigo al inicio no da error pero no hace el update
        data=(nombre,password,codigo)#se pone el codigo en ese orden ya que el codigo se usa en la consulta
        cursor.execute(sql, data)
        conexion.connection.commit()
        flash('Datos actualizados ok','alert-success')
    return redirect(url_for('listar_usuario'))




#### PRODUCTOS ##########

#funcion listar ok
@app.route('/productos', methods=['GET','POST'])
def listar_productos():
    datacbo=llenarcbo_productos()
    data = {}
    data2={
        'titulo':'Productos',
        'Bienvenida':'PRODUCTOS'
    }
    if request.method== 'POST': #filtro
        print("llego al filtro producto")
        nombre= request.form['txtNombre']
        print(request.form['txtNombre'])
        try:
            cursor = conexion.connection.cursor()
            sql = "SELECT producto.codigo,producto.nombre,tipoproducto.nombre AS tipo FROM producto,tipoproducto WHERE producto.codigoTipo=tipoproducto.codigo AND producto.nombre=%s"
            cursor.execute(sql,(nombre,))
            productos = cursor.fetchall()#usar fetchall, fetchone da error
            data=[]        
            columName=[columna[0] for columna in cursor.description]
            for record in productos:
                data.append(dict(zip(columName, record)))
        except Exception as ex:
            data['mensaje'] = 'Error...'
        return render_template('productos.html', data=data, data2=data2,datacbo=datacbo)
    else: #listar normal
        try:
            print("llego al listar productos")
            cursor = conexion.connection.cursor()
            sql = "SELECT producto.codigo,producto.nombre,tipoproducto.nombre AS tipo FROM producto,tipoproducto WHERE producto.codigoTipo=tipoproducto.codigo"
            cursor.execute(sql)
            productos = cursor.fetchall()#usar fetchall, fetchone da error
            data=[]        
            columName=[columna[0] for columna in cursor.description]
            for record in productos:
                data.append(dict(zip(columName, record)))
            print(data)
            print(datacbo)
        except Exception as ex:
            data['mensaje'] = 'Error...'
        return render_template('productos.html', data=data, data2=data2,datacbo=datacbo)

#ordenar
@app.route('/ordenar_producto/<string:ord>')
def ordenar_producto(ord):
    data = {}
    data2={
        'titulo':'productos',
        'Bienvenida':'PRODUCTOS'
    }
    try:
        cursor = conexion.connection.cursor()
        #nuevo
        if ord:
            print(ord)
            sql = f"SELECT * FROM producto ORDER BY {ord}"
        cursor.execute(sql)
        productos = cursor.fetchall()#usar fetchall, fetchone da error
        data=[]        
        columName=[columna[0] for columna in cursor.description]
        for record in productos:
            data.append(dict(zip(columName, record)))
    except Exception as ex:
        data['mensaje'] = 'Error...'
    return render_template('productos.html', data=data, data2=data2)

#no se puede usar el mismo approute en 2 funciones
@app.route('/productos')
def llenarcbo_productos():
    datacbo = {}
    print("llego a llenar cbo")
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT tipoproducto.codigo AS codigoTipo,tipoproducto.nombre FROM tipoproducto"
        cursor.execute(sql)
        productos = cursor.fetchall()#usar fetchall, fetchone da error
        datacbo=[]
        columName=[columna[0] for columna in cursor.description]
        for record in productos:
            datacbo.append(dict(zip(columName, record)))
        print("datos cbo")
        print(datacbo)
    except Exception as ex:
        datacbo['mensaje'] = 'Error...'
    return datacbo


@app.route('/guardar_producto', methods=['POST'])
def guardar_producto():
    producto= request.form['txtProducto']
    tipo= request.form['cboTipo']
    if producto and tipo:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM producto where nombre=%s"
        cursor.execute(sql,(producto,))
        productos = cursor.fetchall()#usar fetchall, fetchone da error
        if productos is None or productos==():#si no encontro datos
            cursor = conexion.connection.cursor()
            sql = "INSERT INTO producto(nombre, codigoTipo) VALUES (%s, %s)"
            data=(producto,tipo)
            cursor.execute(sql, data)
            conexion.connection.commit()
            flash('Datos guardados correctamente','alert-success')
        else:
            #return render_template('usuarios.html',data2=data2, message="El usuario ya existe")
            flash('Error al guardar los datos','alert-danger')
    return redirect(url_for('listar_productos'))


@app.route('/delete_producto/<string:id>')
def delete_producto(id):
    cursor = conexion.connection.cursor()
    sql = "DELETE FROM producto WHERE codigo=%s"
    data=(id,)
    cursor.execute(sql, data)
    conexion.connection.commit()
    flash('Producto eliminado correctamente','alert-success')
    return redirect(url_for('listar_productos'))


@app.route('/update_producto/<string:codigo>', methods=['POST'])
def update_producto(codigo):
    producto= request.form['txtProducto']
    tipo= request.form['cboTipo']
    if producto and tipo:
        cursor = conexion.connection.cursor()
        sql = "UPDATE producto SET nombre=%s, codigoTipo=%s where codigo=%s"
        #si no se pone codigo da error
        #si sepone codigo al inicio no da error pero no hace el update
        data=(producto,tipo,codigo)#se pone el codigo en ese orden ya que el codigo se usa en la consulta
        cursor.execute(sql, data)
        conexion.connection.commit()
        flash('Datos actualizados correctamente','alert-success')
    return redirect(url_for('listar_productos'))


'''
#decoradores
@app.before_request
def before_request():
    print("Antes de la petición...")


@app.after_request
def after_request(response):
    print("Después de la petición")
    return response
'''

 #url personalizada
@app.route('/contacto/<nombre>/<int:edad>') #nombre debe ser = nombre
def contacto(nombre,edad):
    data={
        'titulo':'Contacto',
        'nombre':nombre,
        'edad':edad
    }
    return render_template('contacto.html', data=data)



#funcion para enviar url con varios datos dinamicos, es diferente a url personalizada
def query_string():
    print(request)
    print(request.args)
    print(request.args.get('param1'))
    print(request.args.get('param2'))
    return "Datos ok" #debe retornar algo para que no de error

def pagina_no_encontrada(error):
    #mostrar mensaje de error
    return render_template('error404.html'), 404 # se coloca el numero de error
    #o tambien en ves de mostrar un mensaje de error lo redirijimos al index
    #return redirect(url_for('index')) #se pone nombre de la funcion a llamar

if __name__ == '__main__':
    app.add_url_rule('/query_string',view_func=query_string)#para llamar a funcion query string
    #app.run() normal
    app.register_error_handler(404, pagina_no_encontrada)#para manejar el error 404
    app.run(debug=True)#modo depuracion, osea que actualiza cambios solo con refrescar navegador

