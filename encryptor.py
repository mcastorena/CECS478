import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding


class Encryptor(object):
    def __init__(self, keySize, blockSize, ivSize, message, publicCertificate):
        self.keySize = keySize
        self.publicCertificate = publicCertificate
        self.message = message
        self.ivSize = ivSize
        self.padder = padding.PKCS7(blockSize).padder()              #create padder object using PKCS7, blocksize = 128
        self.blockSize = blockSize


    def encrypt(self):
        return

    def AESEncrypt(keySize, message):
        key = os.urandom(keySize)  # generate key
        iv = os.urandom(ivSize)  # generate iv
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())  # create cipher object using AES in CBC mode using the generated key and iv
        AESEncryptor = cipher.encryptor()  # create encryptor object
        msg = iv + message                  # prepend IV to message befor encryption
        paddedMSG = padder.update(msg) + padder.finalize()    #pad fileStr, which is the file read as string
        cipherText = AESEncryptor.update(paddedMSG) + AESEncryptor.finalize()           #Encrypt paddedMSG and return cipherText
        return cipherText

