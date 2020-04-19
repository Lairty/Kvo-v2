from cx_Freeze import setup, Executable

options = {'build.exe': {'includes': ['askItem', 'backImageSprites', 'Board', 'conn', 'Enemeys', 'Items', 'LoadImage',
                                      'mainGameBoard', 'Menu', 'names', 'Player']}}
setup(name="Knight vs Orc", version='1.0', description='Good game',
      options=options, executables=[Executable('main.py')])
