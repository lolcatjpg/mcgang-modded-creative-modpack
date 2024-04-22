import subprocess

subprocess.run('git fetch origin main && git reset --hard origin/main', shell=True)
