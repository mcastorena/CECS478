import os
import base64
import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding as p
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding


class Encryptor(object):
    def __init__(self, keySize, blockSize, ivSize, publicCertificate, jsonFile):
        self.keySize = keySize
        self.publicCertificate = publicCertificate
        self.message = None
        self.ivSize = ivSize
        self.blockSize = blockSize
        self.AESKey = None
        self.HMACKey = None
        self.cipherText = None
        self.jsonFile = jsonFile


    def encrypt(self, message):
        self.message = message
        b64MSG =  base64.encodebytes(self.AESEncrypt())            #AES encrypt message then bytes to b64
        ASCIIMsg = b64MSG.decode('ascii')                           #b64 to ascii
        b64HMAC = base64.encodebytes(self.HMAC())                    #HMAC then digest to b64
        ASCIIHMAC = b64HMAC.decode('ascii')                        #b64 to ascii
        b64Keys = base64.encodebytes(self.RSAEncrypt())             #RSA encrypt keys then bytes to b64
        ASCIIKeys = b64Keys.decode('ascii')                         #b64 to ascii
        data = {'Msg': ASCIIMsg, 'HMAC': ASCIIHMAC, 'Keys': ASCIIKeys}  #create dictionary with our data
        return data
        #jsonData = json.dumps(data)                                                #dictionary to json object
        #with open(self.jsonFile, 'w') as outFile:
        #    json.dump(jsonData, outFile)                                            #write to jsonFile

    def AESEncrypt(self):
        key = os.urandom(self.keySize)  # generate key
        self.AESKey = key               # save AESKey
        iv = os.urandom(self.ivSize)  # generate iv
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())  # create cipher object using AES in CBC mode using the generated key and iv
        AESEncryptor = cipher.encryptor()                                       # create encryptor object from cipher object
        byteMSG = bytes(self.message, "UTF-8")                                  #message string to bytes
        bytesIVMSG = iv + byteMSG                                               #prepend IV to MSG
        padder = p.PKCS7(self.blockSize).padder()  # create padder object using PKCS7, blocksize = 128
        paddedMSG = padder.update(bytesIVMSG) + padder.finalize()    #pad fileStr, which is the file read as string
        cipherText = AESEncryptor.update(paddedMSG) + AESEncryptor.finalize()           #Encrypt paddedMSG and return cipherText
        self.cipherText = cipherText
        return cipherText

    def HMAC(self):
        HMACKey = os.urandom(self.keySize)  # generate HMAC key
        self.HMACKey = HMACKey              # save HMAC key
        h = hmac.HMAC(HMACKey, hashes.SHA256(), backend=default_backend())  # create hash algorithm object
        h.update(self.cipherText)  # bytes to hash and authenticate
        return h.finalize()  # finalize hash and return digest as bytes


    def RSAEncrypt(self):
        with open(self.publicCertificate, "rb") as publicKey:                                #load public key from filepath
            public_key = serialization.load_pem_public_key(publicKey.read(),backend=default_backend())
        keys = self.AESKey + self.HMACKey                                                    #concatenate keys
        cipherKeys = public_key.encrypt(keys, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(),label=None))  # encrypt keys
        return cipherKeys

