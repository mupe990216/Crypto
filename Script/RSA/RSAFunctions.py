import os, base64, binascii, shutil, hashlib
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme

def generate_key_RSA(pathForKey):
    path_private_key = pathForKey+"\\"+"private_key.key"
    path_public_key = pathForKey+"\\"+"public_key.key"
    private_key = RSA.generate(2048)

    # Generate Private key
    file = open(path_private_key, 'wb')
    file.write(private_key.export_key())
    file.close()

    # Generate Public key
    public_key = private_key.publickey()
    file = open(path_public_key, 'wb')
    file.write(public_key.export_key())
    file.close()

    # Store Private key
    file = open(path_private_key,"rb")
    fileHash = hashlib.sha256(file.read()).hexdigest()
    file.close()
    newPath = pathForKey+"\\"+fileHash+".key"
    hashPrivateKey = fileHash+".key"
    shutil.copyfile(path_private_key, newPath)
    os.remove(path_private_key)
    
    # Store Public key
    file = open(path_public_key,"rb")
    fileHash = hashlib.sha256(file.read()).hexdigest()
    file.close()
    newPath = pathForKey+"\\"+fileHash+".key"
    hashPublicKey = fileHash+".key"
    shutil.copyfile(path_public_key, newPath)
    os.remove(path_public_key)
    result = {'privateKey':hashPrivateKey,'publicKey':hashPublicKey}
    return result

# generate_key_RSA("./keys")