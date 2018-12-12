import requests

class Client(object):
    def __init__(self, url):
        self.URL = url
        self.payload = None
        self.email = None
        self.password = None
        self.response = None
        self.JWT = None
        self.token = None

    def register(self, email, password):

        payload = {'email': email, 'password': password}
        requests.post("http://54.153.48.132:3000/api/register", data = payload)        #post request
        print("User: ", email, "registered succesfully")
        # try:
        #     payload = {'email': email, 'password': password}
        #     requests.post("54.153.48.132:3000/api/register", data = payload)        #post request
        #     print("User: ", email, "registered succesfully")
        # except:
        #     print("Registration failed.")

    def login(self, email, password):
        try:
            self.payload = {'email': email, 'password': password}
            self.response = requests.post(self.URL, data=self.payload)          #store server response
            self.JWT = self.response.json()                                     #get payload
            self.token = self.JWT['token']                                      #get token
            print("Login succesful")
        except:
            raise ValueError('Login failed')

    def postMsg(self, URL, recipient, message):             #message passed as dictionary containing msg, keys, and HMAC tag
        print("Sending message...")
        head = {'Authorization': self.token}                #create header
        mymessage = "HMAC: "+str(message['HMAC'])+" Keys: "+ str(message['Keys'])+ " Msg: "+str(message['Msg'])     #create message in string format
        body = {'to': recipient, 'message_body': mymessage}                                                         #post request body
        try:
            msgResponse = requests.post(URL, headers= head, data= body)                                             #send message
        except:
            raise ValueError('Message could not be sent')



    def getMsg(self, URL):
        print("Fetching new messages...")
        head = {'Authorization': self.token}            #get JWT token
        msgResponse = requests.get(URL, headers=head)   #send request and save return object
        data = {'Response': msgResponse, 'Headers': head}   #return dictionary with messages and header
        return data



