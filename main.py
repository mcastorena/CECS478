publicCertificate = "/Users/mcastro/Documents/public.pem"
privateCertificate = "/Users/mcastro/Documents/private.pem"
from encryptor import Encryptor
from decryptor import Decryptor
import os
import base64

keysize = 32        #32 bytes
blockSize = 128     #128 bits
ivSize = 16         #16 bytes

# iv = os.urandom(16)  # generate iv
# byteMSG = bytes("CECS478", "UTF-8")
# test = iv + byteMSG
#
# print(iv)
# print(type(byteMSG))
# print(byteMSG)
# print(test)
#
# iv2 = test[:16]
# print("iv2:", iv2)

inputString = input("Input message to encrypt: ")
print("Encrypting message: ", inputString)
myEncryptor = Encryptor(keysize, blockSize, ivSize, inputString, publicCertificate)
myEncryptor.encrypt()
print("Message encrypted")

print("Messasge will now be decrypted")
myDecryptor = Decryptor(keysize, blockSize, ivSize, "/Users/mcastro/Desktop/encrypt.json", privateCertificate)
myDecryptor.decrypt()

