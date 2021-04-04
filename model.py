from services import *

class Models:
    
    def login(self):
        data = dataTableMysql("SELECT nombres, correo, usuario, password, id_provisional FROM usuarios WHERE usuario = '{}'".format(self.info['user']))

        return data

    def register(self):
        hash_password = cryptStringBcrypt(self.info['password'])
        _randomID = getBigRandomString()
        
        data = dataTableMysql("INSERT INTO usuarios(nombres, correo, usuario, password, id_provisional) VALUES('{}', '{}', '{}', '{}','{}')".format(self.info['name'], self.info['email'], self.info['user'], hash_password, _randomID), "rowcount")

        return data