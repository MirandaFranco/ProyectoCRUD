from flask import Flask, request, jsonify
from flask_cors import CORS 
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow 


#crear la aplicacion    

app = Flask(__name__)

#utilizar CORS permite el acceso al front end

CORS(app)

#Configurar la base de datos desde la app, se le informa donde va a estar

# configuro la base de datos, con el nombre el usuario y la clave
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root@localhost/alumnos'
# URI de la BBDD. Driver de la BD user:clave@URLBBDD/nombreBBDD
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #none

#crear el objeto db
#Notificamos a la app que trabajara con SQLAlchemy
db = SQLAlchemy(app)

#objeto que nos permite acceder a los metodos para transformar datos
ma = Marshmallow(app)

#Definicion de la clase Producto

class Alumno(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(100))
    apellido = db.Column(db.String(400))
    DNI = db.Column(db.Integer)
    telefono = db.Column(db.Integer)
   


    def __init__(self,nombre,apellido,DNI,telefono):
        self.nombre=nombre 
        self.apellido=apellido
        self.DNI=DNI
        self.telefono=telefono
        


#codigo de creacion de tabla

with app.app_context():
    db.create_all()


#Crea una clase ProductoSchema, donde se definen los campos de la tabla

class AlumnoSchema(ma.Schema):
    class Meta:
        fields=('id','nombre','apellido','DNI','telefono')

#Crear dos objetos para transformar

alumno_schema = AlumnoSchema() #permitir convertir un solo dato. Ej: 1 objeto
alumnos_schema= AlumnoSchema(many=True) #convertir un listado de datos a json

#18. CREAR LAS RUTAS PARA: productos
#'/productos' ENDPOINT PARA MOSTRAR TODOS LOS PRODUCTOS DISPONIBLES EN LA BASE DE DATOS: GET

@app.route('/alumnos', methods=['GET'])

def get_alumnos():
    #consulta toda la info de la tabla productos
    all_alumnos = Alumno.query.all()
    return alumnos_schema.jsonify(all_alumnos)

#'/productos' ENDPOINT PARA RECIBIR DATOS: POST
# '/productos' ENDPOINT PARA RECIBIR DATOS: POST
@app.route('/alumnos', methods=['POST']) # crea ruta o endpoint
def create_alumno():
    # request.json contiene el json que envio el cliente
    # Para insertar registro en la tabla de la base de datos
    # Se usará la clase Producto pasándole cada dato recibido.
    # Para agregar los cambios a la db con db.session.add(objeto)
    # Para guardar los cambios a la db con db.session.commit()
    # Entrada de datos:
#     {
#       "imagen": "https://picsum.photos/200/300?grayscale",
#       "nombre": "MICROONDAS",
#       "precio": 50000,
#       "stock": 10
#    }

    nombre=request.json['nombre']
    apellido=request.json['apellido']
    DNI=request.json['DNI']
    telefono=request.json['telefono']
    

    new_alumno=Alumno(nombre,apellido,DNI,telefono)
    db.session.add(new_alumno)
    db.session.commit()

    # Retornar los datos guardados en formato JSON 
    # Para ello, usar el objeto producto_schema para que convierta con                   # jsonify los datos recién ingresados que son objetos a JSON  
    return alumno_schema.jsonify(new_alumno)


# '/productos/<id>' ENDPOINT PARA MOSTRAR UN PRODUCTO POR ID: GET
@app.route('/alumnos/<id>',methods=['GET'])
def get_alumno(id):
    # Consultar por id, a la clase Producto.
    #  Se hace una consulta (query) para obtener (get) un registro por id
    alumno=Alumno.query.get(id)

   # Retorna el JSON de un producto recibido como parámetro
   # Para ello, usar el objeto producto_schema para que convierta con                   # jsonify los datos recién ingresados que son objetos a JSON  
    return alumno_schema.jsonify(alumno)   


# '/productos/<id>' ENDPOINT PARA BORRAR UN PRODUCTO POR ID: DELETE
@app.route('/alumnos/<id>',methods=['DELETE'])
def delete_alumno(id):
    # Consultar por id, a la clase Producto.
    #  Se hace una consulta (query) para obtener (get) un registro por id
    alumno=Alumno.query.get(id)
    
    # A partir de db y la sesión establecida con la base de datos borrar 
    # el producto.
    # Se guardan lo cambios con commit
    db.session.delete(alumno)
    db.session.commit()
    
    # Devuelve un json con el registro eliminado
    # Para ello, usar el objeto producto_schema para que convierta con                     # jsonify el dato recién eliminado que son objetos a JSON  
    return alumno_schema.jsonify(alumno)   


# '/productos/<id>' ENDPOINT PARA MODIFICAR UN PRODUCTO POR ID: PUT
@app.route('/alumnos/<id>', methods=['PUT'])
def update_alumno(id):
    # Consultar por id, a la clase Producto.
    #  Se hace una consulta (query) para obtener (get) un registro por id
    alumno=Alumno.query.get(id)
 
    #  Recibir los datos a modificar
    nombre=request.json['nombre']
    apellido=request.json['apellido']
    DNI=request.json['DNI']
    telefono=request.json['telefono']

    # Del objeto resultante de la consulta modificar los valores  
    alumno.nombre=nombre
    alumno.apellido=apellido
    alumno.DNI=DNI
    alumno.telefono=telefono
#  Guardar los cambios
    db.session.commit()
# Para ello, usar el objeto producto_schema para que convierta con                     # jsonify el dato recién eliminado que son objetos a JSON  
    return alumno_schema.jsonify(alumno)
#'/productos/<id>' ENDPOINT PARA MOSTRAR UN PRODUCTO POR ID: GET
#'/productos/<id>' ENDPOINT PARA BORRAR UN PRODUCTO POR ID: DELETE
#'/productos/<id>' ENDPOINT PARA MODIFICAR UN PRODUCTO POR ID: PUT

#Bloque principal

if __name__ == '__main__':
    app.run(debug=True)

