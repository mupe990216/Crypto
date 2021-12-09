from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

key = get_random_bytes(16)

kFile = open("Key","wb")
kFile.write(key)
kFile.close()

cipher = AES.new(key, AES.MODE_CBC)

pFile = open("img_Original.jpg","rb")
plaintext = pFile.read()
pFile.close

ciphertext = cipher.encrypt(pad(plaintext,AES.block_size))

cFile = open("img_Cipher.jpg","wb")
cFile.write(cipher.iv)
cFile.write(ciphertext)
cFile.close()