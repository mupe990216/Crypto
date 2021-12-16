import base64, hashlib, shutil, os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

def key_generation_AES(path,name):
    oldPath = path+"\\"+name
    key = get_random_bytes(16) # Size 128 bits
    fileBase64 = base64.b64encode(key)
    with open(oldPath,"wb") as kFile:
        kFile.write(fileBase64)
        kFile.close()
    file = open(oldPath,"rb")
    fileHash = hashlib.sha256(file.read()).hexdigest()
    file.close()
    newPath = path+"\\"+fileHash
    shutil.copyfile(oldPath, newPath)
    os.remove(oldPath)
    return fileHash

def read_key(pathkey,keyName):
    pathKey = pathkey+"\\"+keyName
    with open(pathKey) as kFile:
        linesDocument = kFile.readlines()        
        kFile.close()
    fileDecode = base64.b64decode(linesDocument[0])
    return fileDecode

def encrypt_AES(pathkey,keyName,pathOld,imgName,pathNew):
    oldpath=pathOld+"\\"+imgName
    key = read_key(pathkey,keyName)
    # Read a original image
    cipher = AES.new(key, AES.MODE_CBC)
    # cipher = AES.new(key, AES.MODE_GCM)
    pFile = open(oldpath,"rb")
    plaintext = pFile.read()
    pFile.close
    # Save a image encrypted
    newpath=pathNew+"\\"+imgName
    ciphertext = cipher.encrypt(pad(plaintext,AES.block_size))
    cFile = open(newpath,"wb")
    cFile.write(cipher.iv)
    cFile.write(ciphertext)
    cFile.close()

def decrypt_AES(pathkey,keyName,pathOld,imgName,pathNew):
    oldpath=pathOld+"\\"+imgName
    key = read_key(pathkey,keyName)
    # Read a image encrypted
    cFile = open(oldpath,"rb")
    iv = cFile.read(len(key))
    ciphertext = cFile.read()
    cFile.close()
    # Save a image decrypted
    newpath=pathNew+"\\"+imgName
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    pFile = open(newpath,"wb")
    pFile.write(plaintext)
    pFile.close()
    # Verify hash img
    hash_img_test(pathNew,imgName)

def hash_img_test(path,filename):
    oldPath = path+"\\"+filename
    file = open(oldPath,"rb")
    fileHash = hashlib.sha256(file.read()).hexdigest()
    file.close()
    print(fileHash)