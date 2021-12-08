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

It will guide you through some stuff. When the setup is done you must
close the window. `Launch` will not launch your game and it'll look
like stuff is broken so don't do that.

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

Common problems
===============

A few things I've experienced using this myself on two machines.

## The icon is shit

Windows GOG games have an `.ico` file called `goggame-$GAME_ID.ico`,
which this script converts to the various sized icons in the same
directory, called `goggame-$GAME_ID-$n.png` where `n` is typicallly
1 to 6. Then it picks the "largest" one and uses that as your icon.

It might be that this isn't reliable for some reason so you can
edit (once and for all) the resulting
`~/.local/share/applications/GOG_$GAME.desktop` and replace the
icon path with a better one.

If none of the available icons satisfy you, well, the procedure
is the same.

## The game won't start

This is a pain in the ass and surpsisingly it happens more to older
than recent games (as long as the recent games are sort of
supported on Steam). On this you're generally on your own but there
are a few things to try out.

1. Debug it yourself: the script at the end gives you a commend to
   run. You should try that and see what happens.
2. If the game (or hardware) is old you might want to try your luck
   with vanilla `wine`.
3. Either way, you might need to do things like changing the
   Windows version, installing additional components etc., on `wine`
   this is done with
   `WINEPREFIX="/home/$USER/Games/Custom/Your Game" winetricks component`
   while on proton there's a thingy called `protontricks`. Google it.
   
Keep in mind that version changes and additional components persist
so once you manage to make it work copy your command into the `Exec`
field of the `~/.local/share/applications/GOG_$GAME.desktop` file.
You'll be using environment variables e.g. `WINEPREFIX` or
`STEAM_COMPAT_DATA_PATH` so don't forget `env` at the beginning
(e.g. `Exec=env FOO=bar blah`).
