import os
import random
import jwt
import base64
import time
import mysql.connector
import datetime
import bcrypt
import smtplib
import re
import requests
from pkcs7 import *
from Crypto import Random
from Crypto.Cipher import AES
from Crypto import Random 
from config.config import *
from io import BytesIO
from PIL import Image
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from utils.utilTemplate import UTemplates
from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

# KEYS

bytesRandomGlobal = os.urandom(16)

def fixStringClient(string):
    try:
        if string == True or string == False:
            return string
    
        if string == None:
            print("meg from fixStringClient: ")
            print("string is NoneType")
            return False

        fixed = str(string).replace("'", "").replace("*", "").replace('"', "").replace("+", "").replace("|", "").replace("%", "").replace("$", "").replace("&", "").replace("=", "").replace("?", "").replace('¡', "").replace("\a", "").replace("<", "").replace(">", "").replace("/", "").replace("[", "").replace("]", "").replace("(", "").replace(")", "").replace("´", "").replace("!", "").replace("\n", "")
        return fixed
    except Exception as e:
        print("ERROR IN fixStringClient:")
        print(e)
        return False

def checkJwt(token):
    try:
        data = jwt.decode(token, KEY_TOKEN_AUTH , algorithms=['HS256'])
        return True
    except:
        return False

def dataTableMysql(query, rtn="datatable"):
    try:
        mydb = mysql.connector.connect(host=MYSQL_HOST,user=MYSQL_USER,password=MYSQL_PASSWORD,database=MYSQL_DB)
        #print("OP 1")
        mycursor = mydb.cursor()
        #print("OP 2")
        #print(query)
        mycursor.execute(query)
        #print("OP 3")
        data = mycursor.fetchall()
        #print("OP 4")
        mydb.commit()
        #print("OP 5")
        
        if rtn == "datatable":
            mycursor.close()
            return data
        elif rtn == "rowcount":
            #print(mycursor.rowcount)
            if mycursor.rowcount >= 1:
                mycursor.close()
                return True
            else:
                mycursor.close()
                return False
        else:
            mycursor.close()
            return data
    except Exception as e:
        print("ERROR in dataTableMysql:")
        print(e)
        return False

def encoded_jwt(user_id, data = None, custom = False):
    try:
        if not custom:
            return jwt.encode({'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=1440), 'user_id': user_id}, KEY_TOKEN_AUTH , algorithm='HS256')
        else:
            return jwt.encode({'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=1440), 'user_id': user_id, 'data': data}, KEY_TOKEN_AUTH , algorithm='HS256')
    except Exception as e:
        print("ERROR IN encoded_jwt:")
        print(e)
        return False

def cryptStringBcrypt(string, rtn="string"):
    s = random.randint(5,10)
    salt = bcrypt.gensalt(s)
    hashed = bcrypt.hashpw(bytes(str(string), encoding= 'utf-8'), salt)
    if rtn == "string":
        return hashed.decode("utf-8")
    elif rtn == "byte":
        return hashed
    else:
        return hashed.decode("utf-8")

def decryptStringBcrypt(EncValidate, EncCompare):
    return bcrypt.checkpw(bytes(str(EncValidate), encoding= 'utf-8'), bytes(str(EncCompare), encoding= 'utf-8'))

def getBigRandomString():
    return str(random.randint(random.randint(round(time.time() + 2), round(time.time()) + round(time.time() + 8)), round(time.time() - 3)*round(time.time())+1))

def getMinRandomString():
    try:
        rand1 = random.randint(int(str(round(time.time()))[::-5][::2]),int(str(round(time.time()))[::-5][::2]))
        rand2 = random.randint(int(str(round(time.time()))[::-5][::2]),int(str(round(time.time()))[::-5][::2]))
        return str(random.randint(rand1, rand2+10))
    except :
        return str(random.randint(6, 15))

def cryptBase64(string):
    try:
        m_byte = string.encode('ascii')
        b64_b = base64.b64encode(m_byte)
        return b64_b.decode('ascii')
    except :
        return False

def decryptBase64(b_64):
    try:
        b64_b = b_64.encode('ascii')
        m_b = base64.b64decode(b64_b)
        return m_b.decode('ascii')
    except :
        return False

def CryptData(text, custom="none"):
    """
    master_key: random string based on string {crypt}

    CryptData( String = string to encrypt , String = custom_master_key -- or empty to default )

    return Array[] = [ encrypted string, master_key ]
    """
    try:
        crypt = ''
        if custom != "none" and custom != "random":
            crypt = custom
        elif custom == "random":
            sizeC = len('abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMOPQRSTUVWXYZ+/= :}{')
            crypt = random.sample('abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMOPQRSTUVWXYZ+/= :}{', sizeC)
            cryptJoin = ''.join(crypt)
            bcryptR = random.sample(cryptJoin, len(cryptJoin))
            #print(len(bcrypt))
            b_end = ''.join(bcryptR)

            r_crypt = str.maketrans (cryptJoin, b_end)
            return [text.translate(r_crypt), b_end, cryptJoin]
            print("Random")
        else:
            crypt = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMOPQRSTUVWXYZ+/= :}{'
        size = len(crypt)
        bcryptR = random.sample(crypt, size)
        #print(len(bcrypt))
        b_end = ''.join(bcryptR)

        r_crypt = str.maketrans (crypt, b_end)
        return [text.translate(r_crypt), b_end]
    except:
        return [False, False]

def decode_jwt(jwtx):
    try:
        return jwt.decode(jwtx, KEY_TOKEN_AUTH , algorithms=['HS256'])
    except :
        return False
    
def createStringRandom(size = 0):
    try:
        if size <= 0 or size > 64:
            return False
        else:
            key = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMOPQRSTUVWXYZ+/='
            return ''.join(random.sample(key, size))
    except :
        return False
    
def saveImg(data, route):
    try:
        nameImg = str(getBigRandomString())
        im = Image.open(BytesIO(base64.b64decode(data)))
        im.save('{}'.format(route+nameImg+'.png'), 'PNG')
        return [True, nameImg+'.png']
    except :
        return [False]

def delFile(data, route):
    try:
        os.remove(route+data)
        return True
    except :
        return False

def fixBase64String(b64):
    fixed = str(b64).replace("'", "").replace("*", "").replace('"', "").replace("|", "").replace("%", "").replace("$", "").replace("&", "").replace("?", "").replace('¡', "").replace("\a", "").replace("<", "").replace(">", "").replace("[", "").replace("]", "").replace("(", "").replace("´", "").replace(",", "").replace("!", "").replace("\n", "")
    return fixed

def saveFileCloudDpBx(route, img, routeImg):
    try:
        nameImg = str(getBigRandomString())
        con = dropbox.Dropbox(ACCESS_TOKEN)
        Image64 = Image.open(BytesIO(base64.b64decode(img)))
        nameImage = '{}'.format(nameImg+'.jpg')
        Image64.save(routeImg+nameImage, 'jpeg', quality=90)
        result = ''
        with open(routeImg+nameImage, 'rb') as f:
            result = con.files_upload(f.read(), route+nameImage)

        os.remove(routeImg+nameImage)

        link = con.sharing_create_shared_link(path=route+nameImage, short_url=False)

        ImageFinal = link.url.replace('?dl=0', '?dl=1')
            
        return [True, ImageFinal]
    except Exception as e:
       print(e)
       return [False, '']
    
def updateFileCloudDpBx(route, img, imgPrev):
    try:
        nameImage = str(getBigRandomString()+".jpg")
        con = dropbox.Dropbox(ACCESS_TOKEN)
        Image64 = Image.open(BytesIO(base64.b64decode(img)))
        Image64.save(nameImage, 'jpeg', quality=90)
        result = ''
        with open(nameImage, 'rb') as f:
            result = con.files_upload(f.read(), route+nameImage)

        os.remove(nameImage)

        link = con.sharing_create_shared_link(path=route+nameImage, short_url=False)
        ImageFinal = link.url.replace('?dl=0', '?dl=1')
        
        print("LINK IMG: "+str(ImageFinal))
        
        return [True, ImageFinal]
    except Exception as e:
        print("ERROR FROM services.py / updateFileCloudDpBx")
        print(e)
        return [False, '']
    
def delFileCloudDpBx(route, img):
    try:
        fix = img
        nameImage = fix.replace(".png", ".jpg")
        con = dropbox.Dropbox(ACCESS_TOKEN)
        path = route+nameImage
        con.files_delete(path)
        return True
    except Exception as e:
        print("ERROR FROM services.py / delFileCloudDpBx")
        print(e)
        return False
    
def fixImgB64(img):
    try:
        if "data:image/jpeg;base64," in img:
            imgFix = img.replace("data:image/jpeg;base64,", "")
            return [True, imgFix]
        elif "data:image/png;base64," in img:
            imgFix = img.replace("data:image/png;base64,", "")
            return [True, imgFix]
        else:
            return [False, '']
    except Exception as e:
        print("FROM SERVICES.PY / FIXIMGB64:")
        print(e)
        return [False, '']
    
def sendEmail(receiver, subject, userRec, reason, MsgType='html'):
    """
        MsgType: Tipo de mensaje = html-text,
        receiver: Receptor del mensaje,
        subject: Asunto del mensaje,
        userRec: Información de ayuda para el mensaje,
        reason: 1 = Bienvenida, 2 = recuperar contraseña via telefóno, 3 = recuperar contraseña via correo
    """
    try:
        server = smtplib.SMTP(PROVEEDOR_MAIL)
        server.starttls()
        server.ehlo()
        server.login(CORREO_MAIL, PASSWORD_MAIL)
        msg = MIMEMultipart()

        UTemplate = UTemplates()
        
        message = ''

        if reason == "1":
            message = UTemplate.emailHtmlDefault()
        elif reason == "2":
            UTemplate.info = {
                'name': userRec['name']
            }
            message = UTemplate.recoveryPwdHtml()
        elif reason == "3":
            UTemplate.info = {
                'code': userRec['code'],
                'name': userRec['name']
            }
            message = UTemplate.recoveryPwdEmailHtml()
        else:
            return False

        msg.attach(MIMEText(message, MsgType))
        msg['From'] = CORREO_MAIL
        msg['To'] = receiver
        msg['Subject'] = subject
        server.sendmail(msg['From'] , msg['To'], msg.as_string())
        return True
    except Exception as e:
        print("ERROR FROM sendEmail:")
        print(e)
        return False

def decodeAuth2CertGoogleAPI_py(id_token):
    try:
        certs = requests.get("https://www.googleapis.com/oauth2/v1/certs").json()
        for x in certs:
            for y in certs:
                try:
                    CRT = certs[x]
                    CERT_AUTH2 = str.encode(CRT)
                    cert_obj = load_pem_x509_certificate(CERT_AUTH2, default_backend())
                    pub_key = cert_obj.public_key()
                    token = jwt.decode(id_token, pub_key, algorithms='RS256',audience=AUDIENCE_AUTH2, verify=True)
                    return [True, token]
                except Exception as e2:
                    print("Error decode")
                    print(e2)
                    continue
            break
    except Exception as e:
        print("FROM decodeAuth2CertGoogleAPI error:")
        print(e)
        return [False, '']

def decodeAuth2CertGoogleAPI_GO(id_token):
    try:
        verify = requests.get("https://www.googleapis.com/oauth2/v3/tokeninfo?id_token={}".format(id_token)).json()
        
        for k, v in verify.items():
            if k == "error_description":
                return [False, '']

            if k == "email_verified":
                return [True, verify]

        return [False, '']
    except Exception as e:
        print("ERROR in decodeAuth2CertGoogleAPI_GO")
        print(e)
        return [False, '']

def checkStringEmail(email):
    try:
        root = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
        if(re.search(root, email)):
            return True
        else:
            return False
    except Exception as e:
        print("ERROR FROM checkStringEmail:")
        print(e)
        return False

def checkStringNumberTel(number):
    try:
        root = ['0','1', '2', '3','4', '5', '6', '7', '8', '9']
        if number is None:
            return False

        if len(number) != 12:
            return False
        
        for n in number:
            if n not in root:
                return False

        return True
    except Exception as e:
        print("ERROR FROM checkStringNumberTel:")
        print(e)
        return False

def checkStringNumberSizeType(number, size=0):
    try:
        root = ['0','1','2','3','4','5','6','7','8','9']
        if len(number) != size:
            return False
        
        counter = 0

        for n in number :
            if n not in root:
                return False

            if counter == size:
                break

            counter =+ 1
        
        return True
    except Exception as e:
        print("ERROR FROM checkStringNumberSizeType:")
        print(e)

def encWithPass(data,  pwd=None):
    # Fernet.generate_key() / Generate random key
    try:
        if pwd == None:
            pwd = HIGH_SECRET_KEY_PWD

        pwd = pwd.encode()  
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm = hashes.SHA256(),
            length = 32,
            salt = bytesRandomGlobal,
            iterations = 100000,
            backend = default_backend()
        )
        pwd = base64.urlsafe_b64encode(kdf.derive(pwd))

        key= pwd
        fernet = Fernet(key)
        encMessage = fernet.encrypt(data.encode())
        return [True, encMessage.decode('utf-8')]
    except Exception as e:
        print("ERROR FROM encWithPass:")
        print(e)
        return [False, '']
    
def decWithPass(dataEnc, isJson=False, pwd=None):
    # for use dict: eval(return[1])
    try:
        if pwd == None:
            pwd = HIGH_SECRET_KEY_PWD
            
        pwd = pwd.encode()  
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length = 32,
            salt = bytesRandomGlobal,
            iterations = 100000,
            backend = default_backend()
        )
        pwd = base64.urlsafe_b64encode(kdf.derive(pwd))

        key= pwd
        fernet = Fernet(key)
        dec = fernet.decrypt(dataEnc.encode())
        decDecoded = dec.decode('utf-8')
        decF = decDecoded
        if isJson:
            decF = eval(decDecoded)

        return [True, decF]
    except Exception as e:
        print("ERROR FROM decWithPass:")
        print(e)
        return [False, '']

def createJwt(info, time=10):
    try:
        return jwt.encode({'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=time), 'info': info}, KEY_TOKEN_AUTH , algorithm='HS256')
    except Exception as e:
        print("ERROR FROM createJwt:")
        print(e)
        return False

def createRandomNumberSize(size = 0):
    try:
        if size == 0 or size > 64:
            return False
        else:
            key = '0123456789'
            return ''.join(random.sample(key, size))
    except :
        return False

def sendSMS(number, msg):
    try:
        queryCredits = requests.get(url=API_QUERY_CREDITS_SMS_env)
        querySend = queryCredits.text
        
        print("\nMoney = "+querySend)

        RSend = requests.get(url=API_AUTH2_SMS_env+"&message="+msg+"&numero="+number)
  
        data = RSend.text

        if data[0] == "0":
            queryCredits = requests.get(url=API_QUERY_CREDITS_SMS_env)
            querySend = queryCredits.text

            print("Money = "+querySend)

            return True
        else:
            print("\nSms not sent")

            print(data)

            return False

    except Exception as e:
        print("ERROR FROM sendSMS:")
        print(e)
        return False

def checkIfNumberInt(number):
    try:
        int(number)
        return True
    except Exception as e:
        print("ERROR IN checkIfNumberInt:")
        print(e)
        return False

def initChat(id_emisor = None,  id_evento_grupal = None, typeChat = None, id_receptor = None):
    try:
        """
        Type: 1 = Individual 1 - 1
                  2 = Grupo 1 - *
        """
        
        Response = {
            'estado_invitacion': None,
            'pertenece_grupo': False,
            'son_amigos': False,
            'existen_usuarios': False,
            'existe_grupo': False
        }

        if typeChat == None:
            return Response
        

        if typeChat == "2":
            verificarGrupo = dataTableMysql("SELECT tipo_ev FROM eventos WHERE id = '{}'".format(id_evento_grupal))

            if not verificarGrupo:
                return Response

            for item in verificarGrupo:
                if item[0] != 2:
                    Response['existe_grupo'] = True
                else:
                    Response['existe_grupo'] = False

            verificarEmisor = dataTableMysql("SELECT estado_invitacion FROM eventos_grupales WHERE id_usuario = '{}' AND id_evento = '{}'".format(id_emisor, id_evento_grupal))

            if not verificarEmisor:
                return Response
            
            for item in verificarEmisor:
                Response['estado_invitacion'] = item[0]

            if Response['estado_invitacion'] == 1:
                Response['pertenece_grupo'] = True
            else:
                Response['pertenece_grupo'] = False

            return Response
            
        elif typeChat == "1":
            
            verificarAmistad = dataTableMysql("SELECT id_usuario, id_contacto, estado_invitacion FROM contactos WHERE (id_usuario = '{}' OR id_contacto = '{}') AND (id_usuario = '{}' OR id_contacto = '{}')".format(id_emisor, id_emisor, id_receptor, id_receptor))

            if not verificarAmistad:
                return Response

            for item in verificarAmistad:
                if str(item[0]) == str(id_emisor) and str(item[1]) == str(id_receptor) or str(item[1]) == str(id_emisor) and str(item[0]) == str(id_receptor):
                    Response['existen_usuarios'] = True
                    Response['estado_invitacion'] = item[2]
                    if item[2] == 1:
                        Response['son_amigos'] = True

            return Response
        
        else:
            return Response

    except Exception as e:
        print("ERROR IN initChat:")
        print(e)
        return Response

