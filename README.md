# Abysmal Spore Backup Tool and Instance Manager
A baseline, functional, command line mod/save instance manager for Spore meant to be placed with the save data. Should work fine, though it's not thorougly tested. Meant to be used with the Mod API installed.

<img width="128" height="128" alt="image" src="https://github.com/user-attachments/assets/45b37a26-2315-4f4a-88d8-9e8cc6472ac0" />

### !!EXPERIMENTAL, USE THIS AT YOUR OWN RISK!!
This could potentially screw up the game files if set up wrong, and it could break at any time. I only made this because there wasn't a better one.

There was also a bug in development where it wouldn't copy things into the save directory properly, sometimes not deleting files either, which I have attempted to fix by placing the scripts INSIDE of the save directory. Until further testing can be done I feel like there's a small chance it could resurface in some form, though I'm unsure what it would do in particular. Please back up your files just in case.

## Requirements
This requires both the mod API and Python 3.13. I've only lightly tested this on windows on my own personal install of Spore, though I see no reason why it *shouldn't* work for anyone else?
I would recommend not using this without being clear on where your spore files are and having a backup though.

## Setup Instructions
0. PLEASE backup your Spore files before using this, just to be safe if something goes wrong.
1. Place these files INSIDE of the Spore Save directory. (Directly inside, not in a subfolder.) Originally this was meant to be able to be extracted anywhere, but I was having bizzare issues getting that to work. This is usually in Appdata/Roaming on windows.
2. Run Setup.bat or Setup.py to generate .bat files for ASBtool.py and ASImanager.py ("`Run ASBtool.bat`" and "`Run Instance Manager.bat`" respectively)
4. Generate a partial backup of your Spore files using `Run ASBtool.bat` (Example of which directories you need to use for this below, though it may not apply outside of the EA App.)
5. Run `Run Instance Manager.bat` as administrator to run the Instance Manager. It does not work properly if you don't.

At this point, you can just continue to run the instance manager through the .bat file, though I would recommend setting up a shortcut that runs it as administrator by default for ease of use.

## Spore Directories Example
<img width="515" height="99" alt="image" src="https://github.com/user-attachments/assets/78a0f3bf-eb1b-4011-ae9e-aa46e6c5c66c" />
