

import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding as p
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding


class Encryptor(object):
    def __init__(self, keySize, blockSize, ivSize, message, publicCertificate):
        self.keySize = keySize
        self.publicCertificate = publicCertificate
        self.message = message
        self.ivSize = ivSize
        self.blockSize = blockSize
        self.AESKey = None
        self.HMACKey = None
        self.cipherText = None


    def encrypt(self):
        asciiMSG = (self.AESEncrypt()).decode('UTF-8')
        asciiHMAC = (self.HMAC(self.cipherText)).decode('UTF-8')
        asciiKeys = (self.RSAEncrypt()).decode('UTF-8')
        return

    def AESEncrypt(self):
        key = os.urandom(self.keySize)  # generate key
        self.AESKey = key               # save AESKey
        iv = os.urandom(self.ivSize)  # generate iv
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())  # create cipher object using AES in CBC mode using the generated key and iv
        AESEncryptor = cipher.encryptor()  # create encryptor object
        byteMSG = bytes(self.message, "UTF-8")                                  #message string to bytes
        bytesIVMSG = iv + byteMSG                                               #prepend IV to MSG
        padder = p.PKCS7(self.blockSize).padder()  # create padder object using PKCS7, blocksize = 128
        paddedMSG = padder.update(bytesIVMSG) + padder.finalize()    #pad fileStr, which is the file read as string
        cipherText = AESEncryptor.update(paddedMSG) + AESEncryptor.finalize()           #Encrypt paddedMSG and return cipherText
        self.cipherText = cipherText
        return cipherText

    def HMAC(self,cipherText):
        HMACKey = os.urandom(self.keySize)  # generate HMAC key
        self.HMACKey = HMACKey              # save HMAC key
        h = hmac.HMAC(HMACKey, hashes.SHA256(), backend=default_backend())  # create hash algorithm object
        h.update(cipherText)  # bytes to hash and authenticate
        digest = h.finalize()  # finalize hash and return digest as bytes
        return digest

    def RSAEncrypt(self):
        with open(self.publicCertificate, "rb") as publicKey:                                #load public key from filepath
            public_key = serialization.load_pem_public_key(publicKey.read(),password=None,backend=default_backend())
        keys = self.AESKey + self.HMACKey
        cipherKeys = publicKey.encrypt(keys, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(),label=None))  # encrypt keys
        return cipherKeys

Encryptor(32, 128, 16, "CECS478", "/Users/mcastro/Documents/public.pem").encrypt()
