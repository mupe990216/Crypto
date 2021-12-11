from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from tkinter import filedialog

kFile = open("Key","rb")
key = kFile.read()
kFile.close()


path = filedialog.askopenfilename(title="Select your Art",filetypes=(("jpg files","*.jpg"),("All files","*.*")))
filename = path.split("/")                                           

cFile = open(filename[-1],"rb")
iv = cFile.read(len(key))
ciphertext = cFile.read()
cFile.close()

cipher = AES.new(key, AES.MODE_CBC, iv)
plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

pFile = open("img_Decrypted.jpg","wb")
pFile.write(plaintext)
pFile.close()