from re import A
from services.services import *
from services.servicesAsync import *


class Models:
    def login(self):

        Response = {
            "logged": False,
            "token": None,
            "name": None,
            "email": None,
            "user": None,
            "photo": None,
            "number_tel": None,
            "id": None,
        }

        querySQL = ""
        type = self.info["type"]
        id_token = self.info["id_token"] if self.info["id_token"] else None

        if type == "Google" and id_token:
            email = decodeAuth2CertGoogleAPI_GO(id_token)
            if email[0] and email[1]["email_verified"]:
                querySQL = "SELECT id_usuario, nombres, correo, usuario, foto_perfil FROM usuarios WHERE correo = '{}'".format(
                    email[1]["email"])
            else:
                return Response
        elif type == "normal" and not id_token:
            querySQL = "SELECT id_usuario, nombres, correo, usuario, password, foto_perfil, numero FROM usuarios WHERE usuario = '{}'".format(
                self.info["user"])
        else:
            return Response

        dataDB = dataTableMysql(querySQL)

        if dataDB and type == "normal":
            for data in dataDB:
                if decryptStringBcrypt(self.info["password"], data[4]):
                    jwt = encoded_jwt(data[0])
                    Response = {
                        "logged": True,
                        "token": jwt,
                        "name": data[1],
                        "email": data[2],
                        "user": data[3],
                        "photo": data[5],
                        "number_tel": data[6],
                        "id": data[0],
                    }
                    return Response
                else:
                    return Response
        elif dataDB and type == "Google":
            for data in dataDB:
                if email[1]["email"] != data[2][0:len(email[1]["email"])]:
                    return Response

                jwt = encoded_jwt(data[0])

                Response = {
                    "logged": True,
                    "token": jwt,
                    "name": data[1],
                    "email": data[2],
                    "user": "GoogleUser",
                    "photo": data[4],
                    "id": data[0],
                }

                return Response
        else:
            return Response

    def register(self):
        Response = {"registered": False}

        querySQL = ""

        type = self.info["type"]
        id_token = self.info["id_token"] if self.info["id_token"] else None

        if self.info["user"] == "GoogleUser":
            return Response

        if type == "Google" and id_token:
            deAuth2 = decodeAuth2CertGoogleAPI_GO(id_token)
            if deAuth2[0] and deAuth2[1]["email_verified"]:
                hash_password = cryptStringBcrypt(
                    str(getBigRandomString() + getMinRandomString()))

                querySQL = "INSERT INTO usuarios(nombres, correo, usuario, password, foto_perfil) VALUES('{}', '{}', '{}', '{}', '{}')".format(
                    deAuth2[1]["name"],
                    deAuth2[1]["email"],
                    deAuth2[1]["email"] + str(hash_password),
                    hash_password,
                    deAuth2[1]["picture"],
                )
            else:
                return Response
        elif type == "normal" and not id_token:
            hash_password = cryptStringBcrypt(self.info["password"])
            querySQL = "INSERT INTO usuarios(nombres, correo, usuario, password, foto_perfil) VALUES('{}', '{}', '{}', '{}', 'https://www.dropbox.com/s/4nqmlzijvaeqtts/avatar%20-%20profile.jpeg?dl=1')".format(
                self.info["name"], self.info["email"], self.info["user"],
                hash_password)
        else:
            return Response

        data = dataTableMysql(querySQL, "rowcount")

        Response = {"registered": data}

        return Response

    # Manage Events
    def getEvents(self):
        Response = {"auth_token": False, "events": []}

        if not checkJwt(self.info["token"]):
            return Response

        user_id = decode_jwt(self.info["token"]).get("user_id")

        queryUserSQL = "SELECT id_usuario FROM usuarios WHERE id_usuario = '{}'".format(
            user_id)

        dataUserDB = dataTableMysql(queryUserSQL)
        if dataUserDB:
            Response["auth_token"] = True

            dataDB = dataTableMysql(
                "SELECT id, titulo, time_format(hora, '"
                "%h:%i %p"
                "') as hour, CASE WHEN DAY(fecha) <= 9 THEN CONCAT('0', DAY(fecha)) ELSE DAY(fecha) END as DAY, CASE WHEN MONTH(fecha) <= 9 THEN CONCAT('0', MONTH(fecha)) ELSE MONTH(fecha) END as MONTH, YEAR(fecha) as year, descripcion, codigo, tipo_ev, icono FROM eventos WHERE codigo = {} ORDER BY fecha ASC, hora ASC"
                .format(user_id))

            getEventsGroupJoined = dataTableMysql(
                "SELECT e.id, e.titulo, time_format(e.hora, '"
                "%h:%i %p"
                "') as hour, CASE WHEN DAY(e.fecha) <= 9 THEN CONCAT('0', DAY(e.fecha)) ELSE DAY(e.fecha) END as DAY, CASE WHEN MONTH(e.fecha) <= 9 THEN CONCAT('0', MONTH(e.fecha)) ELSE MONTH(e.fecha) END as MONTH, YEAR(e.fecha) as year, e.descripcion, e.codigo, e.tipo_ev, e.icono FROM eventos e, eventos_grupales eg WHERE e.id = eg.id_evento AND id_usuario = '{}' AND eg.estado_invitacion = 1 ORDER BY e.fecha ASC, e.hora ASC"
                .format(user_id))

            for data in dataDB:
                Response["events"].append({
                    "id": data[0],
                    "title": data[1],
                    "hour": data[2],
                    "day": data[3],
                    "month": data[4],
                    "year": data[5],
                    "description": data[6],
                    "check": False,
                    "type_ev": data[8],
                    "icon": data[9],
                    "owner": True,
                })

            for data in getEventsGroupJoined:
                if data not in dataDB:
                    Response["events"].append({
                        "id": data[0],
                        "title": data[1],
                        "hour": data[2],
                        "day": data[3],
                        "month": data[4],
                        "year": data[5],
                        "description": data[6],
                        "check": False,
                        "type_ev": data[8],
                        "icon": data[9],
                        "owner": False,
                    })

        return Response

    def registerEvents(self):
        Response = {"auth_token": False, "saved": False}

        if not checkJwt(self.info["token"]):
            return Response

        user_id = decode_jwt(self.info["token"]).get("user_id")
        print(self.info["hour"])

        dataDB = dataTableMysql(
            "INSERT INTO eventos(titulo, hora, fecha, descripcion, codigo, tipo_ev, icono) VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}')"
            .format(
                self.info["title"],
                self.info["hour"],
                self.info["date"],
                self.info["description"],
                user_id,
                self.info["type_ev"],
                self.info["icon"] if len(self.info["icon"]) >= 1 else "",
            ),
            "rowcount",
        )

        Response = {"auth_token": True, "saved": dataDB}

        return Response

    def changeEvents(self):
        Response = {
            "auth_token": False,
            "saved": False,
            "reason": None,  # 1= find Users in the event
        }

        check_jwt = checkJwt(self.info["token"])

        if not check_jwt:
            return Response

        Response["auth_token"] = True

        id_event = str(self.info["id_event"])

        check_id_event = checkStringNumberSizeType(id_event, len(id_event))

        if not check_id_event:
            return Response

        user_id = decode_jwt(self.info["token"]).get("user_id")

        if str(self.info["type_ev"]) == "1":
            checkIfParticipantsInEvent = dataTableMysql(
                "SELECT id_usuario FROM eventos_grupales WHERE id_evento = '{}'"
                .format(id_event))

            if checkIfParticipantsInEvent:
                for data in checkIfParticipantsInEvent:
                    if str(data[0]) != str(user_id):
                        Response["reason"] = 1
                        return Response

        dataTableMysql(
            "UPDATE eventos SET titulo = '{}', hora = '{}', fecha = '{}', descripcion = '{}', tipo_ev = '{}', icono = '{}' WHERE codigo = '{}' AND id = '{}'"
            .format(
                self.info["title"],
                self.info["hour"],
                self.info["date"],
                self.info["description"],
                self.info["type_ev"],
                self.info["icon"] if len(self.info["icon"]) >= 1 else "",
                user_id,
                id_event,
            ),
            "rowcount",
        )

        Response["saved"] = True

        return Response

    def deleteEvents(self):
        Response = {
            "auth_token": False,
            "deleted": False,
            "reason": None,  # 1: Have users in event
        }

        if not checkJwt(self.info["token"]):
            return Response

        user_id = decode_jwt(self.info["token"]).get("user_id")

        Response["auth_token"] = True

        events = self.info["events"].split(
            ",") if self.info["events"] else None

        for item in events:
            if not checkIfNumberInt(item):
                return Response

        for item in events:
            verifyEventGroupOwner = dataTableMysql(
                "SELECT id FROM eventos_grupales WHERE id_usuario = '{}' AND id_evento = '{}'"
                .format(user_id, item))

            if verifyEventGroupOwner:
                for ver in verifyEventGroupOwner:
                    deleteOwner = dataTableMysql(
                        "DELETE FROM eventos_grupales WHERE id = '{}' AND id_usuario = '{}' "
                        .format(ver[0], user_id),
                        "rowcount",
                    )

            deleteEvent = dataTableMysql(
                "DELETE FROM eventos WHERE id = '{}' and codigo = '{}' ".
                format(item, user_id),
                "rowcount",
            )
            if deleteEvent:
                Response["deleted"] = True
            else:
                Response["reason"] = 1
                Response["deleted"] = False

        return Response

    # Manage participants
    def getParticipantsEvents(self):
        Response = {
            "auth_token": False,
            "participants": [],  # id, photo, name, statusInvitation.
            "reason":
            None,  # 1= id event invalid, 2= not exist event, 3= Event is not group type, 4= Not is invited to event, 5= Waiting response invitation by user, 6=user has refused invitation, 7= not find participants.
        }

        if not checkJwt(self.info["token"]):
            return Response

        Response["auth_token"] = True

        user_id = decode_jwt(self.info["token"]).get("user_id")

        id_event_group = self.info["id_event"] if self.info[
            "id_event"] else None

        if not id_event_group:
            Response["reason"] = 1
            return Response

        if not checkIfNumberInt(id_event_group):
            Response["reason"] = 1
            return Response

        # verify event if type group, exists and owner
        checkEventType = dataTableMysql(
            "SELECT tipo_ev, codigo FROM eventos WHERE id = '{}'".format(
                id_event_group))

        if not checkEventType:
            Response["reason"] = 2
            return Response

        ownerEvent = None

        for data in checkEventType:
            if data[0] == 1:
                Response["reason"] = 3
                return Response

            ownerEvent = data[1]

        checkInvitationStatus = dataTableMysql(
            "SELECT estado_invitacion FROM eventos_grupales WHERE id_usuario = '{}' AND id_evento = '{}'"
            .format(user_id, id_event_group))

        if not checkInvitationStatus:
            if user_id == ownerEvent:
                addOwnerTOEventGroup = dataTableMysql(
                    "INSERT INTO eventos_grupales(id_usuario, id_evento, estado_invitacion) VALUES('{}', '{}', '{}')"
                    .format(user_id, id_event_group, 1),
                    "rowcount",
                )
            else:
                Response["reason"] = 4
                return Response

        for data in checkInvitationStatus:
            if data[0] == 0:
                Response["reason"] = 5
                return Response

            if data[0] == 2:
                Response["reason"] = 6
                return Response

        getParticipantsEvent = dataTableMysql(
            "SELECT u.id_usuario, u.nombres, u.foto_perfil, eg.estado_invitacion FROM usuarios u, eventos_grupales eg WHERE u.id_usuario = eg.id_usuario AND id_evento = '{}'"
            .format(id_event_group))

        if not getParticipantsEvent:
            Response["reason"] = 7
            return Response

        for participant in getParticipantsEvent:
            statusInvitation = None

            if participant[3] == 0:
                statusInvitation = 0

            if participant[3] == 1:
                statusInvitation = 1

            if participant[3] == 2:
                statusInvitation = 2

            if participant[0] == ownerEvent:
                statusInvitation = 3

            Response["participants"].append({
                "id":
                participant[0],
                "name":
                participant[1],
                "photo":
                participant[2],
                "statusInvitation":
                statusInvitation,
            })

        return Response

    def addParticipantsEvents(self):
        Response = {
            "auth_token": False,
            "invited": False,
            "reason":
            None,  # 0= user is some user invited, 1= id event invalid, 2= user invited invalid, 3= user invited not exists, 4= group not exists, 5= user is not owner of event, 6= event type is not group, 7= Not are friends, 8= User invited is joined to group, 9= system error, 10= system error2, 11= system error3, 12= system error4
        }

        if not checkJwt(self.info["token"]):
            return Response

        Response["auth_token"] = True

        user_id = decode_jwt(self.info["token"]).get("user_id")

        id_event_group = self.info["id_event"] if self.info[
            "id_event"] else None

        if not id_event_group:
            Response["reason"] = 1
            return Response

        if not checkIfNumberInt(id_event_group):
            Response["reason"] = 1
            return Response

        # check user invited
        user_invited = self.info["user_invited"] if self.info[
            "user_invited"] else None

        if not user_invited:
            Response["reason"] = 2
            return Response

        if not checkIfNumberInt(user_invited):
            Response["reason"] = 2
            return Response

        if str(user_invited) == str(user_id):
            Response["reason"] = 0
            return Response

        verifyUserInvited = dataTableMysql(
            "SELECT nombres, correo FROM usuarios WHERE id_usuario = '{}'".
            format(user_invited))

        if not verifyUserInvited:
            Response["reason"] = 3
            return Response

        nameGroup = None

        verifyGroupTypeAndExists = dataTableMysql(
            "SELECT tipo_ev, codigo, titulo FROM eventos WHERE id = '{}'".
            format(id_event_group))

        if not verifyGroupTypeAndExists:
            Response["reason"] = 4
            return Response

        for data in verifyGroupTypeAndExists:
            if str(data[1]) != str(user_id):
                Response["reason"] = 5
                return Response

            if str(data[0]) == "1":
                Response["reason"] = 6
                return Response

            nameGroup = data[2]

        verifyIfAreFriends = dataTableMysql(
            "SELECT estado_invitacion FROM contactos WHERE (id_usuario = '{}' OR id_contacto = '{}') AND (id_usuario = '{}' OR id_contacto = '{}')"
            .format(user_invited, user_invited, user_id, user_id))

        if not verifyIfAreFriends:
            Response["reason"] = 7
            return Response

        for data in verifyIfAreFriends:
            if data[0] != 1:
                Response["reason"] = 7
                return Response

        verifyIfNotIsAdded = dataTableMysql(
            "SELECT estado_invitacion, id FROM eventos_grupales WHERE id_usuario = '{}' AND id_evento = '{}'"
            .format(user_invited, id_event_group))

        if verifyIfNotIsAdded:
            for data in verifyIfNotIsAdded:
                if data[0] == 1:
                    Response["reason"] = 8
                    return Response

                updateStatusInvitationRegister = dataTableMysql(
                    "DELETE FROM eventos_grupales WHERE id = '{}'".format(
                        data[1]),
                    "rowcount",
                )

                if not updateStatusInvitationRegister:
                    Response["reason"] = 9
                    return Response

        # send email notification
        receptorEmail = None
        nameUserInvited = None

        for data in verifyUserInvited:
            nameUserInvited = data[0]
            receptorEmail = data[1]

        getInfoUser = dataTableMysql(
            "SELECT nombres, foto_perfil FROM usuarios WHERE id_usuario= '{}'".
            format(user_id))

        if not getInfoUser:
            Response["reason"] = 10
            return Response

        userName = None
        photoUser = None

        for data in getInfoUser:
            userName = data[0]
            photoUser = data[1]

        tokenDecline = tokenAcepte = encWithPass(data=encoded_jwt(
            user_id=user_id,
            data={
                "mode": "invitation_group",
                "user_sent": user_invited,
                "user_sender": user_id,
                "id_group": id_event_group,
                "status": False,
            },
            custom=True,
            Time=30,
        ))

        tokenAcepte = encWithPass(data=encoded_jwt(
            user_id=user_id,
            data={
                "mode": "invitation_group",
                "user_sent": user_invited,
                "user_sender": user_id,
                "id_group": id_event_group,
                "status": True,
            },
            custom=True,
            Time=30,
        ))

        sendEmailNotification = sendEmail(
            receiver=receptorEmail,
            subject="Invitación a grupo",
            userRec={
                "name": nameUserInvited,
                "photo_contact": photoUser,
                "name_contact": userName,
                "group": nameGroup,
                "link_acepte": tokenAcepte[1],
                "link_decline": tokenDecline[1],
            },
            reason="5",
        )

        if not sendEmailNotification:
            Response["reason"] = 11
            return Response

        sendInvitationUsertToGroup = dataTableMysql(
            "INSERT INTO eventos_grupales(id_usuario, id_evento, estado_invitacion) VALUES('{}', '{}', '{}')"
            .format(user_invited, id_event_group, 0),
            "rowcount",
        )

        if not sendInvitationUsertToGroup:
            Response["reason"] = 12
            return Response

        Response["invited"] = True

        return Response

    def joinParticipantsEvents(self):
        token = self.info["token"] if self.info["token"] else None

        if not token:
            return False

        jwtEnc = decWithPass(token)[1]

        JWT = decode_jwt(jwtEnc)

        if not JWT:
            return False

        mode = JWT["data"]["mode"]

        if not mode:
            return False

        if mode != "invitation_group":
            return False

        user_sent = JWT["data"]["user_sent"]
        user_sender = JWT["data"]["user_sender"]
        id_group = JWT["data"]["id_group"]
        status_invitation = JWT["data"]["status"]

        verifyUserSender = dataTableMysql(
            "SELECT id_usuario FROM usuarios WHERE id_usuario = '{}'".format(
                user_sender))

        if not verifyUserSender:
            return False

        verifyUserSent = dataTableMysql(
            "SELECT id_usuario FROM usuarios WHERE id_usuario = '{}'".format(
                user_sent))

        if not verifyUserSent:
            return False

        verifyAreFriends = dataTableMysql(
            "SELECT estado_invitacion FROM contactos WHERE (id_usuario = '{}' OR id_contacto = '{}') AND (id_usuario = '{}' OR id_contacto = '{}')"
            .format(user_sender, user_sender, user_sent, user_sent))

        if not verifyAreFriends:
            return False

        areFriends = False

        for data in verifyAreFriends:
            if str(data[0]) == "1":
                areFriends = True
            else:
                return False

        if status_invitation == True:
            if not areFriends:
                return False

            verifyStatusInvitationGroup = dataTableMysql(
                "SELECT estado_invitacion, id FROM eventos_grupales WHERE id_usuario = '{}' AND id_evento = '{}'"
                .format(user_sent, id_group))

            id_invitation = None

            if verifyStatusInvitationGroup:
                for data2 in verifyStatusInvitationGroup:
                    if str(data2[0]) == "1" or str(data2[0]) == "2":
                        return False

                    id_invitation = data2[1]

                updateStatusInvitationGroup = dataTableMysql(
                    "UPDATE eventos_grupales SET estado_invitacion = 1 WHERE id = '{}'"
                    .format(id_invitation),
                    "rowcount",
                )

                return updateStatusInvitationGroup

            else:
                return False

        else:
            if not areFriends:
                return False

            verifyStatusInvitationGroup = dataTableMysql(
                "SELECT estado_invitacion, id FROM eventos_grupales WHERE id_usuario = '{}' AND id_evento = '{}'"
                .format(user_sent, id_group))

            id_invitation = None

            if verifyStatusInvitationGroup:
                for data2 in verifyStatusInvitationGroup:
                    if str(data2[0]) == "1" or str(data2[0]) == "2":
                        return False

                    id_invitation = data2[1]

                updateStatusInvitationGroup = dataTableMysql(
                    "UPDATE eventos_grupales SET estado_invitacion = 2 WHERE id = '{}'"
                    .format(id_invitation),
                    "rowcount",
                )

                return updateStatusInvitationGroup

            else:
                return False

    def deleteParticipants(self):
        Response = {
            "auth_token": False,
            "deleted": False,
            "reason":
            None,  # 1= group_id Invalid, 2= user delete is Invalid, 3= some user id and user delete, 4= User delete is not exists, 5= group is not exists, 6= Group is not owner, 7= Group is not type event_group, 8= user delete is not joined to group, 9= System error 1
        }

        if not checkJwt(self.info["token"]):
            return Response

        Response["auth_token"] = True

        user_id = decode_jwt(self.info["token"]).get("user_id")

        id_event_group = self.info["id_event"] if self.info[
            "id_event"] else None

        if not id_event_group:
            Response["reason"] = 1
            return Response

        if not checkIfNumberInt(id_event_group):
            Response["reason"] = 1
            return Response

        # check user invited
        user_delete = self.info["user_delete"] if self.info[
            "user_delete"] else None

        if not user_delete:
            Response["reason"] = 2
            return Response

        if not checkIfNumberInt(user_delete):
            Response["reason"] = 2
            return Response

        if str(user_delete) == str(user_id):
            Response["reason"] = 3
            return Response

        verifyUserDelete = dataTableMysql(
            "SELECT id_usuario FROM usuarios WHERE id_usuario = '{}'".format(
                user_delete))

        if not verifyUserDelete:
            Response["reason"] = 4
            return Response

        verifyGroup = dataTableMysql(
            "SELECT codigo, tipo_ev FROM eventos WHERE id = '{}'".format(
                id_event_group))

        if not verifyGroup:
            Response["reason"] = 5
            return Response

        for data in verifyGroup:
            if str(data[0]) != str(user_id):
                Response["reason"] = 6
                return Response

            if str(data[1]) == "1":
                Response["reason"] = 7
                return Response

        verifyIfJoinedUserDelete = dataTableMysql(
            "SELECT id FROM eventos_grupales WHERE id_usuario = '{}' AND id_evento = '{}'"
            .format(user_delete, id_event_group))

        if not verifyIfJoinedUserDelete:
            Response["reason"] = 8
            return Response

        id_event_register = None

        for data in verifyIfJoinedUserDelete:
            id_event_register = data[0]

        deleteUserToGroup = dataTableMysql(
            "DELETE FROM eventos_grupales WHERE id = '{}'".format(
                id_event_register),
            "rowcount",
        )

        if not deleteUserToGroup:
            Response["reason"] = 9
            return Response
        else:
            Response["deleted"] = True

        return Response

    def exitParticipantEvents(self):
        Response = {
            "auth_token": False,
            "left": False,
            "reason":
            None,  # 1= group is invalid, 2= Group is not exists, 3= Group is type invalid, 4= User is not joined to event, 5= System error 1
        }

        if not checkJwt(self.info["token"]):
            return Response

        Response["auth_token"] = True

        user_id = decode_jwt(self.info["token"]).get("user_id")

        id_event_group = self.info["id_event"] if self.info[
            "id_event"] else None

        if not id_event_group:
            Response["reason"] = 1
            return Response

        if not checkIfNumberInt(id_event_group):
            Response["reason"] = 1
            return Response

        verifyEventGroup = dataTableMysql(
            "SELECT tipo_ev FROM eventos WHERE id = '{}'".format(
                id_event_group))

        if not verifyEventGroup:
            Response["reason"] = 2
            return Response

        for data in verifyEventGroup:
            if str(data[0]) != "2":
                Response["reason"] = 3
                return Response

        id_register_event = None

        verifyIfJoinedEvent = dataTableMysql(
            "SELECT id FROM eventos_grupales WHERE id_usuario = '{}' AND id_evento = '{}'"
            .format(user_id, id_event_group))

        if not verifyIfJoinedEvent:
            Response["reason"] = 4
            return Response

        for data in verifyIfJoinedEvent:
            id_register_event = data[0]

        leftUserEvent = dataTableMysql(
            "DELETE FROM eventos_grupales WHERE id = '{}'".format(
                id_register_event),
            "rowcount",
        )

        if not leftUserEvent:
            Response["reason"] = 5
            return Response
        else:
            Response["left"] = True

        return Response

    # Recovery Account
    def recoveryAccount(self):
        Response = {"recovering": False, "token": None}
        querySQL = ""

        type = self.info["type"] if self.info["type"] else None
        account = self.info["account"] if self.info["account"] else None

        if type == "number" and account:
            if not checkStringNumberTel(account):
                return Response
            else:
                querySQL = "SELECT id_usuario, numero, correo, nombres, usuario FROM usuarios WHERE numero = '{}'".format(
                    account[2::])
        elif type == "email" and account:
            if not checkStringEmail(account):
                return Response
            else:
                querySQL = "SELECT id_usuario, correo, nombres, usuario FROM usuarios WHERE correo = '{}';".format(
                    account)
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
                    rootAsync = sendEmailAndSMSThreading(
                        info={
                            "S-Email": {
                                "subject": "Reestablecer contraseña",
                                "receiver": data[2],
                                "userRec": {
                                    "name": data[3]
                                },
                                "reason": "2",
                            },
                            "S-SMS": {
                                "number": account,
                                "msg": "Calenbell+code+" + codeRandom,
                            },
                        })

                    sendAlerts = rootAsync.run()

                    if sendAlerts:
                        verifyCodeEnc = encWithPass("{'account': '" + account +
                                                    "', 'code': '" +
                                                    codeRandom + "'}")

                        Response["recovering"] = True

                        Response["token"] = createJwt(
                            info={"verify": verifyCodeEnc[1]}, time=5)
                elif type == "email":
                    if account == data[3][0:len(account)]:
                        return Response

                    codeRandom = createRandomNumberSize(6)

                    sendByEmail = sendEmail(
                        receiver=data[1],
                        subject="Reestablecer contraseña",
                        userRec={
                            "name": data[2],
                            "code": codeRandom
                        },
                        reason="3",
                    )

                    if sendByEmail:
                        verifyCodeEnc = encWithPass("{'account': '" + account +
                                                    "', 'code': '" +
                                                    codeRandom + "'}")
                        Response["recovering"] = True
                        Response["token"] = createJwt(
                            info={"verify": verifyCodeEnc[1]}, time=5)
                else:
                    return Response

        return Response

    def validateCodeRecoveryAccount(self):
        token = decode_jwt(self.info["token"])
        Enc = token.get("info")["verify"]
        accountToken = decWithPass(dataEnc=Enc, isJson=True)[1]["account"]
        codeToken = decWithPass(dataEnc=Enc, isJson=True)[1]["code"]

        # validate code token and account

        codeValidate = checkStringNumberSizeType(number=self.info["code"],
                                                 size=6)
        codeTokenValidate = checkStringNumberSizeType(number=codeToken, size=6)

        accountDetector = checkStringNumberSizeType(number=accountToken,
                                                    size=12)

        querySQL = ""
        Response = {"recovered": False, "token": None}

        if codeValidate and token and codeTokenValidate:
            if self.info["code"] != codeToken:
                return Response

            if accountDetector:
                # type number
                querySQL = "SELECT numero FROM usuarios WHERE numero = '{}'".format(
                    accountToken[2:12])
            else:
                # type email
                querySQL = "SELECT correo FROM usuarios WHERE correo = '{}'".format(
                    accountToken)
        else:
            return Response

        dataDB = dataTableMysql(querySQL)

        if dataDB:
            Response["recovered"] = True
            Response["token"] = createJwt(info={
                "verify": Enc,
                "recovered": True
            },
                                          time=5)

        return Response

    def validateChangePwd(self):
        token = decode_jwt(self.info["token"])

        Enc = token.get("info")["verify"]

        accountRecovered = token.get("info")["recovered"]

        accountToken = decWithPass(dataEnc=Enc, isJson=True)[1]["account"]

        accountDetector = checkStringNumberSizeType(number=accountToken,
                                                    size=12)

        passwordForChange = self.info["pwd"] if self.info["pwd"] else None

        querySQL = ""
        querySQLChangePWD = ""

        Response = {"recovered": False}

        if token and accountRecovered and accountToken and Enc and passwordForChange:
            if accountDetector:
                # number
                querySQL = "SELECT numero FROM usuarios WHERE numero = '{}'".format(
                    accountToken[2:12])
            else:
                # email
                querySQL = "SELECT correo FROM usuarios WHERE correo = '{}'".format(
                    accountToken)
        else:
            return Response

        dataDB = dataTableMysql(querySQL)

        if dataDB:

            hash_password = cryptStringBcrypt(passwordForChange)

            if accountDetector:
                # number
                querySQLChangePWD = (
                    "UPDATE usuarios SET password = '{}' WHERE numero = '{}'".
                    format(hash_password, accountToken[2:12]))
            else:
                # email
                querySQLChangePWD = (
                    "UPDATE usuarios SET password = '{}' WHERE correo = '{}'".
                    format(hash_password, accountToken))

        dataDBC = dataTableMysql(querySQLChangePWD, "rowcount")

        if dataDBC and querySQLChangePWD:
            Response["recovered"] = True

        return Response

    # Chat
    def initChatM(self):
        Response = {
            "auth_token": False,
            "token": None,
            "invitation_status": None
        }

        Payload = {
            "friends": None,
            "in_group": None,
            "type_chat": None,
            "receiver": None,
            "transmitter": None,
            "invitation_status": None,
        }

        token = decode_jwt(self.info["token"] if self.info["token"] else None)

        if not token:
            return Response

        user_id = token.get("user_id")

        if not checkIfNumberInt(user_id):
            return Response

        Response["auth_token"] = True

        type_chat = str(
            self.info["chat_type"]) if self.info["chat_type"] else None

        if len(type_chat) != 1:
            return Response

        if type_chat not in ["1", "2"]:
            return Response

        Payload["type_chat"] = type_chat

        if type_chat == "1":
            id_emisor = user_id

            if not checkIfNumberInt(id_emisor):
                return Response

            Payload["transmitter"] = id_emisor

            id_receptor = self.info["receiver"] if self.info[
                "receiver"] else None

            if not checkIfNumberInt(id_receptor):
                return Response

            if id_emisor == id_receptor:
                return Response

            Payload["receiver"] = id_receptor

            resultado_init = initChat(id_emisor=id_emisor,
                                      id_receptor=id_receptor,
                                      typeChat=type_chat)

            if not resultado_init["existen_usuarios"]:
                return Response

            Payload["invitation_status"] = resultado_init["estado_invitacion"]

            Payload["friends"] = resultado_init["son_amigos"]

            token_val_socket = encoded_jwt(
                user_id=user_id,
                data={
                    "friends": Payload["friends"],
                    "transmitter": Payload["transmitter"],
                    "receiver": Payload["receiver"],
                },
                custom=True,
            )

            Response["token"] = token_val_socket if token_val_socket else None

            Response["invitation_status"] = Payload["invitation_status"]

            return Response

        else:
            id_grupo = self.info["group"] if self.info["group"] else None

            if not checkIfNumberInt(id_grupo):
                return Response

            id_emisor = user_id

            if not checkIfNumberInt(id_emisor):
                return Response

            Payload["transmitter"] = id_emisor

            resultado_init = initChat(id_emisor=id_emisor,
                                      id_evento_grupal=id_grupo,
                                      typeChat=type_chat)

            if resultado_init["existe_grupo"] == False:
                return Response

            Payload["invitation_status"] = resultado_init["estado_invitacion"]

            Payload["in_group"] = resultado_init["pertenece_grupo"]

            token_val_socket = encoded_jwt(
                user_id=user_id,
                data={
                    "in_group": Payload["in_group"],
                    "id_group": id_grupo
                },
                custom=True,
            )

            Response["token"] = token_val_socket if token_val_socket else None

            Response["invitation_status"] = Payload["invitation_status"]

            return Response

        return Response

    # Manage contacts and groups
    def getContactsG(self):
        Response = {
            "auth_token": False,
            "contacts": [],  # dictionary = type, name, id, photo
        }

        if not checkJwt(self.info["token"]):
            return Response

        Response["auth_token"] = True

        user_id = decode_jwt(self.info["token"]).get("user_id")

        fetchContacts = dataTableMysql(
            "SELECT c.id_usuario, c.id_contacto, IF(u.id_usuario = '{}', NULL, u.nombres) AS nombre_usuario, IF(u1.id_usuario = '{}', NULL, u1.nombres) AS nombre_contacto, IF(u.id_usuario = '{}', NULL, u.foto_perfil) as foto_perfil_usuario, IF(u1.id_usuario = '{}', NULL, u1.foto_perfil) as foto_perfil_contacto FROM usuarios u INNER JOIN contactos c ON u.id_usuario=c.id_usuario INNER JOIN usuarios u1 ON u1.id_usuario=c.id_contacto WHERE (u.id_usuario = '{}' OR u1.id_usuario = '{}') AND c.estado_invitacion = 1;"
            .format(user_id, user_id, user_id, user_id, user_id, user_id))

        if not fetchContacts:
            return Response

        for contact in fetchContacts:
            if str(contact[0]) != str(user_id) and str(
                    contact[1]) == str(user_id):
                Response["contacts"].append({
                    "type": 1,
                    "name": contact[2],
                    "id": contact[0],
                    "photo": contact[4],
                })

            if str(contact[0]) == str(user_id) and str(
                    contact[1]) != str(user_id):
                Response["contacts"].append({
                    "type": 1,
                    "name": contact[3],
                    "id": contact[1],
                    "photo": contact[5],
                })

        fetchGroups = dataTableMysql(
            "SELECT eg.id, eg.id_evento, e.titulo, e.icono from eventos_grupales eg, eventos e WHERE eg.id_evento = e.id and id_usuario = '{}' AND eg.estado_invitacion = 1"
            .format(user_id))

        if not fetchContacts:
            return Response

        for group in fetchGroups:
            Response["contacts"].append({
                "type": 2,
                "name": group[2],
                "id": group[1],
                "photo": group[3]
            })

        return Response

    def searchContacts(self):
        Response = {"auth_token": False, "users": []}  # id, name, photo

        if not checkJwt(self.info["token"]):
            return Response

        Response["auth_token"] = True

        user_id = decode_jwt(self.info["token"]).get("user_id")

        search_key = self.info["search_key"].strip()

        if len(search_key) == 0:
            return Response

        getUsers = dataTableMysql(
            "SELECT id_usuario, nombres, foto_perfil from usuarios WHERE id_usuario != '{}' and nombres like '%{}%'"
            .format(user_id, search_key))

        for user in getUsers:
            Response["users"].append({
                "id": user[0],
                "name": user[1],
                "photo": user[2]
            })

        return Response

    def addContacts(self):
        Response = {
            "auth_token": False,
            "send": False,
            "reason": None,  # Optional: 1 = are friends, 2 = some
        }

        if not checkJwt(self.info["token"]):
            return Response

        Response["auth_token"] = True

        user_id = decode_jwt(self.info["token"]).get("user_id")

        if not checkIfNumberInt(self.info["user_add"]):
            return Response

        user_add = self.info["user_add"]

        if user_id == user_add:
            Response["reason"] = 2

            return Response

        checkListFriends = dataTableMysql(
            "SELECT * FROM contactos WHERE (id_usuario = '{}' OR id_contacto = '{}')"
            .format(user_id, user_id))

        for data in checkListFriends:
            if str(data[0]) == str(user_id) and str(data[1]) == str(user_add):
                if str(data[2]) == "1":  # are friends?
                    Response["reason"] = 1

                    return Response

                if str(data[2]) != "1":
                    deleteForFix = dataTableMysql(
                        "DELETE FROM contactos WHERE (id_usuario = '{}') AND (id_contacto = '{}')"
                        .format(user_id, user_add))
                    break

            if str(data[1]) == str(user_id) and str(data[0]) == str(user_add):
                if str(data[2]) == "1":  # are friends?
                    Response["reason"] = 1

                    return Response

                if str(data[2]) == "0":
                    deleteForFix = dataTableMysql(
                        "DELETE FROM contactos WHERE (id_usuario = '{}') AND (id_contacto = '{}')"
                        .format(user_add, user_id))
                    break

        addUserToFriendsList = dataTableMysql(
            "INSERT INTO contactos VALUES('{}', '{}', '{}')".format(
                user_id, user_add, 0),
            "rowcount",
        )

        if addUserToFriendsList:
            name_get_user = ""
            photo_contact = ""

            name_user_id = dataTableMysql(
                "SELECT nombres, foto_perfil FROM usuarios WHERE id_usuario = '{}'"
                .format(user_id))

            for data in name_user_id:
                name_get_user = data[0]
                photo_contact = data[1]

            info_contact = dataTableMysql(
                "SELECT nombres, correo FROM usuarios WHERE id_usuario = '{}'".
                format(user_add))

            for data in info_contact:
                Token_Invitation_acepted = encWithPass(
                    data="{'mode': 'invitation_friends', 'user_sent': '" +
                    str(user_add) + "', 'user_sender': '" + str(user_id) +
                    "', 'status': 'true'}")

                Token_Invitation_decline = encWithPass(
                    data="{'mode': 'invitation_friends', 'user_sent': '" +
                    str(user_add) + "', 'user_sender': '" + str(user_id) +
                    "', 'status': 'false'}")

                send_invitation = sendEmail(
                    receiver=data[1],
                    subject="Solicitud de amistad",
                    userRec={
                        "name": data[0],
                        "photo_contact": photo_contact,
                        "name_contact": name_get_user,
                        "link_decline": Token_Invitation_decline[1],
                        "link_acepte": Token_Invitation_acepted[1],
                    },
                    reason="4",
                )

                if send_invitation:
                    Response["send"] = True

        return Response

    def deleteContacts(self):
        Response = {
            "auth_token": False,
            "deleted": False,
            "reason": None,  # 1 = Joined event group, 2 = invalid payload
        }

        if not checkJwt(self.info["token"]):
            return Response

        Response["auth_token"] = True

        user_id = decode_jwt(self.info["token"]).get("user_id")

        payload = self.info["payload"].split(
            ",") if self.info["payload"] else None

        if payload == None:
            Response["reason"] = 2

            return Response

        id_contactG = payload[0]

        if not checkIfNumberInt(id_contactG):
            Response["reason"] = 2

            return Response

        type_contact = payload[1]

        if len(type_contact) != 1 and type_contact not in ["1", "2"]:
            Response["reason"] = 2

            return Response

        if type_contact == "1":
            checkEvents = dataTableMysql(
                "SELECT id FROM eventos WHERE tipo_ev = 2 AND codigo = '{}'".
                format(user_id))

            checkIfEventsGroup = dataTableMysql(
                "SELECT id_evento, estado_invitacion FROM eventos_grupales WHERE id_usuario = '{}'"
                .format(id_contactG))

            haveEvents = False

            for data in checkEvents:
                for data2 in checkIfEventsGroup:
                    if str(data[0]) == str(data2[0]):
                        if str(data2[1]) == "1":
                            haveEvents = True

                            break

            if not haveEvents:
                deleteContactG = dataTableMysql(
                    "DELETE FROM contactos WHERE (id_usuario = '{}' AND id_contacto = '{}') OR (id_usuario = '{}' AND id_contacto = '{}')"
                    .format(user_id, id_contactG, id_contactG, user_id),
                    "rowcount",
                )

                if not deleteContactG:
                    Response["reason"] = 2
                else:
                    Response["deleted"] = True

            else:
                Response["reason"] = 1

        return Response

    # Manage actions query friends
    def manageQueryFriendsM(self):
        token = decWithPass(self.info["token"], isJson=True)

        if not token[0]:
            print("TOKEN INVALID")
            pass
        else:
            info_token = token[1]

            if info_token["mode"] == "invitation_friends":

                if info_token["status"] == "true":
                    changeStatusDB = dataTableMysql(
                        "UPDATE contactos SET estado_invitacion = 1 WHERE (id_usuario = '{}') AND (id_contacto = '{}')"
                        .format(info_token["user_sender"],
                                info_token["user_sent"]),
                        "rowcount",
                    )
                elif info_token["status"] == "false":
                    checkEvents = dataTableMysql(
                        "SELECT id FROM eventos WHERE tipo_ev = 2 AND codigo = '{}'"
                        .format(info_token["user_sender"]))

                    checkIfEventsGroup = dataTableMysql(
                        "SELECT id_evento, estado_invitacion FROM eventos_grupales WHERE id_usuario = '{}'"
                        .format(info_token["user_sent"]))

                    haveEvents = False

                    for data in checkEvents:
                        for data2 in checkIfEventsGroup:
                            if str(data[0]) == str(data2[0]):
                                if str(data2[1]) == "1":
                                    haveEvents = True

                                    break

                    if not haveEvents:
                        changeStatusDB = dataTableMysql(
                            "UPDATE contactos SET estado_invitacion = 2 WHERE (id_usuario = '{}') AND (id_contacto = '{}')"
                            .format(info_token["user_sender"],
                                    info_token["user_sent"]),
                            "rowcount",
                        )
                else:
                    pass

    # Settings Profile user
    def settingsUser(self):
        Response = {
            "auth_token": False,
            "changed": False,
            "reason":
            None,  # 1= action invalid, 2= area invalid, 3= Resource invalid, 4= action invalid for name, 5= action invalid for username, 6= action invalid for email, 7= action invalid for tel, 8= action invalid for password, 9= Error save img to system, 10= Error save img to cloud, 11= User Is invalid (bug), 12= Error update new img in DB, 13= Name is invalid, 14= Error updating name in DB, 16= Name is same, 17= username is invalid, 18 = Error change username (user is invalid), 19= user is GoogleUser, 20 = Error updating username in DB, 15= Username is same, 21= Email is invalid, 22= Error updating email (user is invalid), 24= Email is same, 25= Error updating email in DB, 26= Number tel is invalid, 27= action invalid for img, 28= Error updating number tel (user is invalid), 29= Error updating number tel in DB, 30= Number tel is same, 31= Number Tel is of other user, 32= Username is of other user, 33= Email is of other user, 34= Error updating password (user is invalid), 35= Password is invalid, 36= Error updating password in DB, 23=
        }

        if not checkJwt(self.info["token"]):
            return Response

        Response["auth_token"] = True

        user_id = decode_jwt(self.info["token"]).get("user_id")

        action = self.info["action"] if self.info["action"] else None

        if not action:
            Response["reason"] = 1
            return Response

        if action not in ["update", "delete"]:
            Response["reason"] = 1
            return Response

        area = self.info["area"] if self.info["area"] else None

        if not area:
            Response["reason"] = 2
            return Response

        if area not in ["img", "name", "username", "email", "tel", "password"]:
            Response["reason"] = 2
            return Response

        resource = self.info["resource"] if self.info["resource"] else None

        if not resource:
            Response["reason"] = 3
            return Response

        # validate if area is img
        if area == "img":
            if action == "update":

                image = saveImg(data=resource, route="")

                if not image[0]:
                    Response["reason"] = 9
                    return Response

                savedCloud = saveFileCloudDpBx(image[1],
                                               routeCloud="/profiles/")

                if not savedCloud[0]:
                    Response["reason"] = 10
                    return Response

                getCurrentImg = dataTableMysql(
                    "SELECT foto_perfil FROM usuarios WHERE id_usuario = '{}'".
                    format(user_id))

                if not getCurrentImg:
                    Response["reason"] = 11
                    return Response

                CurrentImgDB = ""

                for data in getCurrentImg:
                    for data2 in data[0][::-1]:

                        if data2 == "/":
                            break

                        CurrentImgDB += data2

                CurrentImgDB = CurrentImgDB[::-1].replace("?dl=1", "")

                # Delete current img in cloud
                delFileCloudDpBx(routeCloud="/profiles/",
                                 nameFileCloud=CurrentImgDB)

                updateImgInDB = dataTableMysql(
                    "UPDATE usuarios SET foto_perfil = '{}' WHERE id_usuario = '{}'"
                    .format(savedCloud[1], user_id),
                    rtn="rowcount",
                )

                if not updateImgInDB:
                    Response["reason"] = 12
                    return Response

                Response["changed"] = True

            if action == 'delete':
                getCurrentImg = dataTableMysql(
                    "SELECT foto_perfil FROM usuarios WHERE id_usuario = '{}'".
                    format(user_id))

                if not getCurrentImg:
                    Response["reason"] = 11
                    return Response

                CurrentImgDB = ""

                for data in getCurrentImg:
                    for data2 in data[0][::-1]:

                        if data2 == "/":
                            break

                        CurrentImgDB += data2

                CurrentImgDB = CurrentImgDB[::-1].replace("?dl=1", "")

                # Delete current img in cloud
                delFileCloudDpBx(routeCloud="/profiles/",
                                 nameFileCloud=CurrentImgDB)

                updateImgInDB = dataTableMysql(
                    "UPDATE usuarios SET foto_perfil = 'https://www.dropbox.com/s/4nqmlzijvaeqtts/avatar%20-%20profile.jpeg?dl=1' WHERE id_usuario = '{}'"
                    .format(user_id),
                    rtn="rowcount",
                )

                Response["changed"] = True

            if action != 'update' or action != 'delete':
                Response["reason"] = 27
                return Response

        # validate if area is name
        if area == "name":
            if action != "update":
                Response["reason"] = 4
                return Response

            if len(resource) < 3 or len(resource) > 30:
                Response["reason"] = 13
                return Response

            checkIfNumbers = findNumbersInString(resource)

            if checkIfNumbers:
                Response["reason"] = 13
                return Response

            resource = fixStringClient(resource)

            updateNameInDB = dataTableMysql(
                "UPDATE usuarios SET nombres = '{}' WHERE id_usuario = '{}'".
                format(resource, user_id), "rowcount")

            if not updateNameInDB:

                reviseIfNameSame = dataTableMysql(
                    "SELECT nombres FROM usuarios WHERE id_usuario = '{}' AND nombres = '{}'"
                    .format(user_id, resource))

                if reviseIfNameSame:
                    Response["reason"] = 16
                    return Response

                Response["reason"] = 14
                return Response

            Response["changed"] = True

        # validate if area is username
        if area == "username":
            if action != "update":
                Response["reason"] = 5
                return Response

            reviseIfNotIsGoogleUser = dataTableMysql(
                "SELECT correo, usuario FROM usuarios WHERE id_usuario = '{}'".
                format(user_id))

            if not reviseIfNotIsGoogleUser:
                Response["reason"] = 18
                return Response

            for data in reviseIfNotIsGoogleUser:
                if str(data[0]) == str(data[1][0:len(data[0])]):
                    Response["reason"] = 19
                    return Response

            if len(resource) < 4 or len(resource) > 40:
                Response["reason"] = 17
                return Response

            resource = fixStringClient(resource)

            updateUsernameInDB = dataTableMysql(
                "UPDATE usuarios SET usuario = '{}' WHERE id_usuario = '{}'".
                format(resource, user_id), "rowcount")

            if not updateUsernameInDB:
                reviseIfUsernameIsOtherUser = dataTableMysql(
                    "SELECT id_usuario FROM usuarios WHERE id_usuario != '{}' AND usuario = '{}'"
                    .format(user_id, resource))

                if reviseIfUsernameIsOtherUser:
                    Response["reason"] = 32
                    return Response

                reviseIfUsernameSame = dataTableMysql(
                    "SELECT id_usuario FROM usuarios WHERE id_usuario = '{}' AND usuario = '{}'"
                    .format(user_id, resource))

                if reviseIfUsernameSame:
                    Response["reason"] = 15
                    return Response

                Response["reason"] = 20
                return Response

            Response["changed"] = True

        # validate if area is email
        if area == "email":
            if action != "update":
                Response["reason"] = 6
                return Response

            reviseIfNotIsGoogleUser = dataTableMysql(
                "SELECT correo, usuario FROM usuarios WHERE id_usuario = '{}'".
                format(user_id))

            if not reviseIfNotIsGoogleUser:
                Response["reason"] = 22
                return Response

            for data in reviseIfNotIsGoogleUser:
                if str(data[0]) == str(data[1][0:len(data[0])]):
                    Response["reason"] = 19
                    return Response

            if len(resource) > 255:
                Response["reason"] = 21
                return Response

            checkIfResourceIsAEmail = checkStringEmail(resource)

            if not checkIfResourceIsAEmail:
                Response["reason"] = 21
                return Response

            updateEmailInDB = dataTableMysql(
                "UPDATE usuarios SET correo = '{}' WHERE id_usuario = '{}'".
                format(resource, user_id), "rowcount")

            if not updateEmailInDB:
                reviseIfEmailisOtherUser = dataTableMysql(
                    "SELECT id_usuario FROM usuarios WHERE id_usuario != '{}' AND correo = '{}'"
                    .format(user_id, resource))

                if reviseIfEmailisOtherUser:
                    Response["reason"] = 33
                    return Response

                reviseIfEmailSame = dataTableMysql(
                    "SELECT id_usuario FROM usuarios WHERE id_usuario = '{}' AND correo = '{}'"
                    .format(user_id, resource))

                if reviseIfEmailSame:
                    Response["reason"] = 24
                    return Response

                Response["reason"] = 25
                return Response

            Response["changed"] = True

        # validate if area is tel
        if area == "tel":
            if action == "update":

                checkIfResourceIsANumberTel = checkStringNumberSizeType(
                    number=resource, size=10)

                if not checkIfResourceIsANumberTel:
                    Response["reason"] = 26
                    return Response

                updateNumberTelinDB = dataTableMysql(
                    "UPDATE usuarios SET numero = '{}' WHERE id_usuario = '{}'"
                    .format(resource, user_id), "rowcount")

                if not updateNumberTelinDB:
                    reviseIfExitsNumberTelinDB = dataTableMysql(
                        "SELECT id_usuario FROM usuarios WHERE numero = '{}' AND id_usuario != '{}'"
                        .format(resource, user_id))

                    if reviseIfExitsNumberTelinDB:
                        Response["reason"] = 31
                        return Response

                    reviseIfResourceIsSame = dataTableMysql(
                        "SELECT id_usuario FROM usuarios WHERE id_usuario = '{}' AND numero = '{}'"
                        .format(user_id, resource))

                    if not reviseIfResourceIsSame:
                        Response["reason"] = 28
                        return Response

                    if reviseIfResourceIsSame:
                        Response["reason"] = 30
                        return Response

                    Response["reason"] = 29
                    return Response

                Response["changed"] = True

            if action != 'update':
                Response["reason"] = 7
                return Response

        # validate if area is password
        if area == "password":
            if action != "update":
                Response["reason"] = 8
                return Response

            reviseIfNotIsGoogleUser = dataTableMysql(
                "SELECT correo, usuario FROM usuarios WHERE id_usuario = '{}'".
                format(user_id))

            if not reviseIfNotIsGoogleUser:
                Response["reason"] = 34
                return Response

            for data in reviseIfNotIsGoogleUser:
                if str(data[0]) == str(data[1][0:len(data[0])]):
                    Response["reason"] = 19
                    return Response

            resource = fixStringClient(resource)

            if len(resource) < 6 or len(resource) > 255:
                Response["reason"] = 35
                return Response

            hash_password = cryptStringBcrypt(resource)

            updatePwdInDB = dataTableMysql(
                "UPDATE usuarios SET password = '{}' WHERE id_usuario = '{}'".
                format(hash_password, user_id), "rowcount")

            if not updatePwdInDB:
                Response["reason"] = 36
                return Response

            Response["changed"] = True

        return Response
