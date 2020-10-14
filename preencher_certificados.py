from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import textwrap
import os.path

certificados = ['arduino_basico', 'arduino_avançado']
coluna_nomes = 'Nome'
pasta_dados = 'recursos/csv'
pasta_modelos = 'recursos/modelos'
font = ImageFont.truetype(font="recursos/fonte.ttf", size=60)

dados = list()
modelos = list()
pastas = list()
for wk in certificados:
  dados.append(wk+'.csv')
  modelos.append(wk+'.png')
  pastas.append(wk)

for pasta in pastas:
  if not os.path.isdir(pasta):
    os.mkdir('./'+pasta)

for i, wk in enumerate(dados):

  dados = pd.read_csv(pasta_dados+'/'+wk)
  img = Image.open(pasta_modelos+'/'+modelos[i])
  W, H = img.size

  for lin, col in dados.iterrows():
    certificado = img.copy()
    text = col[coluna_nomes]
    text_wrap = textwrap.wrap(text, width=25)
    draw = ImageDraw.Draw(certificado)
    current_h = 0.35*H if (len(text_wrap) < 2) else 0.32*H
    for line in text_wrap:
      w, h = draw.textsize(line, font=font)
      draw.text(xy=((W-w)/2, (current_h)), text=line, fill=(0,0,0), font=font)
      current_h += h + 4
    certificado_pdf = certificado.convert('RGB')
    certificado_pdf.save(pastas[i]+f'/{text}.pdf')
