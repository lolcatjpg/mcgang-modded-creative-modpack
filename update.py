"""modpack updater"""

import zipfile
import shutil
import urllib.request
import urllib.error
import json
import tomllib
from tkinter import messagebox
from sys import exit as sysexit
from os import environ, chdir, getcwd


# set working directory to prism launcher instance path, if found
inst_dir = environ.get("INST_DIR", ".")
chdir(inst_dir)
print(f"[modpack updater] current working directory: {getcwd()}")

# load config
with open("updater_config.toml", "rb") as f:
    config = tomllib.load(f)
    print(f"[modpack updater] api url: {config['api-url']}")
    print(f"[modpack updater] release url: {config['release-url']}")
    print(f"[modpack updater] minecraft dir: {config['mc-dir']}")

# check if current version is latest
try:
    with urllib.request.urlopen(config["api-url"]) as response:
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

try:
    with open("version.txt", encoding="UTF8") as file:
        current_release = file.readline()
except FileNotFoundError:
    current_release = "unknown (because the updater script has not been used yet)"

if current_release == latest_release:
    print(f"[modpack updater] your modpack is up to date! (current release: {current_release})")
    sysexit(0)

# ask if user wants to update
UPDATE_AVAILABLE_MESSAGE = f"new update available: your current release is {current_release}, the latest release is {latest_release}. \n\ninstall update?"
if not messagebox.askokcancel("update found", UPDATE_AVAILABLE_MESSAGE):
    print("[modpack updater] update cancelled by user")
    sysexit(0)
# -> contine if user wants to update

# download modpack
try:
    print("[modpack updater] > downloading modpack...")
    urllib.request.urlretrieve(config["release-url"], "mods.zip")
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
shutil.rmtree(f"{config["mc-dir"]}/mods.old/", ignore_errors=True)
shutil.move(f"{config["mc-dir"]}/mods/", f"{config["mc-dir"]}/mods.old/")
print(f"[modpack updater] > renamed {config["mc-dir"]}/mods to {config["mc-dir"]}/mods.old")

# extract zip file
with zipfile.ZipFile("mods.zip") as archive:
    # print(archive.namelist())
    archive.extractall(f"{config["mc-dir"]}/mods/")
    print(f"[modpack updater] > extracted mods archive to {config["mc-dir"]}/mods")

# move mmc_pack.json
shutil.move(f"{config["mc-dir"]}/mods/mmc-pack.json", "mmc-pack.json")
print(f"[modpack updater] > moved {config["mc-dir"]}/mods/mmc-pack.json to ./mmc-pack.json")

# update version file
with open("version.txt", "w", encoding="UTF8") as file:
    file.write(latest_release)
    print("updated version file")

# notify user of success
messagebox.showinfo("modpack updated", f"modpack successfully updated!\ncurrent version: {latest_release}")
