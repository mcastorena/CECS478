from encryptor import Encryptor
from decryptor import Decryptor
from client import Client
import requests
publicCertificate = "/Users/mcastro/Desktop/public.pem"
privateCertificate = "/Users/mcastro/Desktop/private.pem"
jsonFile = "/Users/mcastro/Desktop/encrypt.json"
loginURL = "http://54.153.48.132:3000/api/authenticate"
chatURL = "http://54.153.48.132:3000/api/chat"

keysize = 32        #32 bytes
blockSize = 128     #128 bits
ivSize = 16         #16 bytes

choice = None
choice = input("Input 1 to login, 2 to register: ")

if(choice == '1'):

    inputEmail = input("Enter email address: ")
    inputPassword = input("Enter password: ")

    print("Logging in user: ", inputEmail)
    myClient = Client(loginURL)
    try:
        myClient.login(inputEmail, inputPassword)               #login with given email and password
    except ValueError:                                          #if login fails prompt user for username and password again
        inputEmail = input("Enter email address: ")
        inputPassword = input("Enter password: ")
        myClient.login(inputEmail, inputPassword)

    session = True                                              #session boolean set to true
    myEncryptor = Encryptor(keysize, blockSize, ivSize, publicCertificate)
    myDecryptor = Decryptor(keysize, blockSize, ivSize, privateCertificate)

    option = None
    while(session):                                             #prompt user to send/check messages
        print("Input options: \n\t1: Send message \n\t2: Check messages \n\t3: Logout\n")
        option = input("Input choice: ")

        if(option == '1'):                                        #send message
            recipient = input("Enter recipient email: ")
            msg = input("Enter message:\t")
            encryptedMsg = myEncryptor.encrypt(msg)             #encrypt message before sending
            myClient.postMsg(chatURL, recipient, encryptedMsg)  #send encrypted message

        elif(option == '2'):                                        #check messages
            responseData = myClient.getMsg(chatURL)               #send get request
            head = responseData['Headers']                        #get headers
            msgResponse = responseData['Response']                #get response
            for myMsg in msgResponse.json():
                if (myMsg['msgRead'] == False):           # print only unread messages
                    msgID = myMsg['_id']
                    putURL = chatURL + "/" + str(msgID)           #get put URL to send PUT request to update unread messages as read
                    updateRespose = requests.put(putURL, headers=head, data={'msgRead': True})          #get update response
                    print("Sender ID: ", myMsg['from'])
                    print("Sent at: ", myMsg['createdAt'])
                    body = myMsg['message_body']                    #get message body
                    bodyList = body.split(" ")                      #parse message body into list
                    HMAC = None                                     #init body fields
                    Keys = None
                    Msg = None
                    try:                                            #get body fields
                        HMAC = bodyList[1]
                        Keys = bodyList[3]
                        Msg = bodyList[5]
                    except:
                        print("Parse failed")

                    try:                                            #Decrypt message
                        data = {'HMAC': HMAC, 'Keys': Keys, 'Msg': Msg}
                        print("My decrypted msg: ", myDecryptor.decrypt(data))
                    except:
                        print("Decrypt failed\n")

                    print("\n")
        elif(option == '3'):
            session = False                                     #session boolean = false
            print("Logging out user: ", inputEmail)
            exit(0)                                             #exit program
        else:                                                   #invalid input
            print("Invalid option selected\n")
elif(choice =='2'):
    regEmail = input("Input registration email: ")
    regPass = input("Input password: ")
    myClient = Client(loginURL)
    myClient.register(regEmail, regPass)
else:
    print("Bad input")
