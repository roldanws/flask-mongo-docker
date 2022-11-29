from flask import Flask, render_template,jsonify, request
import json
from database import ConexionDB
from colections import Usuario,Venta
from werkzeug.security import generate_password_hash,check_password_hash
from functools import wraps
import jwt
import datetime
app = Flask(__name__)

conexion = ConexionDB('prueba')
db = conexion.obtener_db()

app.config['SECRET_KEY']='Th1s1ss3cr3t'

#app.register_blueprint(bp_api)
#Rutas de la api
def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'],algorithms=["HS256"])
            #current_user = Users.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'token is not valid'})

        return f(data['public_id'],*args, **kwargs)
    return decorator

@app.route('/api/login', methods=['GET', 'POST'])  
def login_user(): 
    auth = request.authorization   

    if not auth or not auth.username or not auth.password:
        return jsonify({'WWW.Authentication':"could not verified"})

    usuarios = db['usuario']

    usuario = usuarios.find_one({'usuario':auth.username})
    password = usuario['password']
    usuario_id = usuario['usuario']
    print("Password del usuario en hash:",password)
    #usuario = Usuario(usuario['usuario'],usuario['password'],usuario['email'],usuario['edad'])
    #usuario_dict = usuario.obtener_usuario()
        
    if check_password_hash(password, auth.password):  
        token = jwt.encode({'public_id': usuario_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])  
        # return jsonify({'token' : token.decode('UTF-8')}) 
        return jsonify({'token' : token})
        #return jsonify({'token' : token}) 

    return jsonify({'WWW.Authentication':"login required"})

@app.route('/api/create/venta',methods=['POST'])
def create_venta():
    ventas = db['venta']
    data = json.loads(request.data)
    print(data)
    try:
        usuario = data['usuario']
        print(usuario)
        print("llegando a usuario")

        monto = data['monto']
        print("llegando a monto")

        tipo = data['tipo']
    except:
        return jsonify({'datos':'incompletos'})
    if usuario and monto and tipo:
        venta = Venta(usuario,monto,tipo)
        venta_dict = venta.obtener_venta()
        ventas.insert_one(venta_dict)
        print("Se inserto exitosamente: ",venta.obtener_venta())
        return jsonify(venta.obtener_venta())
    else:
        print("datos incompletos")
        return jsonify({'datos':'vacios'})


@app.route('/api/venta',methods=['GET'])
@token_required
def obtener_venta_api(current_user):
    ventas = db['venta']
    data = json.loads(request.data)
    try:
        usuario = data['usuario']
    except:
        return jsonify({'datos':'incompletos'})
    
    if usuario:
        venta_usuario = ventas.find_one({'usuario':usuario})
        venta = Venta(venta_usuario['usuario'],venta_usuario['monto'],venta_usuario['tipo'])
        venta_dict = venta.obtener_venta()

        print(venta_dict,type(venta_dict))
        return jsonify(venta_dict)
    else:
        return jsonify({'datos':'vacios'})


@app.route('/api/create/usuario',methods=['POST'])
@token_required
def crear_usuario_api(current_user):
    if current_user == "admin":
        usuarios = db['usuario']
        data = json.loads(request.data)
        try:
            usuario_id = data['usuario']
            password = data['password']
            email = data['email']
            edad = data['edad']
        except:
            return jsonify({'datos':'incompletos'})
        if usuario_id and password and email and edad:
            hash_password = generate_password_hash(password,method="sha256")
            usuario = {
                'usuario':usuario_id,
                'password':hash_password,
                'email':email,
                'edad':edad,
                
            }
            usuarios.insert_one(usuario)
            #Se borra el añadido automatico del campo _id objeto creado
            del usuario['_id']
            print("Se inserto exitosamente: ",usuario)
            return jsonify(usuario)
        else:
            return jsonify({'datos':'vacios'})
    else:
        return jsonify({'Err':'No tienes permiso de superusuario'})

        
        

#Rutas de la aplicacion
@app.route('/', methods=['GET'])
def hola():
    return render_template('index.html')

@app.route('/crear-usuario',methods=['POST'])
def crear_usuario():
    usuarios = db['usuario']
    usuario_id = request.form['usuario']
    password = request.form['password']
    email = request.form['email']
    edad = request.form['edad']
    if usuario_id and password and email and edad:
        hash_password = generate_password_hash(password,method="sha256")
        usuario = {
            'usuario':usuario_id,
            'password':hash_password,
            'email':email,
            'edad':edad
        }
        usuarios.insert_one(usuario)
        print("Se inserto exitosamente: ",usuario)
        return jsonify({'usuario':'insertado'})
    else:
        return jsonify({'error':'err'})

        #personas.insert_one(persona)

    # print("OKkk ", personas.count_documents({}))
    # print("OKkk2 ", db.list_collection_names())
    # for persona in personas.find({}):
    #     print(persona)
    #return persona
    #conexion.mostrar_dbs()

if __name__ == "__main__":
    app.run(debug=True)