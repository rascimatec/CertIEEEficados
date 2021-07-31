from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import textwrap
import os.path


class PreencherCertificados:
  def __init__(self):
    self.certificados = ['abertura', 'analise_de_dados']
    self.coluna_nomes = 'Nome Completo'
    self.pasta_dados = '_recursos/csv'
    self.pasta_modelos = '_recursos/modelos'
    self.pasta_certificados = '_certificados'

    self.dados = list()
    self.modelos = list()
    self.pastas = list()

  def setFont(self):
    self.y1 = 0.41
    self.y2 = 0.375
    self.width = 30
    self.font_size = 85
    self.espacamento = 4
    self.font = ImageFont.truetype(font="_recursos/fonte.ttf", size=font_size)

  def getData(self):
    if not os.path.isdir(self.pasta_certificados):
      os.mkdir('./'+self.pasta_certificados)

    for wk in certificados:
      self.dados.append(wk+'.csv')
      self.modelos.append(wk+'.png')
      self.pastas.append(pasta_certificados+'/'+wk)

  def generateCertificates(self):

    for pasta in self.pastas:
      if not os.path.isdir(self.pasta):
        os.mkdir('./'+self.pasta)

    for i, wk in enumerate(self.dados):

      self.dados = pd.read_csv(pasta_dados+'/'+wk)
      img = Image.open(self.pasta_modelos+'/'+modelos[i])
      W, H = img.size

      for lin, col in self.dados.iterrows():
        certificado = img.copy()
        text = col[coluna_nomes]
        text_wrap = textwrap.wrap(text, width=width)
        draw = ImageDraw.Draw(certificado)
        current_h = y1*H if (len(text_wrap) < 2) else y2*H
        for line in text_wrap:
          w, h = draw.textsize(line, font=font)
          draw.text(xy=((W-w)/2, (current_h)), text=line, fill=(255,255,255), font=font)
          current_h += h + espacamento
        certificado_pdf = certificado.convert('RGB')
        certificado_pdf.save(pastas[i]+f'/{text}.pdf')

      print(wk[:-4]+ " finalizado...")

    print("Todos os certificados foram gerados com sucesso!")
