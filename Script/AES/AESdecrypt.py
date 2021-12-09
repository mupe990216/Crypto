from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

kFile = open("Key","rb")
key = kFile.read()
kFile.close()

cFile = open("img_Cipher.jpg","rb")
iv = cFile.read(len(key))
ciphertext = cFile.read()
cFile.close()

cipher = AES.new(key, AES.MODE_CBC, iv)
plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

pFile = open("img_Decrypted.jpg","wb")
pFile.write(plaintext)
pFile.close()