from sqlite3 import connect
from flask import Flask
from flask import render_template,request , redirect
from flaskext.mysql import MySQL

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


@app.route("/libros")
def libros():
    return render_template('sitio/libros.html') 


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
    conexion.commit
    print(libros)
    print(conexion)

    return render_template("admin/libros.html",libros=libros)

@app.route("/admin/libros/guardar",methods=['POST'])
def admin_libros_guardar():
    _nombre=request.form['txtNombre']#recepcion de los archivos (va el mismo nombre que se le dio al input en el form)  
    _url=request.form['txtURL'] #recepcion de los archivos (va el mismo nombre que se le dio al input en el form)
    _archivo=request.files["txtImagen"] #recepcion de las imagenes (va el mismo nombre que se le dio al input en el form)

    sql = "INSERT INTO `libros` (`id`, `nombre`, `imagen`, `url`) VALUES (NULL, %s, %s, %s);"
    datos=(_nombre,_archivo.filename,_url)

    conexion = mysql.connect()#se genera la conexion
    cursor= conexion.cursor()#se genera el cursor
    cursor.execute(sql,datos)#el cursor ejecuta la instruccion sql y se integra los datos (que enviara el usuario)
    conexion.commit()# se hace una creacion 

    print(_nombre)
    print(_archivo)
    print(_url)
    return redirect('/admin/libros')

if __name__=='__main__':
    app.run(debug=True) 