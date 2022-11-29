from pymongo import MongoClient
import certifi

class ConexionDB:
    USUARIO_DB = "admin"
    PASSWORD_DB = "admin1234"
    MONGO_URI = "mongodb+srv://admin:admin1234@cluster0.dalbuox.mongodb.net/?retryWrites=true&w=majority"

    def __init__(self,db_name):
        self.cliente = None
        self.db = None
        self.conectar(db_name)

    def conectar(self,db_name):
        try:
            ca = certifi.where()
            self.cliente = MongoClient(ConexionDB.MONGO_URI, tlsCAFile=ca)
            self.db =  self.cliente[db_name] 
        except ConnectionError:
            print("Error en la conexion con la db")
        

    def obtener_db(self):
        return self.db

    def mostrar_dbs(self):
        print("bds...")
        print(self.cliente.list_database_names())

    # def crear_db(self,db):
    #     self.db = self.cliente[db]

    # def crear_coleccion(self,nombre):
    #     try:
    #         col = self.db[nombre]
    #         print("Coleccion {} creada",col)
    #         return col
    #     except:
    #         print("nombre de la coleccion invalido")
    
    # def crear_datos(self,col,datos):
    #     col.insert_one(datos)
    #     pass
    
    # def leer_datos(self,col):
    #     documentos = col.find({})
    #     for documento in documentos:
    #         print(documento)




# def main ():
#     #conexion = ConexionDB()
#     #conexion.crear_db("prueba")
#     #conexion.mostrar_dbs()
#     #db.close()
    

# if __name__ == "__main__":
#     main()
    