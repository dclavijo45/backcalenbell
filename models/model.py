from services.services import *
from services.servicesAsync import *

class Models:
    
    def login(self):

        Response = {"logged": False, "token": None, "name": None, "email": None, "user": None, "photo": None, "id": None}

        querySQL = ""
        type = self.info['type']
        id_token = self.info['id_token'] if self.info['id_token'] else None

        if type == "Google" and id_token:
            email = decodeAuth2CertGoogleAPI_GO(id_token)
            if email[0] and email[1]['email_verified']:
                querySQL = "SELECT id_usuario, nombres, correo, usuario, foto_perfil FROM usuarios WHERE correo = '{}'".format(email[1]['email'])
            else:
                return Response
        elif type == "normal" and not id_token:
            querySQL = "SELECT id_usuario, nombres, correo, usuario, password, foto_perfil FROM usuarios WHERE usuario = '{}'".format(self.info['user'])
        else:
            return Response

        dataDB = dataTableMysql(querySQL)

        if dataDB and type == "normal":
            for data in dataDB:
                if decryptStringBcrypt(self.info['password'], data[4]):
                    jwt = encoded_jwt(data[0])
                    Response = {"logged": True, "token": jwt, "name": data[1], "email": data[2], "user": data[3], "photo": data[5], "id": data[0]}
                    return Response
                else:
                    return Response
        elif dataDB and type == "Google":
            for data in dataDB:
                if email[1]['email'] != data[2][0:len(email[1]['email'])]:
                        return Response

                jwt = encoded_jwt(data[0])

                Response = {"logged": True, "token": jwt, "name": data[1], "email": data[2], "user": 'GoogleUser', "photo": data[4], "id": data[0]}
                
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

                querySQL = "INSERT INTO usuarios(nombres, correo, usuario, password, foto_perfil) VALUES('{}', '{}', '{}', '{}', '{}')".format(deAuth2[1]['name'], deAuth2[1]['email'], deAuth2[1]['email'] + str(hash_password), hash_password, deAuth2[1]['picture'])
            else:
                return Response
        elif type == "normal" and not id_token:
            hash_password = cryptStringBcrypt(self.info['password'])
            querySQL = "INSERT INTO usuarios(nombres, correo, usuario, password, foto_perfil) VALUES('{}', '{}', '{}', '{}', 'https://www.dropbox.com/s/4nqmlzijvaeqtts/avatar%20-%20profile.jpeg?dl=1')".format(self.info['name'], self.info['email'], self.info['user'], hash_password)
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
                querySQL = "SELECT id_usuario, numero, correo, nombres, usuario FROM usuarios WHERE numero = '{}'".format(account[2::])
        elif type == "email" and account:
            if not checkStringEmail(account):
                return Response
            else:
                querySQL = "SELECT id_usuario, correo, nombres, usuario FROM usuarios WHERE correo = '{}';".format(account)
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

    # Chat
    def initChatM(self):
        Response = {
            'auth_token': False,
            'token': None,
            'invitation_status': None
        }

        Payload = {
            'friends': None,
            'in_group': None,
            'type_chat': None,
            'receiver': None,
            'transmitter': None,
            'invitation_status': None
        }

        token = decode_jwt(self.info['token'] if self.info['token'] else None)

        if not token:
            return Response

        user_id = token.get("user_id")

        if not checkIfNumberInt(user_id):
            return Response

        Response['auth_token'] = True
        
        type_chat = str(self.info['chat_type']) if self.info['chat_type'] else None

        if len(type_chat) != 1:
            return Response

        if type_chat not  in ['1', '2']:
            return Response

        Payload['type_chat'] = type_chat

        if type_chat == "1":
            id_emisor = user_id

            if not checkIfNumberInt(id_emisor):
                return Response

            Payload['transmitter'] = id_emisor

            id_receptor = self.info['receiver'] if self.info['receiver'] else None

            if not checkIfNumberInt(id_receptor):
                return Response

            if id_emisor == id_receptor:
                return Response

            Payload['receiver'] = id_receptor

            resultado_init = initChat(
                id_emisor = id_emisor,
                id_receptor = id_receptor,
                typeChat = type_chat
                )

            if not resultado_init['existen_usuarios']:
                return Response
            
            Payload['invitation_status'] = resultado_init ['estado_invitacion']

            Payload['friends'] = resultado_init['son_amigos']

            token_val_socket = encoded_jwt(
                user_id = user_id,
                data = {
                    'friends': Payload['friends'],
                    'transmitter': Payload['transmitter'],
                    'receiver': Payload['receiver']
                },
                custom = True
                )
            
            Response['token'] = token_val_socket if token_val_socket else None

            Response['invitation_status'] = Payload['invitation_status']

            return Response

        else:
            id_grupo = self.info['group'] if self.info['group'] else None

            if not checkIfNumberInt(id_grupo):
                return Response
            
            id_emisor = user_id

            if not checkIfNumberInt(id_emisor):
                return Response

            Payload['transmitter'] = id_emisor

            resultado_init = initChat(
                id_emisor = id_emisor,
                id_evento_grupal = id_grupo,
                typeChat = type_chat
                )

            if resultado_init['existe_grupo'] == False:
                return Response

            Payload['invitation_status'] = resultado_init['estado_invitacion']
            
            Payload['in_group'] = resultado_init['pertenece_grupo']

            token_val_socket = encoded_jwt(
                user_id = user_id,
                data = {
                    'in_group': Payload['in_group'],
                    'id_group': id_grupo
                },
                custom = True
            )

            Response['token'] = token_val_socket if token_val_socket else None

            Response['invitation_status'] = Payload['invitation_status']

            return Response

        return Response

    # Manage contacts and groups
    def getContactsG(self):
        Response = {
            'auth_token': False,
            'contacts': [] # dictionary = type, name, id, photo
        }

        if not checkJwt(self.info['token']):
            return Response

        Response['auth_token'] = True
        
        user_id = decode_jwt(self.info['token']).get("user_id")

        fetchContacts = dataTableMysql("SELECT c.id_usuario, c.id_contacto, IF(u.id_usuario = '{}', NULL, u.nombres) AS nombre_usuario, IF(u1.id_usuario = '{}', NULL, u1.nombres) AS nombre_contacto, IF(u.id_usuario = '{}', NULL, u.foto_perfil) as foto_perfil_usuario, IF(u1.id_usuario = '{}', NULL, u1.foto_perfil) as foto_perfil_contacto FROM usuarios u INNER JOIN contactos c ON u.id_usuario=c.id_usuario INNER JOIN usuarios u1 ON u1.id_usuario=c.id_contacto WHERE (u.id_usuario = '{}' OR u1.id_usuario = '{}') AND c.estado_invitacion = 1;".format(user_id,user_id,user_id,user_id,user_id,user_id))

        if not fetchContacts:
            return Response

        for contact in fetchContacts:
            if str(contact[0]) != str(user_id) and str(contact[1]) == str(user_id):
                Response['contacts'].append({
                    'type': 1,
                    'name': contact[2],
                    'id': contact[0],
                    'photo': contact[4]
                })
            
            if str(contact[0]) == str(user_id) and str(contact[1]) != str(user_id):
                Response['contacts'].append({
                    'type': 1,
                    'name': contact[3],
                    'id': contact[1],
                    'photo': contact[5]
                })
            

        fetchGroups = dataTableMysql("SELECT eg.id, eg.id_evento, e.titulo, e.icono from eventos_grupales eg, eventos e WHERE eg.id_evento = e.id and id_usuario = '{}'".format(user_id))

        if not fetchContacts:
            return Response

        for group in fetchGroups:
            Response['contacts'].append({
                'type': 2,
                'name': group[2],
                'id': group[1],
                'photo': group[3]
            })

        return Response

    def searchContacts(self):
        Response = {
            "auth_token": False,
            "users": [] # id, name, photo
        }

        if not checkJwt(self.info['token']):
            return Response

        Response['auth_token'] = True
        
        user_id = decode_jwt(self.info['token']).get("user_id")

        search_key = self.info['search_key'].strip()

        if len(search_key) == 0:
            return Response

        getUsers = dataTableMysql("SELECT id_usuario, nombres, foto_perfil from usuarios WHERE id_usuario != '{}' and nombres like '%{}%'".format(user_id, search_key))

        for user in getUsers:
            Response['users'].append({
                'id': user[0],
                'name': user[1],
                'photo': user[2]
            })
        
        return Response

    def addContacts(self):
        Response = {
            "auth_token": False,
            "send": False,
            "reason": None # Optional: 1 = are friends, 2 = some
        }

        if not checkJwt(self.info['token']):
            return Response

        Response['auth_token'] = True
        
        user_id = decode_jwt(self.info['token']).get("user_id")

        if not checkIfNumberInt(self.info['user_add']):
            return Response

        user_add = self.info['user_add']

        if user_id == user_add:
            Response['reason'] = 2

            return Response

        checkListFriends = dataTableMysql("SELECT * FROM contactos WHERE (id_usuario = '{}' OR id_contacto = '{}')".format(user_id, user_id))

        for data in checkListFriends:
            if str(data[0]) == str(user_id) and str(data[1]) == str(user_add):
                if str(data[2]) == "1": # are friends?
                    Response['reason'] = 1

                    return Response

                if str(data[2]) != "1":
                    deleteForFix = dataTableMysql("DELETE FROM contactos WHERE (id_usuario = '{}') AND (id_contacto = '{}')".format(user_id, user_add))
                    break

            if str(data[1]) == str(user_id) and str(data[0]) == str(user_add):
                if str(data[2]) == "1": # are friends?
                    Response['reason'] = 1

                    return Response

                if str(data[2]) == "0":
                    deleteForFix = dataTableMysql("DELETE FROM contactos WHERE (id_usuario = '{}') AND (id_contacto = '{}')".format(user_add, user_id))
                    break

        addUserToFriendsList = dataTableMysql("INSERT INTO contactos VALUES('{}', '{}', '{}')".format(user_id, user_add, 0), "rowcount")

        if addUserToFriendsList:
            name_get_user = ''
            photo_contact = ''

            name_user_id = dataTableMysql("SELECT nombres, foto_perfil FROM usuarios WHERE id_usuario = '{}'".format(user_id))

            for data in name_user_id:
                name_get_user = data[0]
                photo_contact = data[1]

            info_contact = dataTableMysql("SELECT nombres, correo FROM usuarios WHERE id_usuario = '{}'".format(user_add))

            for data in info_contact:
                Token_Invitation_acepted = encWithPass(
                    data = "{'mode': 'invitation_friends', 'user_sent': '"+str(user_add)+"', 'user_sender': '"+str(user_id)+"', 'status': 'true'}"
                )

                # Token_Invitation_acepted = ""

                # for char in Token_Invitation_acepted_N_URL[1]:
                #     if char.isupper():
                #         Token_Invitation_acepted += "*"+char
                #     else:
                #         Token_Invitation_acepted += char

                Token_Invitation_decline = encWithPass(
                    data = "{'mode': 'invitation_friends', 'user_sent': '"+str(user_add)+"', 'user_sender': '"+str(user_id)+"', 'status': 'false'}"
                )

                # Token_Invitation_decline = ""

                # for char in Token_Invitation_decline_N_URL[1]:
                #     if char.isupper():
                #         Token_Invitation_decline += "*"+char
                #         
                #     else:
                #         Token_Invitation_decline += char

                send_invitation = sendEmail(
                    receiver = data[1],
                    subject = 'Solicitud de amistad',
                    userRec = {
                        'name': data[0],
                        'photo_contact': photo_contact,
                        'name_contact': name_get_user,
                        'link_decline': Token_Invitation_decline[1],
                        'link_acepte': Token_Invitation_acepted[1]
                    },reason = '4')

                if send_invitation:
                    Response['send'] = True
        
        return Response

    def deleteContacts(self):
        Response = {
            'auth_token': False,
            'deleted': False,
            'reason': None # 1 = Joined event group, 2 = invalid payload
        }

        if not checkJwt(self.info['token']):
            return Response

        Response['auth_token'] = True
        
        user_id = decode_jwt(self.info['token']).get("user_id")

        payload = self.info['payload'].split(",") if self.info['payload'] else None

        if payload == None:
            Response['reason'] = 2

            return Response

        id_contactG = payload[0]

        if not checkIfNumberInt(id_contactG):
            Response['reason'] = 2

            return Response
        
        type_contact = payload[1]

        if len(type_contact) != 1 and type_contact not in ['1', '2']:
            Response['reason'] = 2

            return Response

        if type_contact == "1":
            checkEvents = dataTableMysql("SELECT id FROM eventos WHERE tipo_ev = 2 AND codigo = '{}'".format(user_id))

            checkIfEventsGroup = dataTableMysql("SELECT id_evento, estado_invitacion FROM eventos_grupales WHERE id_usuario = '{}'".format(id_contactG))

            haveEvents = False

            for data in checkEvents:
                for data2 in checkIfEventsGroup:
                    if str(data[0]) == str(data2[0]):
                        if str(data2[1]) == "1":
                            haveEvents = True

                            break

            if not haveEvents:
                deleteContactG = dataTableMysql("DELETE FROM contactos WHERE (id_usuario = '{}' AND id_contacto = '{}') OR (id_usuario = '{}' AND id_contacto = '{}')".format(user_id, id_contactG, id_contactG, user_id),"rowcount")
                
                if not deleteContactG:
                    Response['reason'] = 2
                else:
                    Response['deleted'] = True

            else:
                Response['reason'] = 1
        
        return Response

    # Manage actions query friends
    def manageQueryFriendsM(self):
        token = decWithPass(self.info['token'], isJson=True)

        if not token[0]:
            print("TOKEN INVALID")
            pass
        else:
            info_token = token[1]

            if info_token['mode'] == 'invitation_friends':

                if info_token['status'] == "true":
                    changeStatusDB = dataTableMysql("UPDATE contactos SET estado_invitacion = 1 WHERE (id_usuario = '{}') AND (id_contacto = '{}')".format(info_token['user_sender'], info_token['user_sent']), "rowcount")
                elif info_token['status'] == "false":
                    checkEvents = dataTableMysql("SELECT id FROM eventos WHERE tipo_ev = 2 AND codigo = '{}'".format(info_token['user_sender']))

                    checkIfEventsGroup = dataTableMysql("SELECT id_evento, estado_invitacion FROM eventos_grupales WHERE id_usuario = '{}'".format(info_token['user_sent']))

                    haveEvents = False

                    for data in checkEvents:
                        for data2 in checkIfEventsGroup:
                            if str(data[0]) == str(data2[0]):
                                if str(data2[1]) == "1":
                                    haveEvents = True

                                    break

                    if not haveEvents:
                        changeStatusDB = dataTableMysql("UPDATE contactos SET estado_invitacion = 2 WHERE (id_usuario = '{}') AND (id_contacto = '{}')".format(info_token['user_sender'], info_token['user_sent']), "rowcount")
                else:
                    pass




