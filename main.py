from encryptor import Encryptor
from decryptor import Decryptor
publicCertificate = "/Users/mcastro/Desktop/public.pem"
privateCertificate = "/Users/mcastro/Desktop/private.pem"
jsonFile = "/Users/mcastro/Desktop/encrypt.json"

keysize = 32        #32 bytes
blockSize = 128     #128 bits
ivSize = 16         #16 bytes

inputString = input("Input message to encrypt: ")
print("Encrypting message: ", inputString)
myEncryptor = Encryptor(keysize, blockSize, ivSize, inputString, publicCertificate, jsonFile)
myEncryptor.encrypt()
print("Message encrypted")

print("\nMessasge will now be decrypted")
myDecryptor = Decryptor(keysize, blockSize, ivSize, jsonFile, privateCertificate)
myDecryptor.decrypt()
