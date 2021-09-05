from PIL import Image, ImageDraw, ImageFont
import PySimpleGUI as sg
import pandas as pd
import textwrap
import os.path
import io


class PreencherCertificados:
  
  def __init__(self):
    
    sg.theme('DarkAmber')

    self.__col_browse = [[sg.Text('Pasta de Dados (.CSV)', size=(20,0)), sg.Input(size=(40,0), key='csv_folder', default_text="./materiais/csv"), sg.FolderBrowse()],
                         [sg.Text('Pasta de Modelos', size=(20,0)), sg.Input(size=(40,0), key='models_folder', default_text="./materiais/modelos"), sg.FolderBrowse()],
                         [sg.Text('Pasta de Certificados', size=(20,0)), sg.Input(size=(40,0), key='destination_folder', default_text="./certificados"), sg.FolderBrowse()],
                         [sg.Text('Altura da linha (única / múltiplas)', size=(28,0)), sg.Slider(range=(0,1000), default_value=500, orientation='h', size=(17,12), key="y1"),
                          sg.Slider(range=(0,1000), default_value=500, orientation='h', size=(17,12), key="y2")]]
    self.__col_font = [[sg.Text('Comprimento', size=(15,0)), sg.Input(size=(6, 0), key="width", default_text="10")],
                       [sg.Text('Tamanho da fonte', size=(15,0)), sg.Input(size=(6, 0), key="font_size", default_text="100")],
                       [sg.Text('Espaçamento',size=(15,0)), sg.Input(size=(6, 0), key="espacamento", default_text="10")]]
    self.__col_font_color = [[sg.Text('Red', size=(5,0)), sg.Spin([rc for rc in range(0, 256)], key="red", size=(4,0))],
                             [sg.Text('Green', size=(5,0)), sg.Spin([gc for gc in range(0, 256)], key="green", size=(4,0))],
                             [sg.Text('Blue', size=(5,0)), sg.Spin([bc for bc in range(0, 256)], key="blue", size=(4,0))]]
    self.__col_name = [[sg.Text('Coluna de Nomes', size=(15,0)), sg.Input(size=(15,0), key="names_col", default_text="Nome Completo")],
                       [sg.Text('Fonte', size=(5,0)), sg.Input(size=(15,0), key='font', default_text="./materiais/fonte.ttf"), sg.FileBrowse(size=(4,0))],
                       [sg.Cancel(), sg.Button('Update', key='update'), sg.OK(size=(5,0))]]

    self.__col_total = [[sg.Column(self.__col_browse)], [sg.Column(self.__col_font), sg.Column(self.__col_font_color), sg.Column(self.__col_name)]]

    self.__layout = [[sg.Image(r'wallpaper_ieee.png', key="image"), sg.Column(self.__col_total)],
                     [sg.Button('<<', size=(3,0), key="prev_model"), sg.Button('>>', size=(3,0), key="next_model"), sg.Text(size=(5,0)), sg.Button('<', size=(3,0), key="prev"), sg.Button('>', size=(3,0), key="next")]]
    
    self.__data = list()
    self.__models = list()
    self.__folders = list()

    self.__cont = 0
    self.__cont_model = -1

    self.__timeout = None


  def initInterface(self):
    self.window = sg.Window('Gerador de Certificados', self.__layout)
    while True:
      self.event, self.values = self.window.read(timeout=self.__timeout)
      self.getData()
      if self.event in (sg.WIN_CLOSED, 'Cancel'):
        break
      elif self.event == 'OK':
        self.generateCertificates()
        break
      elif self.event == 'update':
        if not os.path.isdir(self.values['csv_folder']):
          self.__timeout = None
        elif not os.path.isdir(self.values['models_folder']):
          self.__timeout = None
        else:
          self.__timeout = 100
      elif self.__timeout != None:
        if self.event == 'prev' and self.__cont > 0:
          self.__cont -= 1
        elif self.event == 'next' and self.__cont < len(pd.read_csv(self.values['csv_folder'] + '/' + self.__data[self.__cont_model])) - 1:
          self.__cont += 1
        elif self.event == 'prev_model' and self.__cont_model > 0:
            self.__cont_model -= 1
            self.__cont = 0
        elif self.event == 'next_model' and self.__cont_model < len(self.__wks)-1:
          self.__cont_model += 1
          self.__cont = 0
      if self.__timeout != None:
        self.updateInterface()

    self.window.close()

  def updateInterface(self):
    wk = self.__data[self.__cont_model]
    self.__wk_data = pd.read_csv(self.values['csv_folder'] + '/' + wk)
    img = Image.open(self.values['models_folder']+'/'+self.__models[self.__cont_model])

    for i, col in self.__wk_data.iterrows():
      if i == self.__cont:
        image, _ = self.writeCertificate(img, col)    
        image.thumbnail((420, 420))
        bio = io.BytesIO()
        image.save(bio, format="PNG")
        self.window.Element('image').Update(data=bio.getvalue())
        break


  def getData(self):

    if not os.path.isfile(self.values['font']):
      sg.Popup("Erro", "Arquivo de fonte .ttf não existe. Insira um arquivo válido.")
      self.__font = None
      self.__timeout = None
    else:
      self.__font = ImageFont.truetype(font=self.values['font'], size=int(self.values['font_size']))

    if not os.path.isdir(self.values['csv_folder']):
      sg.Popup("Erro", "Pasta de Dados (.CSV) não existe. Insira um caminho válido.")
      self.__timeout = None
    elif not os.path.isdir(self.values['models_folder']):
      sg.Popup("Erro", "Pasta de Modelos não existe. Insira um caminho válido.")
      self.__timeout = None
    else:
      self.__data = []
      self.__models = []
      self.__folders = []
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
      draw.text(xy=((W-w)/2, (current_h)), text=line, fill=(int(self.values['red']), int(self.values['green']), int(self.values['blue'])), font=self.__font)
      current_h += h + int(self.values['espacamento'])
    return certificado, text


  def generateCertificates(self):
    if not os.path.isdir(self.values['destination_folder']):
      os.mkdir(self.values['destination_folder'])

    for pasta in self.__folders:
      if not os.path.isdir(pasta):
        os.mkdir(pasta)

    for i, wk in enumerate(self.__data):

      self.__data = pd.read_csv(self.values['csv_folder']+'/'+wk)
      img = Image.open(self.values['models_folder']+'/'+self.__models[i])

      for _, col in self.__data.iterrows():
        certificado, name = self.writeCertificate(img, col)
        certificado_pdf = certificado.convert('RGB')
        certificado_pdf.save(self.__folders[i]+f'/{name}.pdf')

      print(wk[:-4].upper() + " finalizado...")

    sg.Popup("", "Todos os certificados foram gerados com sucesso!")



if __name__ == "__main__":
  gerador = PreencherCertificados()
  gerador.initInterface()
