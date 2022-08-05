import os
from flask import Flask
from flask import render_template,request , redirect
from flaskext.mysql import MySQL
from datetime import datetime
from flask import send_from_directory
app = Flask(__name__)
mysql=MySQL()

app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='sitio'
mysql.init_app(app) #inicializar

@app.route('/')
def inicio():
    return render_template('sitio/index.html')

@app.route("/img/<imagen>")
def imagenes(imagen):
    print(imagen)
    return send_from_directory(os.path.join('templates/sitio/img'),imagen)

@app.route("/libros")
def libros():

    conexion=mysql.connect()#conexion con la bd
    cursor = conexion.cursor()#cursor
    cursor.execute("SELECT * FROM `libros` ")
    libros = cursor.fetchall()#recuperacion de los ,obros y almacenamiento en la variable "libros"
    conexion.commit() 
        
    return render_template('sitio/libros.html',libros=libros) 


@app.route("/nosotros")
def nosotros():
    return render_template('sitio/nosotros.html')


@app.route("/admin/")
def admin_index():
    return render_template('admin/index.html')

@app.route("/admin/login")
def admin_login():
    return render_template('admin/login.html')

@app.route("/admin/libros")
def admin_libros():
    conexion=mysql.connect()#conexion con la bd
    cursor = conexion.cursor()#cursor
    cursor.execute("SELECT * FROM `libros` ")
    libros = cursor.fetchall()#recuperacion de los ,obros y almacenamiento en la variable "libros"
    conexion.commit()
    print(libros)
    print(conexion) 

    return render_template("admin/libros.html",libros=libros)

@app.route("/admin/libros/guardar",methods=['POST'])
def admin_libros_guardar():
    _nombre=request.form['txtNombre']#recepcion de los archivos (va el mismo nombre que se le dio al input en el form)  
    _url=request.form['txtURL'] #recepcion de los archivos (va el mismo nombre que se le dio al input en el form)
    _archivo=request.files["txtImagen"] #recepcion de las imagenes (va el mismo nombre que se le dio al input en el form)


    tiempo = datetime.now()#hora actual
    horaActual= tiempo.strftime('%Y%H%M%S')#formato 

    if _archivo.filename!="":
        nuevoNombre=horaActual+"_"+_archivo.filename#formato del nombre del archivo
        _archivo.save("templates/sitio/img/"+nuevoNombre)#guardamos en la carpeta img las imagenes


    sql = "INSERT INTO `libros` (`id`, `nombre`, `imagen`, `url`) VALUES (NULL, %s, %s, %s);"
    datos=(_nombre,nuevoNombre,_url)

    conexion = mysql.connect()#se genera la conexion
    cursor= conexion.cursor()#se genera el cursor
    cursor.execute(sql,datos)#el cursor ejecuta la instruccion sql y se integra los datos (que enviara el usuario)
    conexion.commit()# se hace una creacion 

    print(_nombre)
    print(_archivo)
    print(_url)
    return redirect('/admin/libros')

@app.route("/admin/libros/borrar",methods=['POST'])
def admin_libros_borrar():
    _id=request.form['txtID']#recepcionamos el id
    print(_id)

    conexion=mysql.connect()#conexion con la bd
    cursor = conexion.cursor()#cursor
    cursor.execute("SELECT imagen FROM `libros` WHERE id =%s ",(_id))
    libro = cursor.fetchall()#recuperacion de los ,obros y almacenamiento en la variable "libros"
    conexion.commit()
    print(libro)
    
    if os.path.exists("templates/sitio/img/"+str(libro[0][0])):
        os.unlink("templates/sitio/img/"+str(libro[0][0]))

    conexion=mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("DELETE  FROM `libros` WHERE id =%s ",(_id))
    conexion.commit()


    return redirect('/admin/libros')
if __name__=='__main__':
    app.run(debug=True) 