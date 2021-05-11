from services import *
from servicesAsync import *

class Models:
    
    def login(self):

        Response = {"logged": False, "token": None, "name": None, "email": None, "user": None}

        querySQL = ""
        type = self.info['type']
        id_token = self.info['id_token'] if self.info['id_token'] else None

        if type == "Google" and id_token:
            email = decodeAuth2CertGoogleAPI_GO(id_token)
            if email[0] and email[1]['email_verified']:
                querySQL = "SELECT id_usuario, nombres, correo, usuario FROM usuarios WHERE correo = '{}'".format(email[1]['email'])
            else:
                return Response
        elif type == "normal" and not id_token:
            querySQL = "SELECT id_usuario, nombres, correo, usuario, password FROM usuarios WHERE usuario = '{}'".format(self.info['user'])
        else:
            return Response

        dataDB = dataTableMysql(querySQL)

        if dataDB and type == "normal":
            for data in dataDB:
                if decryptStringBcrypt(self.info['password'], data[4]):
                    jwt = encoded_jwt(data[0])
                    Response = {"logged": True, "token": jwt, "name": data[1], "email": data[2], "user": data[3]}
                    return Response
                else:
                    return Response
        elif dataDB and type == "Google":
            for data in dataDB:
                if email[1]['email'] != data[2][0:len(email[1]['email'])]:
                        return Response

                jwt = encoded_jwt(data[0])
                Response = {"logged": True, "token": jwt, "name": data[1], "email": data[2], "user": 'GoogleUser'}
                return Response
        else:
            return Response

    def register(self):
        Response = {
            'registered': False
        }

        querySQL = ""

        type = self.info['type']
        id_token = self.info['id_token'] if self.info['id_token'] else None

        if type == "Google" and id_token:
            deAuth2 = decodeAuth2CertGoogleAPI_GO(id_token)
            if deAuth2[0] and deAuth2[1]['email_verified']:
                hash_password = cryptStringBcrypt(str(getBigRandomString() + getMinRandomString()))

                querySQL = "INSERT INTO usuarios(nombres, correo, usuario, password) VALUES('{}', '{}', '{}', '{}')".format(deAuth2[1]['name'], deAuth2[1]['email'], deAuth2[1]['email'] + str(hash_password), hash_password)
            else:
                return Response
        elif type == "normal" and not id_token:
            hash_password = cryptStringBcrypt(self.info['password'])
            querySQL = "INSERT INTO usuarios(nombres, correo, usuario, password) VALUES('{}', '{}', '{}', '{}')".format(self.info['name'], self.info['email'], self.info['user'], hash_password)
        else:
            return Response
        
        data = dataTableMysql(querySQL, "rowcount")

        Response = {
            'registered': data
        }

        return Response

    # Manage Events
    def getEvents(self):
        Response = {
            'auth_token': False,
            'events': []
        }

        if not checkJwt(self.info['token']):
            return Response
        
        user_id = decode_jwt(self.info['token']).get("user_id")

        if user_id:
            queryUserSQL = "SELECT id_usuario FROM usuarios WHERE id_usuario = '{}'".format(user_id)

            dataUserDB = dataTableMysql(queryUserSQL)
            if dataUserDB:
                Response['auth_token'] = True

                dataDB = dataTableMysql("SELECT id, titulo, time_format(hora, '"'%h:%i %p'"') as hour, CASE WHEN DAY(fecha) <= 9 THEN CONCAT('0', DAY(fecha)) ELSE DAY(fecha) END as DAY, CASE WHEN MONTH(fecha) <= 9 THEN CONCAT('0', MONTH(fecha)) ELSE MONTH(fecha) END as MONTH, YEAR(fecha) as year, descripcion, codigo, tipo_ev, icono FROM eventos WHERE codigo = {} ORDER BY fecha ASC, hora ASC".format(user_id))

                for data in dataDB:
                    Response['events'].append({
                        'id': data[0],
                        'title': data[1],
                        'hour': data[2],
                        'day': data[3],
                        'month': data[4],
                        'year': data[5],
                        'description': data[6],
                        'check': False,
                        'type_ev': data[8],
                        'icon': data[9]
                    })
            
        return Response

    def registerEvents(self):
        Response = {
            'auth_token': False,
            'saved': False
        }

        if not checkJwt(self.info['token']):
            return Response
        
        user_id = decode_jwt(self.info['token']).get("user_id")
        print(self.info['hour'])

        dataDB = dataTableMysql("INSERT INTO eventos(titulo, hora, fecha, descripcion, codigo, tipo_ev, icono) VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(self.info['title'], self.info['hour'], self.info['date'], self.info['description'], user_id, self.info['type_ev'], self.info['icon'] if len(self.info['icon']) >= 1 else ""), "rowcount")

        Response = {
            'auth_token': True,
            'saved': dataDB
        }

        return Response

    def changeEvents(self):
        Response = {
            'auth_token': False,
            'saved': False
        }

        try:
            check_jwt = checkJwt(self.info['token'])

            if not check_jwt:
                return Response
            else:
                Response['auth_token'] = True

            id_event = str(self.info['id_event'])

            check_id_event = checkStringNumberSizeType(id_event, len(id_event))
            
            if not check_id_event:
                return Response

            user_id = decode_jwt(self.info['token']).get("user_id")

            dataDB = dataTableMysql("UPDATE eventos SET titulo = '{}', hora = '{}', fecha = '{}', descripcion = '{}', tipo_ev = '{}', icono = '{}' WHERE codigo = '{}' AND id = '{}'".format(self.info['title'], self.info['hour'], self.info['date'], self.info['description'], self.info['type_ev'], self.info['icon'] if len( self.info['icon']) >= 1 else "", user_id, id_event), "rowcount")

            Response['saved'] = True

            return Response
        except Exception as e:
            print("ERROR IN changeEvents (Model):")
            print(e)
            return Response

    def deleteEvents(self):
        Response = {
            'auth_token': False,
            'deleted': False
        }

        if not checkJwt(self.info['token']) and not id_event:
            return Response
        
        user_id = decode_jwt(self.info['token']).get("user_id")

        Response['auth_token'] = True

        events = self.info['events'].split(',') if self.info['events'] else None

        for item in events:
            if not checkIfNumberInt(item):
                return Response

        for item in events:
            deleteEvent = dataTableMysql("DELETE FROM eventos WHERE id = '{}' and codigo = '{}' ".format(item, user_id), "rowcount")
            if deleteEvent:
                Response['deleted'] = True
            else:
                Response['deleted'] = False

        return Response

    # Recovery Account
    def recoveryAccount(self):
        Response = {'recovering': False, 'token': None}
        querySQL = ''

        type = self.info['type'] if self.info['type'] else None
        account = self.info['account'] if self.info['account'] else None

        if type == "number" and account:
            if not checkStringNumberTel(account):
                return Response
            else:
                querySQL = "SELECT numero, id_provisional, correo, nombres, usuario FROM usuarios WHERE numero = '{}'".format(account[2::])
        elif type == "email" and account:
            if not checkStringEmail(account):
                return Response
            else:
                querySQL = "SELECT id_provisional, correo, nombres, usuario FROM usuarios WHERE correo = '{}';".format(account)
        else:
            return Response

        dataDB = dataTableMysql(querySQL)
        
        if dataDB:
            for data in dataDB:
                if type == "number":

                    # Validate if not Google
                    if data[2] == data[4][0:len(data[2])]:
                        return Response

                    codeRandom = createRandomNumberSize(6)
                    
                    # Using threads for send email and SMS
                    rootAsync = sendEmailAndSMSThreading(info = {
                        'S-Email': {
                                'subject': 'Reestablecer contraseña',
                                'receiver': data[2],
                                'userRec': {'name': data[3]},
                                'reason': '2'
                            },
                        'S-SMS': {
                                'number': account,
                                'msg': 'Calenbell+code+'+codeRandom
                            }})

                    sendAlerts = rootAsync.run()

                    if sendAlerts:
                        verifyCodeEnc = encWithPass("{'account': '"+account+"', 'code': '"+codeRandom+"'}")

                        Response['recovering'] = True

                        Response['token'] = createJwt(info={'verify':verifyCodeEnc[1]}, time=5)
                elif type == "email":
                    if account == data[3][0:len(account)]:
                        return Response
                        
                    codeRandom = createRandomNumberSize(6)
                    
                    sendByEmail = sendEmail(receiver=data[1], subject='Reestablecer contraseña', userRec={'name': data[2], 'code': codeRandom}, reason="3")

                    if sendByEmail:
                        verifyCodeEnc = encWithPass("{'account': '"+account+"', 'code': '"+codeRandom+"'}")
                        Response['recovering'] = True
                        Response['token'] = createJwt(info={'verify':verifyCodeEnc[1]}, time=5) 
                else:
                    return Response

        return Response

    def validateCodeRecoveryAccount(self):
        token = decode_jwt(self.info['token'])
        Enc = token.get("info")['verify']
        accountToken = decWithPass(dataEnc=Enc, isJson=True)[1]['account']
        codeToken = decWithPass(dataEnc=Enc, isJson=True)[1]['code']
        
        # validate code token and account
        
        codeValidate = checkStringNumberSizeType(number=self.info['code'], size=6)
        codeTokenValidate = checkStringNumberSizeType(number=codeToken, size=6)

        accountDetector = checkStringNumberSizeType(number=accountToken, size=12)

        querySQL = ''
        Response = {
            'recovered': False,
            'token': None
        }

        if codeValidate and token and codeTokenValidate:
            if self.info['code'] != codeToken:
                return Response
                
            if accountDetector:
                # type number
                querySQL = "SELECT numero FROM usuarios WHERE numero = '{}'".format(accountToken[2:12])
            else:
                # type email
                querySQL = "SELECT correo FROM usuarios WHERE correo = '{}'".format(accountToken)
        else:
            return Response

        dataDB = dataTableMysql(querySQL)

        if dataDB:
            Response['recovered'] = True
            Response['token'] = createJwt(info={'verify': Enc, 'recovered': True}, time=5) 

        return Response

    def validateChangePwd(self):
        token = decode_jwt(self.info['token'])

        Enc = token.get("info")['verify']

        accountRecovered = token.get("info")['recovered']

        accountToken = decWithPass(dataEnc=Enc, isJson=True)[1]['account']

        accountDetector = checkStringNumberSizeType(number=accountToken, size=12)

        passwordForChange = self.info['pwd'] if self.info['pwd'] else None

        querySQL = ''
        querySQLChangePWD = ''

        Response = {
            'recovered': False
        }

        if token and accountRecovered and accountToken and Enc and passwordForChange:
            if accountDetector:
                # number
                querySQL = "SELECT numero FROM usuarios WHERE numero = '{}'".format(accountToken[2:12])
            else:
                # email
                querySQL = "SELECT correo FROM usuarios WHERE correo = '{}'".format(accountToken)
        else:
            return Response

        dataDB = dataTableMysql(querySQL)

        if dataDB:
            
            hash_password = cryptStringBcrypt(passwordForChange)

            if accountDetector:
                # number
                querySQLChangePWD = "UPDATE usuarios SET password = '{}' WHERE numero = '{}'".format(hash_password, accountToken[2:12])
            else:
                # email
                querySQLChangePWD = "UPDATE usuarios SET password = '{}' WHERE correo = '{}'".format(hash_password, accountToken)
            
        
        dataDBC = dataTableMysql(querySQLChangePWD, "rowcount")

        if dataDBC and querySQLChangePWD:
            Response['recovered'] = True


        return Response

