proton-gog-install
==================

A script to install a Windows game through GOG on Linux. Based on
[this gist](https://gist.github.com/myyc/4b57f9a5637362d37961a10cd32b8f0b).

Tested on Arch, might work elsewhere. Requirements:

* Imagemagick (lol)
* The install files of the game to be downloaded in a single folder.

If you're trying to install Cyberpunk 2077 make sure to use a helper to
download them or have fun clicking on over 9000 links.

Why this?
=========

You can use Gamehub or other things. The fact is ... it's a bit unreliable.
It's a great piece of software but sometimes it just doesn't work and it's
almost impossible to debug it for now. So this just installs your games,
always outputs what it does so that you can try the commands yourself with
your little hands.

How do I use it?
================

`$ python proton-gog-install.py`

It will guide you through some stuff.

The actual game setup part is trash because for some reason Wine exits
successfully even when it fails and most importantly it exists right
before you can see a window. If you know ways around this that aren't
some hack like "waiting for a certain directory to be populated" feel
free to submit a PR.

How do I keep games up to date?
===============================

Great question. In principle it should be enough to run the .exe with
the patch using the same parameters (`STEAM_COMPAT_CLIENT_INSTALL_PATH`
and `STEAM_COMPAT_DATA_PATH` mainly). Probably something like this:

```
$ cd /where/the/patch/files/are 
$ STEAM_COMPAT_CLIENT_INSTALL_PATH=/home/$USER/.local/share/Steam \
  STEAM_COMPAT_DATA_PATH="/home/$USER/Games/Custom/Your Game" \
  /usr/share/steam/compatibilitytools.d/proton-ge-custom/proton run \
  your_games_patch.exe
```

But hey, I've never tried it, so I guess you'll have to trust some
guy on the internet.
