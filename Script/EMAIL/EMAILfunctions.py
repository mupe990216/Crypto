import smtplib, getpass, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.encoders import encode_base64

def send_contracts_email(files,data):
    try:
        user = "test.projects.school@gmail.com"
        pswd = "T0stad0ra3000"
        # pswd = getpass.getpass(" * Password email: ")
        remitente = "D-E-S art support"
        destinatario = "{};{};{}".format(data[6:9])
        asunto = "Contract D-E-S art"
        mensaje = "<h1>Contract of art</h1><br><p>Artist:{}</p><br><p>Client:{}</p><br><p>Public Notary:{}</p><p>Certificate registration: {}<a href='localhost/contracts/{}}'>{}}</a></p>".format(data[6:9],data[1],data[1],data[1])
        certificate = files['CERTIFICATES']+"\\"+data[1]+".pdf"
        digital_Art = files['A_SIGNED']+"\\"+data[5]
        Tconditions = files['CONDITIONS']+"\\"+"terms.pdf"

        # Host and port SMTP for gmail
        gmail = smtplib.SMTP("smtp.gmail.com",587)

        # Procol cipher TLS
        gmail.starttls()

        # Login
        gmail.login(user,pswd)

        # Depuration true
        gmail.set_debuglevel(1)

        # Headers to send by TLS
        header = MIMEMultipart()
        header['Subject'] = asunto
        header['From'] = remitente
        header['To'] = destinatario

        mensaje = MIMEText(mensaje,"html")
        header.attach(mensaje)

        if(os.path.isfile(certificate)):
            if(os.path.isfile(digital_Art)):
                if(os.path.isfile(Tconditions)):
                    certifi = MIMEBase("application","octet-stream")
                    certifi.set_payload(open(certificate,"rb").read())
                    encode_base64(certifi)
                    certifi.add_header("Content-Disposition","attachment; filename={}".format(os.path.basename(certificate)))
                    header.attach(certifi)
                    img_Art = MIMEBase("application","octet-stream")
                    img_Art.set_payload(open(digital_Art,"rb").read())
                    encode_base64(img_Art)
                    img_Art.add_header("Content-Disposition","attachment; filename={}".format(os.path.basename(digital_Art)))
                    header.attach(img_Art)
                    adjunto = MIMEBase("application","octet-stream")
                    adjunto.set_payload(open(Tconditions,"rb").read())
                    encode_base64(adjunto)
                    adjunto.add_header("Content-Disposition","attachment; filename={}".format(os.path.basename(Tconditions)))
                    header.attach(adjunto)

        gmail.sendmail(remitente,destinatario.split(';'),header.as_string())

        gmail.quit()
        print(" * Email send succesful")
    except Exception as e:
        print("\n *** Exception sending Email: {} \n".format(e))





