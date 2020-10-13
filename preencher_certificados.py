from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import textwrap

df = pd.read_csv('recursos/nomes.csv')
font = ImageFont.truetype(font="recursos/fonte.ttf", size=60)
img = Image.open('recursos/modelo.png')
W, H = img.size

for lin, col in df.iterrows():
  certificado = img.copy()
  text = col['Nome']
  text_wrap = textwrap.wrap(text, width=25)
  draw = ImageDraw.Draw(certificado)
  current_h = 0.35*H if (len(text_wrap) < 2) else 0.32*H
  for line in text_wrap:
    w, h = draw.textsize(line, font=font)
    draw.text(xy=((W-w)/2, (current_h)), text=line, fill=(0,0,0), font=font)
    current_h += h + 4
  certificado_pdf = certificado.convert('RGB')
  certificado_pdf.save('certificados/{}.pdf'.format(text))
