from cx_Freeze import setup, Executable

setup(name="Peasants' Ascension",
      version="1.0.0",
      description="An open-world, text-based RPG programmed in Python",
      executables=[Executable("PeasantsAscension.py", base="console", icon="peasant_icon.ico")])
