"""modpack updater"""

import zipfile
import shutil

MC_DIR = "test"

# delete old mods.old and rename mods to mods.old
shutil.rmtree(f"{MC_DIR}/mods.old/", ignore_errors=True)
shutil.move(f"{MC_DIR}/mods/", f"{MC_DIR}/mods.old/")

# extract zip file
with zipfile.ZipFile("test/mods.zip") as archive:
    print(archive.namelist())
    archive.extractall(f"{MC_DIR}/mods/")

# move mmc_pack.json
shutil.move(f"{MC_DIR}/mods/mmc-pack.json", "mmc-pack.json")
