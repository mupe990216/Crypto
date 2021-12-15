import os, hashlib, shutil
from PIL import Image,ImageDraw,ImageFont

# Esta funcion crea una copia de la original que se usara para su previsualziacion con marca de agua
def watermark(oldPath, filename, newPath):
    img = Image.open(oldPath+"\\"+filename)
    w, h = img.size
    font = ImageFont.truetype("calibri.ttf", int(w/5))
    draw = ImageDraw.Draw(img)
    draw.text((w/50,h/50), text='©D-E-S art\n©D-E-S art\n©D-E-S art\n©D-E-S art\n©D-E-S art\n©D-E-S art\n©D-E-S art\n©D-E-S art\n©D-E-S art\n©D-E-S art\n©D-E-S art\n©D-E-S art', fill=(205, 205, 205), font=font)
    img.save(newPath+"\\"+filename)
    file = open(newPath+"\\"+filename,"rb")
    print(hashlib.sha256(file.read()).hexdigest())
    file.close()


# Esta funcion copia el archivo que se acaba de subir con su nombre cambiado por el hash de este mismo
def hash_img(path,filename):
    oldPath = path+"\\"+filename
    file = open(oldPath,"rb")
    fileHash = hashlib.sha256(file.read()).hexdigest()
    formatImg = filename.rsplit(".", 1)[1].lower()
    newPath = path+"\\"+fileHash+"."+formatImg
    file.close()
    shutil.copyfile(oldPath, newPath)
    return fileHash+"."+formatImg

# Una vez que la imagen ya tiene una copia con su hash, se elimina la original
def rm_img(path,filename):
    oldPath = path+"\\"+filename
    os.remove(oldPath)
    print(" * Image eliminated")

# Se copia la imagen a una nueva ruta
def copy_img(oldPath, filename, newPath):
    old_path = oldPath+"\\"+filename
    new_path = newPath+"\\"+filename
    shutil.copyfile(old_path, new_path)
    print(" * Image to sign copied")
