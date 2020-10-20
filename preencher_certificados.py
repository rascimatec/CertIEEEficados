from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import textwrap
import os.path

certificados = ['abertura', 'analise_de_dados']

y1 = 0.41
y2 = 0.375
width = 30
font_size = 85
espacamento = 4

coluna_nomes = 'Nome Completo'
pasta_dados = '_recursos/csv'
pasta_modelos = '_recursos/modelos'
pasta_certificados = '_certificados'
font = ImageFont.truetype(font="_recursos/fonte.ttf", size=font_size)

if not os.path.isdir(pasta_certificados):
  os.mkdir('./'+pasta_certificados)

dados = list()
modelos = list()
pastas = list()
for wk in certificados:
  dados.append(wk+'.csv')
  modelos.append(wk+'.png')
  pastas.append(pasta_certificados+'/'+wk)

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
