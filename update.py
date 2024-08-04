"""modpack updater"""

import zipfile
import shutil
import urllib.request, urllib.error
import json
from tkinter import messagebox
from sys import exit as sysexit


API_URL = "https://api.github.com/repos/lolcatjpg/mcgang-modded-creative-modpack/releases/latest"
RELEASE_URL = "https://github.com/lolcatjpg/mcgang-modded-creative-modpack/releases/latest/download/mods.zip"
MC_DIR = "test"


# check if current version is latest
try:
    with urllib.request.urlopen(API_URL) as response:
        latest_release = json.load(response)["name"]
except urllib.error.HTTPError:
    messagebox.showerror("URL not found", "could not check for updates because the api url could not be accessed.\n(returned HTTPError)")
    print("[modpack updater] exited due to HTTPError")
    sysexit(0)
except urllib.error.URLError:
    messagebox.showerror("URL could not be accessed",
                        "could not check for updates because the api url could not be accessed.\ncheck your internet connection.\n(returned URLError)")
    print("[modpack updater] exited due to URLError")
    sysexit(0)

with open("version.txt", encoding="UTF8") as file:
    current_release = file.readline()

if current_release == latest_release:
    print(f"[modpack updater] your modpack is up to date!\n(current release: {current_release})")
    sysexit(0)

# ask if user wants to update
UPDATE_AVAILABLE_MESSAGE = f"new update available: your current release is {current_release}, latest release is {latest_release}. \n\ninstall update?"
if not messagebox.askokcancel("update found", UPDATE_AVAILABLE_MESSAGE):
    print("[modpack updater] update cancelled by user")
    sysexit(0)
# -> contine if user wants to update

# download modpack
try:
    urllib.request.urlretrieve(RELEASE_URL, "mods.zip")
    print("[modpack updater] > modpack downloaded")
except urllib.error.HTTPError:
    messagebox.showerror("URL not found", "could not download update because the download url could not be accessed.\n(returned HTTPError)")
    print("[modpack updater] exited due to HTTPError")
    sysexit(0)
except urllib.error.URLError:  # should normally never happen bc at this point it could access the api url? but implementing it anyways bc who knows
    messagebox.showerror("URL could not be accessed",
                        "could not download update because the download url could not be accessed.\ncheck your internet connection.\n(returned URLError)")
    print("[modpack updater] exited due to URLError")
    sysexit(0)

# delete old mods.old and rename mods to mods.old
shutil.rmtree(f"{MC_DIR}/mods.old/", ignore_errors=True)
shutil.move(f"{MC_DIR}/mods/", f"{MC_DIR}/mods.old/")
print(f"[modpack updater] > renamed {MC_DIR}/mods to {MC_DIR}/mods.old")

# extract zip file
with zipfile.ZipFile("mods.zip") as archive:
    # print(archive.namelist())
    archive.extractall(f"{MC_DIR}/mods/")
    print(f"[modpack updater] > extracted mods archive to {MC_DIR}/mods")

# move mmc_pack.json
shutil.move(f"{MC_DIR}/mods/mmc-pack.json", "mmc-pack.json")
print(f"[modpack updater] > moved {MC_DIR}/mods/mmc-pack.json to ./mmc-pack.json")

# update version file
with open("version.txt", "w", encoding="UTF8") as file:
    file.write(latest_release)
    print("updated version file")

# notify user of success
messagebox.showinfo("modpack updated", f"modpack successfully updated!\ncurrent version: {latest_release}")
