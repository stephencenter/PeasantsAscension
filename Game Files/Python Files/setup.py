from cx_Freeze import setup, Executable

setup(name="Peasants' Ascension",
      version="1.0.0",
      description="A fun, text-based RPG programmed in Python",
      executables=[Executable("PeasantsAscension.py", base="console", icon="peasant_icon.ico")])
