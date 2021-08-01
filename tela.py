import PySimpleGUI as sg

# Demo of how columns work
# window has on row 1 a vertical slider followed by a COLUMN with 7 rows
# Prior to the Column element, this layout was not possible
# Columns layouts look identical to window layouts, they are a list of lists of elements.

sg.theme('DarkAmber')   # Add a touch of color

# Column layout
col_browse = [[sg.Text('Pasta de Dados (.CSV)', size=(20,0)), sg.Input(size=(40,0), key='csv_folder'), sg.FolderBrowse()],
              [sg.Text('Pasta de Modelos', size=(20,0)), sg.Input(size=(40,0), key='models_folder'), sg.FolderBrowse()],
              [sg.Text('Pasta de Certificados', size=(20,0)), sg.Input(size=(40,0), key='destination_folder'), sg.FolderBrowse()]]
col_lines = [[sg.Text('Altura da linha (única)', size=(22,0)), sg.Slider(range=(0,1000), default_value=500, orientation='h', size=(15,12), key="y1")],
             [sg.Text('Altura da linha (múltiplas)', size=(22,0)), sg.Slider(range=(0,1000), default_value=500, orientation='h', size=(15,12), key="y2")]]
col_font = [[sg.Text('Comprimento', size=(15,0)), sg.Input(size=(10, 0), key="width")],
            [sg.Text('Tamanho da fonte', size=(15,0)), sg.Input(size=(10, 0), key="font_size")],
            [sg.Text('Espacamento',size=(15,0)), sg.Input(size=(10,0), key="espacamento")]]
col_total = [[sg.Column(col_browse)], [sg.Column(col_lines), sg.Column(col_font)]]

layout = [[sg.Image(r'wallpaper_ieee.png'), sg.Column(col_total)],
          [sg.Button('Anterior', size=(12,0), key="prev"), sg.Button('Proximo', size=(12,0), key="next"), 
          sg.Text(size=(60,0)), sg.Cancel(), sg.OK()]]

# Display the window and get values

window = sg.Window('Gerador de Certificados', layout)
while True:
  event, values = window.read()
  if event in (sg.WIN_CLOSED, 'Cancel', 'OK'):
    break
  
window.close()
# sg.Popup(event, values, line_width=200)
