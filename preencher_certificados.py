from PIL import Image, ImageDraw, ImageFont
import PySimpleGUI as sg
import pandas as pd
import textwrap
import os.path

# TO-DO:
# Atualizar a imagem do certificado automaticamente

class PreencherCertificados:
  
  def __init__(self):
    
    sg.theme('DarkAmber')

    self.__col_browse = [[sg.Text('Pasta de Dados (.CSV)', size=(20,0)), sg.Input(size=(40,0), key='csv_folder', default_text="./_recursos/csv"), sg.FolderBrowse()],
                         [sg.Text('Pasta de Modelos', size=(20,0)), sg.Input(size=(40,0), key='models_folder', default_text="./_recursos/modelos"), sg.FolderBrowse()],
                         [sg.Text('Pasta de Certificados', size=(20,0)), sg.Input(size=(40,0), key='destination_folder', default_text="./certificados"), sg.FolderBrowse()],
                         [sg.Text('Altura da linha (única / múltiplas)', size=(28,0)), sg.Slider(range=(0,1000), default_value=500, orientation='h', size=(17,12), key="y1"),
                          sg.Slider(range=(0,1000), default_value=500, orientation='h', size=(17,12), key="y2")]]
    self.__col_font = [[sg.Text('Comprimento', size=(15,0)), sg.Input(size=(6, 0), key="width")],
                       [sg.Text('Tamanho da fonte', size=(15,0)), sg.Input(size=(6, 0), key="font_size")],
                       [sg.Text('Espaçamento',size=(15,0)), sg.Input(size=(6  ,0), key="espacamento")]]
    self.__col_font_color = [[sg.Text('Red', size=(5,0)), sg.Spin([rc for rc in range(0, 255)], key="red", size=(4,0))],
                             [sg.Text('Green', size=(5,0)), sg.Spin([gc for gc in range(0, 255)], key="green", size=(4,0))],
                             [sg.Text('Blue', size=(5,0)), sg.Spin([bc for bc in range(0, 255)], key="blue", size=(4,0))]]
    self.__col_name = [[sg.Text('Coluna de Nomes', size=(15,0)), sg.Input(size=(15,0), key="names_col", default_text="Nome Completo")],
                       [sg.Text('Fonte', size=(5,0)), sg.Input(size=(15,0), key='font', default_text="./recursos/fonte.ttf"), sg.FileBrowse(size=(4,0))],
                       [sg.Cancel(), sg.Button('Update'), sg.OK(size=(5,0))]]

    self.__col_total = [[sg.Column(self.__col_browse)], [sg.Column(self.__col_font), sg.Column(self.__col_font_color), sg.Column(self.__col_name)]]

    self.__layout = [[sg.Image(r'wallpaper_ieee.png'), sg.Column(self.__col_total)],
                     [sg.Button('<<', size=(3,0), key="prev_model"), sg.Button('>>', size=(3,0), key="next_model"), sg.Text(size=(5,0)), sg.Button('<', size=(3,0), key="prev"), sg.Button('>', size=(3,0), key="next")]]
    
    self.__data = list()
    self.__models = list()
    self.__folders = list()

    self.__cont = 0
    self.__cont_model = 0


  def initInterface(self):
    self.window = sg.Window('Gerador de Certificados', self.__layout)
    while True:
      self.event, self.values = self.window.read()
      if self.event in (sg.WIN_CLOSED, 'Cancel'):
        break
      elif self.event == '<' and self.__cont > 0:
        self.__cont -= 1
      elif self.event == '>' and self.__cont < 10:
        self.__cont += 1
      elif self.event == '<<' and self.__cont_model > 0:
          self.__cont_model -= 1
      elif self.event == '>>' and self.__cont_model < 10:
        self.__cont_model += 1
      elif self.event == 'OK':
        self.getData()
        self.generateCertificates()
        break
      window.close()


  def getData(self):

    self.__font = ImageFont.truetype(font="_recursos/fonte.ttf", size=int(self.values['font_size']))

    if not os.path.isdir(self.values['destination_folder']):
      os.mkdir('./'+self.values['destination_folder'])
    self.__certificates = [os.path.splitext(filename)[0] for filename in os.listdir(self.values['destination_folder'])]

    self.__wks = [os.path.splitext(filename)[0] for filename in os.listdir(self.values['csv_folder'])]
    for wk in self.__wks:
      self.__data.append(wk+'.csv')
      self.__models.append(wk+'.png')
      self.__folders.append(self.values['destination_folder']+'/'+wk)

  def writeCertificate(self, img, col):
    certificado = img.copy()
    W, H = certificado.size
    text = col[self.values['names_col']]
    text_wrap = textwrap.wrap(text, width=int(self.values['width']))
    draw = ImageDraw.Draw(certificado)
    current_h = (int(self.values['y1'])/1000)*H if (len(text_wrap) < 2) else (int(self.values['y2'])/1000)*H
    for line in text_wrap:
      w, h = draw.textsize(line, font=self.__font)
      draw.text(xy=((W-w)/2, (current_h)), text=line, fill=(255,255,255), font=self.__font)
      current_h += h + int(self.values['espacamento'])
    return certificado, text


  def generateCertificates(self):

    for pasta in self.__folders:
      if not os.path.isdir(pasta):
        os.mkdir('./'+pasta)

    for i, wk in enumerate(self.__data):

      self.__data = pd.read_csv(self.values['csv_folder']+'/'+wk)
      img = Image.open(self.values['models_folder']+'/'+self.__models[i])

      for _, col in self.__data.iterrows():
        certificado, name = self.writeCertificate(img, col)
        certificado_pdf = certificado.convert('RGB')
        certificado_pdf.save(self.__folders[i]+f'/{name}.pdf')

      print(wk[:-4].upper() + " finalizado...")

    sg.Popup("", "Todos os certificados foram gerados com sucesso!")
