import time
import threading
from services.services import *

class sendEmailAndSMSThreading:
    def __init__(self, info):
        self.info = info
        self.response = [False, False]

    def call1(self): # send Email
        self.response[0] = sendEmail(subject=self.info['S-Email']['subject'], receiver=self.info['S-Email']['receiver'], userRec=self.info['S-Email']['userRec'], reason=self.info['S-Email']['reason'])

        return self.response[0]

    def call2(self): # send SMS
        self.response[1] = sendSMS(number=self.info['S-SMS']['number'], msg=self.info['S-SMS']['msg'])

        return self.response[1]

    def run(self):
        # creating threads
        t1 = threading.Thread(name='call1', target=self.call1, daemon=True)
        t2 = threading.Thread(name='call2', target=self.call2, daemon=True)

        # init threads
        t1.start()
        t2.start()

        # join threads
        t1.join()
        t2.join()

        if self.response[0] and self.response[1]:
            return True
        else:
            return False