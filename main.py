
publicCertificate = "/Users/mcastro/Documents/public.pem"
privateCertificate = "/Users/mcastro/Documents/private.pem"
import os
import base64

iv = os.urandom(16)  # generate iv
byteMSG = bytes("CECS478", "UTF-8")
test = iv + byteMSG

print(iv)
print(type(byteMSG))
print(byteMSG)
print(test)

iv2 = test[:16]
print("iv2:", iv2)
