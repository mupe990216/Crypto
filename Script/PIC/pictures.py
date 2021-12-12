import os, hashlib, shutil
from PIL import Image,ImageDraw,ImageFont

def watermark(filename, text,pic):
    # Crea una instancia del objeto de imagen
    img = Image.open(filename)
    w, h = img.size  # Obtenga el ancho y el alto de la imagen para calcular la posición relativa de la imagen
    print(pic+"Altura de la imagen:",h)
    print(pic+"Ancho de la imagen:",w)
    print("==========================================")
    # Establecer fuente, tamaño de fuente
    font = ImageFont.truetype("calibri.ttf", int(w/5))  
    draw = ImageDraw.Draw(img)
    '''
           Los cuatro ajustes de parámetros de draw.text: posición del texto (abscisas, ordenadas) / contenido / color / fuente
           El primer parámetro ajusta la posición relativa de la inserción de texto (la dirección del eje de coordenadas de la pantalla es la siguiente)
                   →w
                  ↓
                   h
     '''
    # draw.text((w/6,h/1.2), text=text, fill=(255, 255, 255), font=font)
    draw.text((w/20,h/3), text=text, fill=(255, 255, 255), font=font)
    # Crear si la siguiente carpeta no existe
    if not os.path.exists("marked_images"):
        os.mkdir("marked_images")
    save_name=pic.split(".")[0]+"_marked.jpg"#Establezca el nombre de la imagen después de agregar la marca de agua
    img.save("./marked_images/"+save_name)


# Esta funcion copia el archivo que se acaba de subir con su nombre cambiado por el hash de este mismo
def hash_img(path,filename):
    oldPath = path+"\\"+filename
    file = open(oldPath,"rb")
    fileHash = hashlib.sha256(file.read()).hexdigest()
    formatImg = filename.rsplit(".", 1)[1].lower()
    newPath = path+"\\"+fileHash+"."+formatImg
    shutil.copyfile(oldPath, newPath)
    return fileHash+"."+formatImg

# Una vez que la imagen ya tiene una copia con su hash, se elimina la original
def rm_img(path,filename):
    oldPath = path+"\\"+filename
    os.remove(oldPath)

# La imagen 

# if __name__ == '__main__':
#     text = "©D-E-S art"
#     director_path="./images/"#Guardar la ruta de la carpeta de imágenes
#     pictures=os.listdir(director_path)# Obtenga todos los nombres de las imágenes en la carpeta
#     for pic in pictures:
#         filename=director_path+pic#Construye el nombre de la ruta de cada imagen
#         watermark(filename,text,pic)#Añadir marca de agua
#     print("Todo procesado")