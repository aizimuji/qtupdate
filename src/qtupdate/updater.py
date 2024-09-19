import requests
from packaging import version
import os
import sys
from qtupdate.version import __version__

GITHUB_REPO = "aizimuji/qtupdate"
VERSION_FILE_URL = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main/version.txt"
RELEASE_URL = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"


def get_current_version():
    return ".".join(map(str, __version__))


def check_for_updates():
    try:
        response = requests.get(VERSION_FILE_URL)
        latest_version = response.text.strip()
        current_version = get_current_version()

        if version.parse(latest_version) > version.parse(current_version):
            return True, latest_version
        return False, current_version
    except Exception as e:
        print(f"Error checking for updates: {e}")
        return False, get_current_version()


def download_update():
    try:
        response = requests.get(RELEASE_URL)
        release_data = response.json()
        asset_url = release_data["assets"][0]["browser_download_url"]

        response = requests.get(asset_url)
        with open("update.exe", "wb") as f:
            f.write(response.content)
        return True
    except Exception as e:
        print(f"Error downloading update: {e}")
        return False


def apply_update():
    if getattr(sys, "frozen", False):
        # Running as compiled exe
        current_exe = sys.executable
        update_exe = "update.exe"

        # Create a batch file to replace the current exe with the update
        with open("update.bat", "w") as f:
            f.write(
                f"""
@echo off
timeout /t 2 /nobreak > NUL
move /y "{update_exe}" "{current_exe}"
start "" "{current_exe}"
del "%~f0"
            """
            )

        # Run the batch file and exit the current process
        os.system("start update.bat")
        sys.exit()
    else:
        print("Update can only be applied to compiled exe")
