import smtplib
import pandas as pd
from email.message import EmailMessage

certificados = ['abertura', 'analise_de_dados']

from_email = input("Endereço de email: ")
password = input("Digite a senha: ")

titulo = 'Teste de email com anexo em Python'
texto = 'Segue o certificado em anexo'

server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.login(from_email, password)
print("Login sucedido")

for certificado in certificados:
  print("ENVIANDO " + certificado)
  df = pd.read_csv('_recursos/csv/'+certificado+'.csv')
  for lin, col in df.iterrows():
    
    msg = EmailMessage()
    msg['From'] = from_email
    msg['Subject'] = titulo
    msg['To'] = col['Endereço de e-mail']
    msg.set_content(texto)

    file_name = col['Nome Completo']+'.pdf'
    with open('_certificados/'+certificado+'/'+file_name, 'rb') as f:
      file_data = f.read()

    msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

    server.send_message(msg)
    print("  -> Email enviado para " + col['Nome Completo'])
  
