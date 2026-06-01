import cx_Freeze
from packages.Startup.Version import VERSION, RELEASE_SUFFIX
import sys
from pathlib import Path

FINAL_VERSION = f"{VERSION}{RELEASE_SUFFIX}"

icon_suffix = ".png"
program_suffix = ""
if sys.platform == "win32":
    system = "Windows64"
    program_suffix = ".exe"
    icon_suffix = ".ico"
elif sys.platform == "linux":
    system = "Linux"
else:
    system = "Other Systems"

include_files = [
    [
        "Resources/Languages/iso639_language_list.json",
        "Resources/Languages/iso639_language_list.json",
    ],
    ["Resources/Icons/", "Resources/Icons/"],
    ["Resources/Fonts/OpenSans.ttf", "Resources/Fonts/OpenSans.ttf"],
]

for tool in ["mkvmerge", "mkvpropedit"]:
    src = f"Resources/Tools/{system}/{tool}{program_suffix}"
    dst = f"Resources/Tools/{system}/{tool}{program_suffix}"
    lib = f"Resources/Tools/{system}/lib"
    lib_dst = f"Resources/Tools/{system}/lib"
    if Path(src).resolve().exists():
        include_files.append([src, dst])
    if Path(lib).resolve().exists():
        include_files.append([lib, lib_dst])

build_exe_options = {
    "include_files": include_files,
    "zip_include_packages": ["PySide6", "comtypes"],
    "optimize": 2,
}

cx_Freeze.setup(
    name="mkv-muxing-batch-gui",
    version=FINAL_VERSION,
    description="Batch gui program to mux mkv files",
    options={
        "build_exe": build_exe_options,
    },
    executables=[
        {
            "script": "main.py",
            "base": "gui",
            "icon": f"Resources/Icons/App{icon_suffix}",
            "copyright": "Copyright (c) Khaoklong51",
            "target_name": "mkv-muxing-batch-gui",
        }
    ],
)
