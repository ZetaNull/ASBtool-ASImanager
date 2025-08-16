!!PLEASE EXTRACT THESE FILES INTO YOUR SPORE SAVE DIRECTORY IN ROAMING!!
These scripts are hardcoded to only function properly when placed INSIDE of the Spore folder in %Appdata%/Roaming, as it had issues when it was set to be used elsewhere. 
Please do not place them inside of a folder IN the Spore folder, place them directly in the Spore folder itself.

Use this at your own risk. If this damages your Spore files, I can't do much about it. Please be careful with this.

To set up the Backup Tool and Instance Manager, run Setup.bat or Setup.py. Please run ASBtool and ASImanager through the generated .bat files.

The Instance Manager has to be run as administrator in order to properly be able to switch instances, though it can create and delete instances fine otherwise.
I would recommend setting up a shortcut to run "Run Instance Manager.bat" as administrator

This is only tested on windows on my own personal install. It works with the EA App version of Spore and is inteded to be used with the Mod API Launcher Kit installed.
I'd assume it should work fine with other versions of Spore, I've just not tested that.

MORE DETAILED SETUP GUIDE (WINDOWS ONLY):
1. Run the "Setup.bat" file to generate the other .bat files.
2. Run the "Run ASBtool.bat" file and create a partial backup of the Spore Files. This should create a copy of most modded spore files, most save data, and the files 
   that the Mod API uses to track which mods are in use.
3. Run the "Run Instance Manager.bat" file as administrator to launch the actual Instance Manager. I would reccomend creating a full backup of your spore installation
   somewhere on the off chance something breaks before switching instances, though at this point you should be able to use it without issue.

While I feel like it's unlikely, if the Mod API's tracking structure were to ever change dramatically, this will break. So keep that in mind.

EXTRA NOTES:
- Whatever ASBtool's most recent backup is will be used by the Instance Manager to create new instances. If you want a cleaner install than that, run it again and create
a new backup using a cleaner instance. This will then be used as the base instance for any new instances unless you create a new backup.

- I'm unsure how leaving save folders empty would impact an instance when you try and switch to it, so probably don't do this? Just make sure to run Spore after deleting anything. It /should/ be fine. I still recommend keeping a backup somewhere though on the off chance you forget or something goes wrong.