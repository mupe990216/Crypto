import pdfkit, base64
from jinja2 import Environment, FileSystemLoader

def get_image_file_as_base64_data(pathFile):
    with open(pathFile, 'rb') as image_file:
        return base64.b64encode(image_file.read()).decode()

def generate_PDF(paths,data):
    config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
    env = Environment(loader=FileSystemLoader(paths['TEMPLATE']))
    template = env.get_template("pdf.html")
    img_pathAux = paths['PICTURES']+"\\logo.png"
    logo_DESart = get_image_file_as_base64_data(img_pathAux)
    img_pathAux = paths['PICTURES']+"\\ESCOM.png"
    logo__ESCOM = get_image_file_as_base64_data(img_pathAux)
    img_pathAux = paths['ARTS_DIR']+"\\"+data[5]
    Select_Arts = get_image_file_as_base64_data(img_pathAux)
    html = template.render(id=data,art=Select_Arts,DESart=logo_DESart,ESCOM=logo__ESCOM)
    newPDF = paths['CERTIFICATES']+"\\"+data[1]+".pdf"
    pdfkit.from_string(html,newPDF,configuration=config)
    print(" * PDF Created")