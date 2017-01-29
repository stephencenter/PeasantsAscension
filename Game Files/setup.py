import sys
from cx_Freeze import setup, Executable

setup(
    name = "Peasants' Ascension",
    version = "v1.0.0 Beta",
    description = "A fun RPG programmed in Python",
    executables  = [Executable("PeasantsAscension.py", base = "console")])
