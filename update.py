"""modpack updater"""

import zipfile
from os import rename
from shutil import rmtree

MC_DIR = "test/"


rmtree(f"{MC_DIR}mods.old/", ignore_errors=True)
rename(f"{MC_DIR}mods/", f"{MC_DIR}mods.old/")

with zipfile.ZipFile("test/mods.zip") as archive:
    print(archive.namelist())
    archive.extractall(f"{MC_DIR}mods/")
