import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
  base = "Win32GUI"

executables = [Executable("preencher_certificados.py", base=base, icon="icon.ico")]

buildOptions = dict( packages = [],
                     includes = ["PIL", "PySimpleGUI", "textwrap", "pandas", "io", "os"],
                     include_files = ["wallpaper_ieee.png", "icon.ico"],
                     excludes = []
                   )

setup(name="Gerador de Certificados",
      version = "0.2",
      description = "Gerador automático de certificados",
      options = dict(build_exe = buildOptions),
      executables = executables
     )
