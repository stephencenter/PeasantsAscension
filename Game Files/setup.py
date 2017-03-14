from cx_Freeze import setup, Executable
import sys

sys.path.append("C:\\Users\Stephen Center\\Documents\\Peasants' Ascension\\Game Files\\Content")
sys.path.append("C:\\Users\Stephen Center\\Documents\\Peasants' Ascension\\Game Files\\Scripts")
sys.path.append("C:\\Users\Stephen Center\\Documents\\Peasants' Ascension\\Game Files\\Classes")

setup(name="Peasants' Ascension",
      version="v1.0.0 Beta",
      description="A fun RPG programmed in Python",
      executables=[Executable("PeasantsAscension.py", base="console", icon="peasant_icon.ico")])
