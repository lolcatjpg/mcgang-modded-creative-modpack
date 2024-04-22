import subprocess
from tkinter import messagebox

update = messagebox.askokcancel('update', 'Update modpack?')
if update == True:
    subprocess.run('git fetch origin main && git reset --hard origin/main', shell=True)

