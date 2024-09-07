import os
import MySQLdb
from flask import Flask, Response, flash, jsonify, redirect, render_template, request, session, url_for, send_file
from flask_mysqldb import MySQL
from datetime import datetime
from dateutil.relativedelta import relativedelta
import io
import pandas as pd

# os para usar fechas en export
# response para export
# io para imagenes y archivos
#pandas para hacer import



############ version 2 prueba git ##########

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'bdpython'
app.config['SECRET_KEY'] = 'codigoCualquiera-HEX_SEC_KEY'
#app.config['MYSQL_CURSORCLASS'] = 'DictCursor' # devuelve diccionarios en global
# o si se quiere para una funcion especifica se deja esto comentado y se agrega como en la
#funcion de login

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
    cursor = conexion.connection.cursor(MySQLdb.cursors.DictCursor)
    #sql = "SELECT * FROM usuario where username=%s and password=%s"
    sql = "SELECT Usuario.codigo,Usuario.username,Usuario.password,tipoUsuario.tipo FROM Usuario,tipoUsuario WHERE Usuario.codigoTipo=tipoUsuario.codigo and username=%s and password=%s"
    cursor.execute(sql,(usuario,password))
    usuarios = cursor.fetchone()
    if usuarios is not None and usuarios!=():#si encontro datos
        print("llego al if login")
        session['usuario'] = usuario
        session['password'] = password
        session['tipo'] = usuarios['tipo']
        #print(session['tipo'])
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

#tiene listar normal y filtro
@app.route('/usuarios', methods=['GET','POST'])
def listar_usuario():
    datacbo=llenarcbo_usuarios()
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
            sql = "SELECT Usuario.codigo,Usuario.username,Usuario.password,tipoUsuario.tipo FROM Usuario,tipoUsuario WHERE Usuario.codigoTipo=tipoUsuario.codigo and username=%s"
            cursor.execute(sql,(nombre,))
            usuarios = cursor.fetchall()#usar fetchall, fetchone da error
            data=[]        
            columName=[columna[0] for columna in cursor.description]
            for record in usuarios:
                data.append(dict(zip(columName, record)))
                print("llego al for")
        except Exception as ex:
            data['mensaje'] = 'Error...'
        return render_template('usuarios.html', data=data, data2=data2,datacbo=datacbo)
    else:#listar normal
        try:
            cursor = conexion.connection.cursor()
            sql = "SELECT Usuario.codigo,Usuario.username,Usuario.password,tipoUsuario.tipo FROM Usuario,tipoUsuario WHERE Usuario.codigoTipo=tipoUsuario.codigo"
            cursor.execute(sql)
            usuarios = cursor.fetchall()#usar fetchall, fetchone da error
            data=[]        
            columName=[columna[0] for columna in cursor.description]
            for record in usuarios:
                data.append(dict(zip(columName, record)))
        except Exception as ex:
            data['mensaje'] = 'Error...'
        return render_template('usuarios.html', data=data, data2=data2,datacbo=datacbo)

#url for es el app route

@app.route('/ordenar_usuario/<string:ord>')
def ordenar_usuario(ord):
    datacbo=llenarcbo_usuarios()
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
            sql = f"SELECT Usuario.codigo,Usuario.username,Usuario.password,tipoUsuario.tipo FROM Usuario,tipoUsuario WHERE Usuario.codigoTipo=tipoUsuario.codigo ORDER BY {ord}"
        cursor.execute(sql)
        usuarios = cursor.fetchall()#usar fetchall, fetchone da error
        data=[]        
        columName=[columna[0] for columna in cursor.description]
        for record in usuarios:
            data.append(dict(zip(columName, record)))
    except Exception as ex:
        data['mensaje'] = 'Error...'
    return render_template('usuarios.html', data=data, data2=data2,datacbo=datacbo)

@app.route('/usuarios')# se activa solo al cargar la pagina, ya que tiene el mismo decorador que el listar
def llenarcbo_usuarios():
    datacbo = {}
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT tipousuario.codigo AS codigoTipo,tipousuario.tipo FROM tipousuario"
        cursor.execute(sql)
        usuarios = cursor.fetchall()#usar fetchall, fetchone da error
        datacbo=[]
        columName=[columna[0] for columna in cursor.description]
        for record in usuarios:
            datacbo.append(dict(zip(columName, record)))
    except Exception as ex:
        datacbo['mensaje'] = 'Error...'
    return datacbo

@app.route('/guardar', methods=['POST'])
def guardar():
    data2={
        'titulo':'Usuarios',
        'Bienvenida':'USUARIOS',
        'counter':1
    }
    usuario= request.form['txtUsuario']
    password= request.form['txtPassword']
    tipo= request.form['cboTipo']
    if usuario and password and tipo:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM usuario where username=%s"
        cursor.execute(sql,(usuario,))
        usuarios = cursor.fetchall()#usar fetchall, fetchone da error
        if usuarios is None or usuarios==():#si no encontro datos
            print("usuario nuevo")
            print(usuarios)
            cursor = conexion.connection.cursor()
            sql = "INSERT INTO usuario(username, password, codigoTipo) VALUES (%s, %s, %s)"
            data=(usuario,password,tipo)
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
    tipo= request.form['cboTipo']
    if nombre and password and tipo:
        cursor = conexion.connection.cursor()
        sql = "UPDATE usuario SET username=%s, password=%s, codigoTipo=%s where codigo=%s"
        #si no se pone codigo da error
        #si sepone codigo al inicio no da error pero no hace el update
        data=(nombre,password,tipo,codigo)#se pone el codigo en ese orden ya que el codigo se usa en la consulta
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
            sql = "SELECT producto.codigo,producto.nombre,producto.stock,producto.stock_min,producto.estado,tipoproducto.nombre AS tipo FROM producto,tipoproducto WHERE producto.codigoTipo=tipoproducto.codigo AND producto.nombre=%s"
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
            cursor = conexion.connection.cursor()
            sql = "SELECT producto.codigo,producto.nombre,producto.stock,producto.stock_min,producto.estado,tipoproducto.nombre AS tipo FROM producto,tipoproducto WHERE producto.codigoTipo=tipoproducto.codigo"
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
    datacbo=llenarcbo_productos()
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
            sql = f"SELECT producto.codigo,producto.nombre,producto.stock,producto.stock_min,producto.estado,tipoproducto.nombre AS tipo FROM producto,tipoproducto WHERE producto.codigoTipo=tipoproducto.codigo ORDER BY {ord}"
        cursor.execute(sql)
        productos = cursor.fetchall()#usar fetchall, fetchone da error
        data=[]        
        columName=[columna[0] for columna in cursor.description]
        for record in productos:
            data.append(dict(zip(columName, record)))
    except Exception as ex:
        data['mensaje'] = 'Error...'
    return render_template('productos.html', data=data, data2=data2,datacbo=datacbo)

#no se puede usar el mismo approute en 2 funciones
@app.route('/productos')# se activa solo al cargar la pagina, ya que tiene el mismo decorador que el listar
def llenarcbo_productos():
    datacbo = {}
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT tipoproducto.codigo AS codigoTipo,tipoproducto.nombre FROM tipoproducto"
        cursor.execute(sql)
        productos = cursor.fetchall()#usar fetchall, fetchone da error
        datacbo=[]
        columName=[columna[0] for columna in cursor.description]
        for record in productos:
            datacbo.append(dict(zip(columName, record)))
    except Exception as ex:
        datacbo['mensaje'] = 'Error...'
    return datacbo


@app.route('/guardar_producto', methods=['POST'])
def guardar_producto():
    producto= request.form['txtProducto']
    stock= request.form['txtStock']
    stockminimo= request.form['txtStockMinimo']
    if stock > stockminimo:
        estado="Ok"
    else:
        estado="Insuficiente"
    tipo= request.form['cboTipo']
    if producto and stock and stockminimo and estado and tipo: #si vienen datos del form
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM producto where nombre=%s"
        cursor.execute(sql,(producto,))
        productos = cursor.fetchall()
        if productos is None or productos==():#si no encontro datos entonces guarda
            cursor = conexion.connection.cursor()
            sql = "INSERT INTO producto(nombre, stock, stock_min, estado, codigoTipo) VALUES (%s, %s, %s, %s, %s)"
            data=(producto,stock,stockminimo,estado,tipo)
            cursor.execute(sql, data)
            conexion.connection.commit()
            flash('Datos guardados correctamente','alert-success')
        else:
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
    stock= request.form['txtStock']
    stockminimo= request.form['txtStockMinimo']
    if stock > stockminimo:
        estado="Ok"
    else:
        estado="Insuficiente"
    tipo= request.form['cboTipo']
    if producto and stock and stockminimo and estado and tipo:
        cursor = conexion.connection.cursor()
        sql = "UPDATE producto SET nombre=%s, stock=%s, stock_min=%s, estado=%s, codigoTipo=%s where codigo=%s"
        #si no se pone codigo da error
        #si sepone codigo al inicio no da error pero no hace el update
        data=(producto,stock,stockminimo,estado,tipo,codigo)#se pone el codigo en ese orden ya que el codigo se usa en la consulta
        cursor.execute(sql, data)
        conexion.connection.commit()
        flash('Datos actualizados correctamente','alert-success')
    return redirect(url_for('listar_productos'))


######### empleados ##########
@app.route('/empleados', methods=['GET','POST'])
def listar_empleados():
    data = {}
    data2={
        'titulo':'Empleados',
        'Bienvenida':'EMPLEADOS',
        'counter':1
    } #filtro
    if request.method== 'POST': 
        nombre= request.form['txtNombre']
        try:
            cursor = conexion.connection.cursor()
            # cuando hay fechas y where con %, en la fecha se usa %% para que funcione, %%d-%%m-%%Y = DDMMYYYY o %%d-%%m-%%y= DDMMYY
            sql = "SELECT codigo,nombre,edad,direccion,sexo,DATE_FORMAT(fecha_nacimiento, '%%d-%%m-%%Y') AS fecha,sueldo FROM empleado where nombre=%s"
            cursor.execute(sql,(nombre,))
            empleados = cursor.fetchall()
            data=[]        
            columName=[columna[0] for columna in cursor.description]
            for record in empleados:
                data.append(dict(zip(columName, record)))
        except Exception as ex:
            data['mensaje'] = 'Error...'
        return render_template('Empleados.html', data=data, data2=data2)
    else:#listar normal
        try:
            print("llego al listar normal")
            cursor = conexion.connection.cursor()
            sql = "SELECT codigo,nombre,edad,direccion,sexo,DATE_FORMAT(fecha_nacimiento, '%d-%m-%Y') AS fecha,sueldo,imagen FROM empleado"
            cursor.execute(sql)
            empleados = cursor.fetchall()
            data=[]        
            columName=[columna[0] for columna in cursor.description]
            for record in empleados:
                data.append(dict(zip(columName, record)))
        except Exception as ex:
            data['mensaje'] = 'Error...'
        return render_template('Empleados.html', data=data, data2=data2)


@app.route('/ordenar_empleados/<string:ord>')
def ordenar_empleados(ord):
    data = {}
    data2={
        'titulo':'Empleados',
        'Bienvenida':'EMPLEADOS'
    }
    try:
        cursor = conexion.connection.cursor()
        if ord:
            sql = f"SELECT codigo,nombre,edad,direccion,sexo,DATE_FORMAT(fecha_nacimiento, '%d-%m-%Y') AS fecha,sueldo FROM empleado ORDER BY {ord}"
        cursor.execute(sql)
        empleados = cursor.fetchall()#usar fetchall, fetchone da error
        data=[]        
        columName=[columna[0] for columna in cursor.description]
        for record in empleados:
            data.append(dict(zip(columName, record)))
    except Exception as ex:
        data['mensaje'] = 'Error...'
    return render_template('Empleados.html', data=data, data2=data2)


@app.route('/guardar_empleado', methods=['POST'])
def guardar_empleado():
    data2={
        'titulo':'Empleados',
        'Bienvenida':'EMPLEADOS',
        'counter':1
    }
    nombre= request.form['txtNombre']
    direccion= request.form['txtDireccion']
    sexo= request.form['btnrSexo']
    fechad= request.form['txtFecha']
    fecha = datetime.strptime(fechad, '%Y-%m-%d')#trasforma la fecha tipo varchar a datetime
    edad = relativedelta(datetime.now(), fecha)#hace el calculo de edad en formato YYYY-MM-DD
    edad=edad.years #para guardar solo el año
    sueldo= request.form['txtSueldo']
    imagen = request.files['imagen'].read()
    if nombre and edad and direccion and sexo and fecha and sueldo and imagen:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM empleado where nombre=%s"
        cursor.execute(sql,(nombre,))
        empleados = cursor.fetchall()
        if empleados is None or empleados==():#si no encontro datos
            cursor = conexion.connection.cursor()
            sql = "INSERT INTO empleado(nombre, edad, direccion, sexo, fecha_nacimiento, sueldo, imagen) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            data=(nombre,edad,direccion,sexo,fecha,sueldo,imagen) 
            cursor.execute(sql, data)
            conexion.connection.commit()
            flash('Datos guardados ok','alert-success')
        else:
            flash('ERROR: El empleado ya existe','alert-danger')
    return redirect(url_for('listar_empleados'))

@app.route('/delete_empleado/<string:id>')
def delete_empleado(id):
    cursor = conexion.connection.cursor()
    sql = "DELETE FROM empleado WHERE codigo=%s"
    data=(id,)
    cursor.execute(sql, data)
    conexion.connection.commit()
    flash('Datos eliminados ok','alert-success')
    return redirect(url_for('listar_empleados'))

@app.route('/update_empleado/<string:codigo>', methods=['POST'])
def update_empleado(codigo):
    nombre= request.form['txtNombre']
    direccion= request.form['txtDireccion']
    sexo= request.form['btnrSexoModal']
    fechad= request.form['txtFecha']
    fecha = datetime.strptime(fechad, '%Y-%m-%d')#trasforma la fecha tipo varchar a datetime
    edad = relativedelta(datetime.now(), fecha)#hace el calculo de edad en formato YYYY-MM-DD
    edad=edad.years #para guardar solo el año
    sueldo= request.form['txtSueldo']
    imagen = request.files['imagen'].read()
    if nombre and edad and direccion and sexo and fecha and sueldo and imagen:
        cursor = conexion.connection.cursor()
        sql = "UPDATE empleado SET nombre=%s, edad=%s, direccion=%s, sexo=%s, fecha_nacimiento=%s, sueldo=%s, imagen=%s where codigo=%s"
        #si no se pone codigo da error
        #si sepone codigo al inicio no da error pero no hace el update
        data=(nombre,edad,direccion,sexo,fecha,sueldo,imagen,codigo) #se pone el codigo en ese orden ya que el codigo se usa en la consulta
        cursor.execute(sql, data)
        conexion.connection.commit()
        flash('Datos actualizados ok','alert-success')
    return redirect(url_for('listar_empleados'))

@app.template_filter('datetimeformat')
def datetimeformat(value, format='%Y-%m-%d'):
    return datetime.strptime(value, '%d-%m-%Y').strftime(format)


@app.route('/mostrar_imagen/<string:id>')
def mostrar_imagen(id):
    print("llego a funcion imagen")
    print(id)
    cursor = conexion.connection.cursor()
    sql = "SELECT imagen from empleado where codigo=%s"#para que esta linea muestra el codigo amarillo en consola
    data = (id,)  # Asegúrate de pasar el código como una tupla
    cursor.execute(sql, data)
    image_data = cursor.fetchone()
    if image_data:
        # Extrae la imagen de la tupla
        imagen_bytes = image_data[0]
        return send_file(io.BytesIO(imagen_bytes), mimetype='image/jpeg')
    else:
        return "Imagen no encontrada", 404

#funcion para exportar
@app.route('/download', methods=['POST'])
def download():
    data = request.form.get('table_data')
    current_date = datetime.now().strftime("%Y%m%d")
    file_name = f"csv_{current_date}.csv"
    file_path = request.form.get('file_path', '/descargas/')
    full_path = os.path.join(file_path, file_name)

    csv_data = data.split('\n')
    response = Response(
        '\n'.join(csv_data),
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment;filename={file_name}'}
    )
    return response

#para importar, tiene que ser un upload diferente para cada tabla
@app.route('/uploadProductos', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        data = pd.read_csv(file)

        cursor = conexion.connection.cursor()
        for i, row in data.iterrows():
            sql = "INSERT INTO producto(nombre, stock, stock_min, estado, codigoTipo) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, tuple(row))
        conexion.connection.commit()
        return 'Datos importados exitosamente'
    return redirect(url_for('listar_productos'))


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

