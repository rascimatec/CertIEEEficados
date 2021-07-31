import smtplib
import pandas as pd
from email.message import EmailMessage

class EnviarCertificado:
  def __init__(self):
    self.certificados = ['abertura', 'analise_de_dados']

  def setEmail(self):
    self.from_email = input("Endereço de email: ")
    self.password = input("Digite a senha: ")

    self.titulo = 'Teste de email com anexo em Python'
    self.texto = 'Segue o certificado em anexo'

    self.server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    self.server.login(self.from_email, self.password)
    print("Login sucedido")

def enviarCertificados(self):
  for certificado in self.certificados:
    print("ENVIANDO " + certificado)
    df = pd.read_csv('_recursos/csv/'+certificado+'.csv')
    for lin, col in df.iterrows():
      
      msg = EmailMessage()
      msg['From'] = self.from_email
      msg['Subject'] = self.titulo
      msg['To'] = col['Endereço de e-mail']
      msg.set_content(self.texto)

      file_name = col['Nome Completo']+'.pdf'
      with open('_certificados/'+certificado+'/'+file_name, 'rb') as f:
        file_data = f.read()

      msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

      self.server.send_message(msg)
      print("  -> Email enviado para " + col['Nome Completo'])
    