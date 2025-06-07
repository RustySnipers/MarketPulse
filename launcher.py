import json
import subprocess
import sys
import tempfile
from pathlib import Path

import requests
from packaging import version

from version import __version__ as APP_VERSION

MANIFEST_URL = "https://github.com/your-username/market-pulse/releases/latest/download/manifest.json"
APP_NAME = "Market Pulse"


def check_update():
    try:
        resp = requests.get(MANIFEST_URL, timeout=5)
        data = resp.json()
        if version.parse(data.get("version", "0")) > version.parse(APP_VERSION):
            return data.get("installer_url")
    except Exception:
        pass
    return None


def prompt_update():
    choice = input("Update available. Update now? [y/N] ")
    return choice.lower().startswith("y")


def download_and_run(url: str):
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".exe")
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(tmp.name, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    subprocess.Popen([tmp.name], shell=True)


def launch_app():
    exe = Path(__file__).with_name("main.exe")
    if exe.exists():
        subprocess.Popen([str(exe)])
    else:
        subprocess.Popen([sys.executable, str(Path(__file__).with_name("main.py"))])


if __name__ == "__main__":
    url = check_update()
    if url and prompt_update():
        print("Downloading update...")
        download_and_run(url)
        sys.exit(0)
    launch_app()
