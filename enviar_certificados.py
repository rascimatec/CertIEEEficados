import smtplib
import pandas as pd
from email.message import EmailMessage

df = pd.read_csv('recursos/nomes.csv')

from_email = input("Endereço de email: ")
password = input("Digite a senha: ")

titulo = 'Teste de email com anexo em Python'
texto = 'Segue o certificado em anexo'

server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.login(from_email, password)
print("Login sucedido")

for lin, col in df.iterrows():
  
  msg = EmailMessage()
  msg['From'] = from_email
  msg['Subject'] = titulo
  msg['To'] = col['Email']
  msg.set_content(texto)

  file_name = col['Nome']+'.pdf'
  with open('certificados/'+file_name, 'rb') as f:
    file_data = f.read()

  msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

  server.send_message(msg)
  print("Email enviado para " + col['Nome'])
