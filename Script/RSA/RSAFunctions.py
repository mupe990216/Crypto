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

def read_private_key(path,fileName):
    file = open(path+"\\"+fileName, 'r')
    private_key = RSA.import_key(file.read())
    file.close()
    return private_key

def read_public_key(path,fileName):
    file = open(path+"\\"+fileName, 'r')
    public_key = RSA.import_key(file.read())
    file.close()
    return public_key

def signing_data(oldPath,fileName,newPath,private_key):
    try:
        separator = '\n\n\\'
        imge = open(oldPath+"\\"+fileName, "rb") # read bytes
        data = imge.read()
        data = base64.encodebytes(data)
        data_hash = SHA256.new()
        data_hash.update(data)
        signer = PKCS115_SigScheme(private_key)
        signature = signer.sign(data_hash)
        signed_file = open(newPath+"\\"+fileName, "wb") # write bytes
        signed_file.write(base64.decodebytes(data))
        signed_file.write(separator.encode('utf-8'))
        signed_file.write(binascii.hexlify(signature))
        signed_file.close()
        imge.close()
        return "Art signed successful"
    except Exception as e:
        print("\n *** Exception RSA Signing: {} \n".format(e))
        return e

def verify_signature(path,fileName,public_key,ignore = 0):
    try:
        signed_file_aux = open(path+"\\"+fileName, "rb") # Name of the sign document
        signature = signed_file_aux.read()
        separator = '\n\n\\'
        parts = signature.split(bytes(separator, 'utf-8'))
        data = b''
        # In case that found more separator
        # Always the last part will be the sign or signs, others parts will be data from the file
        for i in range(len(parts) - 1 - ignore):
            data += parts[i]
            if(i != len(parts) - 2 - ignore):
                data += bytes(separator, 'utf-8')
        data = base64.encodebytes(data)
        sign = parts[len(parts) - 1 - ignore]
        sign = binascii.unhexlify(sign)
        # We need the hash of data file for sign a file
        data_hash = SHA256.new()
        data_hash.update(data)
        verification = PKCS115_SigScheme(public_key)
        verification.verify(data_hash, sign)
        signed_file_aux.close()
        return "Art signed successful"
    except Exception as e:
        # print("\n *** Exception RSA Verify Sign: {} \n".format(e))
        return "Invalid Art"

# generate_key_RSA("./")
# public_key_artist = read_public_key("../../keys/","6519e2d6b68f043e92864c2106b52c3a9195cbc5cacdf973389b5db98d57738e.key")
# private_key_artist = read_private_key("../../keys/","5b50a9bbbe618f38b7289b7ffef3a4609392c7681501ae8f0c0960762d407a97.key")
# print("Artist Sign: "+signing_data("./","test2.jpg","./artist/", private_key_artist))
# print("Artist Very: "+verify_signature("./artist/","test2.jpg",public_key_artist))

# public_key_client = read_private_key("../../keys/","c5aae9adb097ad23584b47cdf2bc3313edf4aa4978bf21d10f73b52a1215e6e5.key")
# private_key_client = read_private_key("../../keys/","9aa99cb2dc2e78b69a1160f87c9bf1608e0ab13d52557ad89ad14126c9d763b7.key")
# print("Client Sign: "+signing_data("./artist/","test2.jpg","./client/", private_key_client))
# print("Client Very: "+verify_signature("./client/","test2.jpg",public_key_client))

# public_key_notary = read_private_key("../../keys/","2941f9418888ad88f00a7dfd4532983e2499cafae6073f43ea3230a688eb03a5.key")
# private_key_notary = read_private_key("../../keys/","aa3d9072877bbc5a75e025aa5517fbec2021978e8f685569101bedf509670824.key")
# print("Notary Sign: "+signing_data("./client/","test2.jpg","./notary/", private_key_notary))
# print("Notary Very: "+verify_signature("./notary/","test2.jpg",public_key_notary))

# private_key_ext = read_private_key("./","8efda4ffc4dfd9e0f005ae95cf39acfc53962730d4c6fa4795daee33087b4169.key")
# public_key_ext = read_private_key("./","2c3f1b028e5cc495ae4314e10a30f4ad2a8406cb6e7f6999ed856a1fd656d144.key")
# print("Other Very: "+verify_signature("./notary/","test2.jpg",public_key_ext))


# print("Artist Very: "+verify_signature("./client/","test2.jpg",public_key_artist,1))
# print("Client Very: "+verify_signature("./client/","test2.jpg",public_key_client,0))


# print("Artist Very: "+verify_signature("./notary/","test2.jpg",public_key_artist,2))
# print("Client Very: "+verify_signature("./notary/","test2.jpg",public_key_client,1))
# print("Notary Very: "+verify_signature("./notary/","test2.jpg",public_key_notary,0))


# private_key_artist = read_private_key("./","4965b53e810067ffb5350d2add29eb028fdbfe85202a2ea6f622e001135e429d.key")
# public_key_artist = read_private_key("./","a8f518aa68ba86a4d89e4cb116ebd91a63260f3d7490e407e1cd5868db7e7552.key")
# print("Artist Sign: "+signing_data("./","test2.jpg","./artist/", private_key_artist))
# print("Artist Very: "+verify_signature("./artist/","test2.jpg",public_key_artist))

# private_key_client = read_private_key("./","e0091fec680e4ff553881e6798d0c839e5105fe06c47cf41ada846cd8c970eb3.key")
# public_key_client = read_private_key("./","6ca6d9abe30b313a8fcef9862540c5a07180625a82d5fd25cc488ba963642c3c.key")
# print("Client Sign: "+signing_data("./artist/","test2.jpg","./client/", private_key_client))
# print("Client Very: "+verify_signature("./client/","test2.jpg",public_key_client))

# private_key_notary = read_private_key("./","d8dc173fbdee5ffbd7ae7fb033b57a12b23219ab2c77475638184bffe4b8a91f.key")
# public_key_notary = read_private_key("./","8cdfd5642cc40ee483ae2b303f2f89c0c7463aa32b1eb2dbea5d55e179abf496.key")
# print("Notary Sign: "+signing_data("./client/","test2.jpg","./notary/", private_key_client))
# print("Notary Very: "+verify_signature("./notary/","test2.jpg",public_key_client))
# private_key_ext = read_private_key("./","8efda4ffc4dfd9e0f005ae95cf39acfc53962730d4c6fa4795daee33087b4169.key")
# public_key_ext = read_private_key("./","2c3f1b028e5cc495ae4314e10a30f4ad2a8406cb6e7f6999ed856a1fd656d144.key")
# print("Other Very: "+verify_signature("./notary/","test2.jpg",public_key_ext))


# print("Artist Very: "+verify_signature("./notary/","test2.jpg",public_key_client))
# print("Client Very: "+verify_signature("./notary/","test2.jpg",public_key_client))
# print("Notary Very: "+verify_signature("./notary/","test2.jpg",public_key_client))

