from client import Client
import requests
publicCertificate = "/Users/mcastro/Desktop/public.pem"
privateCertificate = "/Users/mcastro/Desktop/private.pem"
jsonFile = "/Users/mcastro/Desktop/encrypt.json"
loginURL = "http://54.153.48.132:3000/api/authenticate"
chatURL = "http://54.153.48.132:3000/api/chat"
signURL = "http://54.153.48.132:3000/api/register"


keysize = 32        #32 bytes
blockSize = 128     #128 bits
ivSize = 16         #16 bytes


ession = True
while (session):
    print("Input options: \n\t1: Sign up \n\t2: Login")
    option = input("Input choice: ")

    if (option == '1'):
        inputEmail = input("Enter email address: ")
        inputPassword = input("Enter password: ")

        print("Logging in user: ", inputEmail)
        myClient = Client(signURL)
        myClient.signUp(inputEmail, inputPassword)               #login with given email and password
   if (option == '2'):
        print("Logging in user: ", inputEmail)
        myClient = Client(loginURL)
        try:
            myClient.login(inputEmail, inputPassword)  # login with given email and password
        except ValueError:  # if login fails prompt user for username and password again
            inputEmail = input("Enter email address: ")
            inputPassword = input("Enter password: ")
            myClient.login(inputEmail, inputPassword)

session = True                                              #session boolean set to true
myEncryptor = Encryptor(keysize, blockSize, ivSize, publicCertificate, jsonFile)
myDecryptor = Decryptor(keysize, blockSize, ivSize, jsonFile, privateCertificate)


while(session):                                             #prompt user to send/check messages
    print("Input options: \n\t1: Send message \n\t2: Check messages \n\t3: Logout\n")
    option = input("Input choice: ")

    if(option == '1'):                                        #send message
        recipient = input("Enter recipient email: ")
        msg = input("Enter message:\t")
        encryptedMsg = myEncryptor.encrypt(msg)             #encrypt message before sending

        myClient.postMsg(chatURL, recipient, encryptedMsg)

        # try:
        #     myClient.postMsg(chatURL, encryptedMsg)
        # except:
        #     print("Message could not be sent")
    if(option == '2'):                                        #check messages
        msgResponse = myClient.getMsg(chatURL)
        print(msgResponse.json())
        # try:
        #     print(myClient.getMsg(chatURL))
        # except:
        #     print("Error fetching messages")
    if(option == '3'):
        session = False                                     #session boolean = false
        print("Logging out user: ", inputEmail)
        exit(0)                                             #exit program
    else:                                                   #invalid input
        print("Invalid option selected\n")
