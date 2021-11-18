#!/usr/bin/env python

import os
import os.path
import sys
import glob
import subprocess
import time

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-g", "--game", type=str, help="the name of the game (e.g. 'Cyberpunk 2077')",
                    required=True)
parser.add_argument("-p", "--path", type=str,
                    help="the path with the install files (default: current dir)")
parser.add_argument("-o", "--output-path", type=str,
                    help="the path where games will be installed (default: ~/Games/Custom/game)")
parser.add_argument("-P", "--proton", type=str,
                    help=("the absolute path of the chosen proton bin (default: "
                          "/usr/share/steam/compatibilitytools.d/proton-ge-custom/proton). "
                          "THIS IS A WISE CHOICE IF YOU USE ARCH LINUX AND PROTON GE. "
                          "If you don't, add this parameter"))
parser.add_argument("-s", "--steam-compat-client-install-path", type=str,
                    help=("STEAM_COMPAT_CLIENT_INSTALL_PATH. Should be the same on most major "
                          "distros (default: ~/.local/share/Steam)"))
args = parser.parse_args()

game = args.game
path = os.getcwd() if args.path is None else os.path.abspath(args.path)
games_path = os.path.expanduser("~/Games/Custom") if args.output_path is None else os.path.abspath(args.output_path)

sccip = os.path.expanduser("~/.local/share/Steam") if args.steam_compat_client_install_path is None else \
        os.path.abspath(args.steam_compat_client_install_path)
protonbin = "/usr/share/steam/compatibilitytools.d/proton-ge-custom/proton" if args.proton is None else \
        os.path.abspath(args.proton)

for f in (sccip, protonbin):
    if not os.path.exists(f):
        raise FileNotFoundError(f)

gpath = f"{games_path}/{game}"

def checkyes(s: str, explicit: bool = False) -> bool:
    return s.strip() in (("y", "Y") if explicit else ("", "y", "Y"))

def bootstrap(game: str, path: str, games_path: str) -> bool:
    if not os.path.exists(path):
        raise FileNotFoundError(path)

    print("👋 Welcome to this thing. I'll guide you through this process.")

    if not os.path.exists(games_path):
        print(f"🤔 `{games_path}` doesn't exist. Should I create it for you? (Y/n): ", end="")

        if not checkyes(c := input()):
            print("😥 Okay, pick another directory then. Bye!")
            sys.exit()

        os.mkdir(games_path)
        print("✅ Done!")

    print("")
    print("👍 Here's a summary of what's gonna happen")
    print(f"* Installing `{game}` in `{gpath}` (to be created)")
    print(f"* Will be searching for install files in `{path}`")
    print("Is this good? (Y/n): ", end="")

    if not checkyes(c := input()):
        print("😥 Okay, come back when you change your mind.")
        sys.exit()

    print("")

    try:
        os.mkdir(gpath)
        print(f"✅ Created `{gpath}`!")
    except FileExistsError:
        if len(os.listdir(gpath)) == 0:
            print(f"✅ `{gpath}` exists but it's empty. Using it anyway.")
        else:
            print(f"😥 `{gpath}` exists and it's not empty. Is the game installed already? (y/N): ", end="")
            if not checkyes(c := input(), explicit=True):
                print("😥 Okay, either clean the directory up or pick a different one")
                sys.exit()
            else:
                print("✅ Okay. Skipping install!")
                print("")
                return True

    print("")
    return False

def install_game(game: str, path: str, games_path: str):
    g = glob.glob(f"{path}/*.exe")
    if len(g) != 1:
        if len(g) == 0:
            print(f"😥 No .exe files found in `{path}`!")
        else:
            print(f"😥 Multiple .exe files found in `{path}`, no idea which one to pick!")
        sys.exit()

    exe = os.path.abspath(g[0])
    print(f"🤔 found install file `{exe}`. Should I use it? (Y/n): ", end="")

    if not checkyes(c := input()):
        print("😥 As you wish. Bye!")
        sys.exit()

    print("")
    print("✅ In ten seconds I will start the install process.")
    print("This will output a fair amount of lines. If you see the GOG setup and ")
    print("you manage to go through it, once it's finished close everything. If ")
    print("you don't see any window or the setup fails, you'll need to do some ")
    print("reading on why. Good luck!")

    print("")
    print("Here it comes ...")
    print("")
    time.sleep(2)

    # subprocess.Popen doesn't work for some reason
    os.system(f"""
        STEAM_COMPAT_CLIENT_INSTALL_PATH="{sccip}" STEAM_COMPAT_DATA_PATH="{gpath}" \\
        {protonbin} run \\
        '{exe}'
        """)

    print("")
    print("✅ Now the install window should be showing up.")
    print("If it doesn't show up, press CTRL+C and answer 'n' to the next question.")
    print("")

    while True:
        try:
            print("😴 Press CTRL+C when the install process is over ...")
            time.sleep(5)
        except KeyboardInterrupt:
            print("")
            break

    print("🤔 Is the game installed? (Y/n): ", end="")
    if not checkyes(c := input()):
        print("😥 Try running the command yourself next time:")
        print(f"""
        STEAM_COMPAT_CLIENT_INSTALL_PATH="{sccip}" STEAM_COMPAT_DATA_PATH="{gpath}" \\
        {protonbin} run \\
        '{exe}'
        """)
        sys.exit()

    print("")

def create_launcher(game: str, path: str, games_path: str):
    env = {
        "STEAM_COMPAT_CLIENT_INSTALL_PATH": sccip,
        "STEAM_COMPAT_DATA_PATH": gpath,
    }

    print("🤔 Do you want to enable ray tracing? (Y/n): ", end="")
    if checkyes(c := input()):
        env["VKD3D_CONFIG"] = "dxr11"
    print("🤔 Do you want to enable DLSS? (Y/n): ", end="")
    if checkyes(c := input()):
        env["PROTON_ENABLE_NVAPI"] = "1"


    envflags=" ".join(f'{k}="{env[k]}"' for k in env)

    print("")

    ggpath = glob.glob(f"{gpath}/pfx/drive_c/GOG Games/*")[0]

    print("✅ Almost done. Now you need to figure out the main executable.")
    print("It should be in this path:")
    print(ggpath)
    print("")
    print("It might be in a subpath. Write below the path relative to it.")
    print("E.g. if it's right there and it's called game.exe just write ")
    print("game.exe. If it's in a subpath called foo/bar/game.exe, then")
    print("write foo/bar/game.exe.")
    print("")

    gexe = input('>> ')
    while not os.path.exists(f"{ggpath}/{gexe}"):
        print(gpath)
        print(f"😥 I can't find {gexe} there. Try again or CTRL+C")
        gexe = input('>> ')

    print("✅ found it! Do you want me to create a .desktop launcher? (Y/n): ", end="")
    if checkyes(c := input()):
        launcher_template = """
[Desktop Entry]
Encoding=UTF-8
Value=1.0
Type=Application
Name={game}
GenericName={game}
Comment={game}
{iconbit}
Exec=env {envflags} {protonbin} run {gexe}
Categories=Game;
Path={ggpath}
"""
        iconbit = "Icon="
        if not os.path.exists("/usr/bin/convert"):
            print("😥 You don't have imagemagick, I won't be able to create an icon!")
        else:
            if len(icolist := glob.glob(f"{ggpath}/goggame-*ico")) != 1:
                print("😥 Icon not found! Continuing without")
            else:
                # this bit converts the .ico to a set of PNGs and then gets the largest
                icofile = icolist[0]
                pngfile = icofile[:-4] + ".png"
                subprocess.call(["/usr/bin/convert", icofile, pngfile])

                pnglist = glob.glob(f"{ggpath}/goggame-*png")
                pngfile = None
                fs = 0
                for icon in pnglist:
                    if os.path.getsize(icon) > fs:
                        pngfile = icon

                iconbit = f"Icon={pngfile}"
            desktop_file = launcher_template.format(
                game=game,
                iconbit=iconbit,
                protonbin=protonbin,
                gexe=gexe,
                ggpath=ggpath,
                envflags=envflags
            )

            prettygame = game.replace(" ", "_")
            with open(os.path.expanduser(f"~/.local/share/applications/GOG_{prettygame}.desktop"), "w") as f:
                f.write(desktop_file)
            
            udd = "/usr/bin/update-desktop-database"
            if os.path.exists(udd):
                subprocess.call([udd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("✅ Done! Give it a couple of seconds and it will show up in your apps!")

    print("")
    print("Either way, to try it out and debug it, here's the command you should launch:")
    print("")

    print(f"""
        {envflags} \\
        {protonbin} \\
        run {gexe}
    """)

    print("")
    print("👋 Enjoy!")

skip_install = bootstrap(game, path, games_path)
if not skip_install:
    install_game(game, path, games_path)
create_launcher(game, path, games_path)

# print(game, path, games_path)
