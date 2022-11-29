class Usuario:
    def __init__(self,usuario,password,email,edad):
        self.usuario = usuario
        self.password = password
        self.email = email
        self.edad = edad

    def obtener_usuario(self):
        return{
            'usuario':self.usuario,
            'password':self.password,
            'email':self.email,
            'edad':self.edad,
        }

class Venta:
    def __init__(self,usuario,monto,tipo):
        self.usuario = usuario
        self.monto = monto
        self.tipo = tipo

    def obtener_venta(self):
        return{
            'usuario':self.usuario,
            'monto':self.monto,
            'tipo':self.tipo,
        }
    