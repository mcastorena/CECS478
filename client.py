from encryptor import Encryptor
from decryptor import Decryptor
import requests
publicCertificate = "/Users/mcastro/Desktop/public.pem"
privateCertificate = "/Users/mcastro/Desktop/private.pem"

class Client(object):
    def __init__(self, url):
        self.URL = url
        self.payload = None
        self.email = None
        self.password = None
        self.response = None
        self.JWT = None
        self.token = None

        
    def singUp (self, email, password, URL):
        try:
            self.payload = {'email': email, 'password' : password}
            self.response = requests.posts( URL, params = self.payload)
            self.JWT = self.response.json()
            self.token = self.JWT['token']
            print("Sign up succesful")
        except:
            raise ValueError('Sign up failed')

        
    def login(self, email, password):
        try:
            self.payload = {'email': email, 'password': password}
            self.response = requests.post(self.URL, data=self.payload)          #store server response
            self.JWT = self.response.json()                                     #get payload
            self.token = self.JWT['token']                                      #get token
            print("Login succesful")
        except:
            raise ValueError('Login failed')

    def postMsg(self, URL, recipient, message):
        print("Sending message...")
        head = {'Authorization': self.token}
        body = {'to': recipient, 'message_body': message}

        msgResponse = requests.post(URL, headers=head, data=body)
        # try:
        #     msgResponse = requests.post(URL, headers= head, data= body)
        # except:
        #     raise ValueError('Message could not be sent')



    def getMsg(self, URL):
        print("Fetching new messages...")
        head = {'Authorization': self.token}
        msgResponse = requests.get(URL, headers=head)
        return msgResponse
        # try:
        #     msgResponse = requests.get(URL, headers=head)
        #     return msgResponse
        # except:
        #     raise ValueError('Messages could not be fetched')



