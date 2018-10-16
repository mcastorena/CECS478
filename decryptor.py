import os
import base64
import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding as p
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding


class Decryptor(object):
    def __init__(self, keySize, blockSize, ivSize, jsonFile, privateCertificate):
        self.keySize = keySize
        self.privateCertificate = privateCertificate
        self.jsonFile = jsonFile
        self.ivSize = ivSize
        self.blockSize = blockSize
        self.msg = None
        self.HMAC = None
        self.keys = None
        self.AESKey = None
        self.HMACKey = None

    def decrypt(self):
        with open(self.jsonFile) as jsonFile:  # open JSON file
            jsonData = json.load(jsonFile)  # load json data from file
            data = json.loads(jsonData)  # load json data into dictionary
        ASCIIMsg = data['Msg']  # get values from dictionary
        ASCIIHMAC = data['HMAC']
        ASCIIKeys = data['Keys']

        b64MSG = ASCIIMsg.encode('ascii')  # ascii to b64
        b64HMAC = ASCIIHMAC.encode('ascii')
        b64Keys = ASCIIKeys.encode('ascii')

        self.msg = base64.decodebytes(b64MSG)  # b64 to bytes
        self.HMAC = base64.decodebytes(b64HMAC)
        self.keys = base64.decodebytes(b64Keys)

        self.RSADecrypt()
        self.HMACVerify()
        self.AESDecrypt()

    def RSADecrypt(self):
        with open(self.privateCertificate, 'rb') as keyFile:  # open private certificate file
            privateKey = serialization.load_pem_private_key(keyFile.read(), password=None,
                                                            backend=default_backend())  # create privatekey object
        keys = privateKey.decrypt(self.keys,
                                  padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(),
                                               label=None))  # RSA Decrypt
        self.AESKey = keys[:self.keySize]  # slice AES key
        self.HMACKey = keys[(self.keySize):]  # slice HMAC key


    def HMACVerify(self):

        h = hmac.HMAC(self.HMACKey, hashes.SHA256(), backend=default_backend()) #re-generates hash tag
        h.update(self.msg)  #creating a new hash stored in the object
        h.verify(self.HMAC)  #veryfing if the HMACs matches if thye do it will return true and if it fails it throws an error


    def AESDecrypt(self):
        IV = self.msg[:self.ivSize]  # slicing the iv
        CT = self.msg[self.ivSize:]  # slicing the blocksize
        decryptor =  CT.decryptor()
        CT = decryptor.update(CT) + decryptor.finalize()
        unpadder = padding.PKCS7(self.blockSize).unpadder()
        CT = unpadder.update(CT) + unpadder.finalize()
        CT = str(CT, 'utf-8')
        print("Decrypted Message: ", CT)
