# Imports
import pathlib
import shutil
import os

# Main program loop
def Main():
    # Quickly make sure the directories file exists so we don't error later
    try:
        with open("directories.txt", 'x') as file:
            file.write("")
    except FileExistsError:
        pass
    
    # Text Preamble thing
    print("------------------------------------------------------------------------")
    print("Welcome to the Abysmal Spore Backup tool. (0.1.1) - Save Folder Rework \nThis probably sucks, but oh well. I'm just going for functional here.")
    print("------------------------------------------------------------------------\n")
    print("This program will back up some files in your current spore installation that \nshould allow you to restore your saves and mods if needed.\n")
    print("Can theoretically be used to manually switch between different sets of mods, \nthough I do not reccomend this.\n")
    # Warning that this is experimental
    print("!!THIS PROGRAM IS EXPERIMENTAL!!")
    print("While this should be fine to back up files with, \nplease don't rely on it as your main method for doing this.")
    # Ask user if they want to back up their spore install
    print("\nWould you like to back up your current installation of Spore?")
    startup = input("(y = yes, n = no, d = clear set directories. i for info.)\n")
    if (startup == 'y'):
        # Backup function
        SporeBackup()
    elif (startup == 'd'):
        # Wipe Directories.txt
        dirs = open("directories.txt",'w')
        dirs.write("")
        dirs.close()
        scrap = input("Your set Spore directories have been cleared. Press enter to close.")
    elif (startup == 'i'):
        # Information block
        print("\n\"What is this?\" You might be wondering. \"What does it do?\"\n")
        print("The Abysmal Spore Backup tool (ASBtool) is an experimental tool I created \n"
              + "to test what would be needed to be able to set up different mod profiles, \n"
              + "which could be useful for modpacks for example. It's mostly a proof of \n"
              + "concept on its own, only creating a backup of what seem to be the nescessary\n"
              + "files for restoring your mods and saves with a fresh install of the \n"
              + "Spore Modding API, though it can be used in conjunction with the instance\n"
              + "tool to create a base instance. You can rerun this at any time to set a\n"
              + "different configuration as what's created when you make a new one.\n"
              + "Use this at your own risk. It sucks. I've not tested it vert thoroughly\n"
              + "as of writing, though I trust it enough that I don't expect it to break\n"
              + "with my particular use case.\n"
              + "If something breaks because of how you use this, you've been warned.\n\n")
        scrap = input ("(press enter to continue.)")
        Main()
    else:
        # Exit
        print("Goodbye!")
    # Check for if paths have already been set

# Code that runs to back up your spore directories
def SporeBackup():
    
    cwd = os.getcwd()
    backupdir = cwd + "/Backup/My Spore Creations"
    
    # Open directories file, set uninitialized directories
    dirs = open("directories.txt",'r')
    
    # If it is blank, prompt user to input directories
    if dirs.read() == '':
        print("You do not have your Spore directories set. Please set your spore directories.\n")
        dirs.close()
        dirs = open("directories.txt",'a')
        # Get My Spore Creations Path
        path = pathlib.Path(input("My Spore Creations Directory: \n"))
        mscpath = str(path).replace("\\","/")
        dirs.write(mscpath + "\n")
        # Get Spore Save Path (Outdated, from a version that could be in any arbitrary folder.)
        #path = pathlib.Path(input("Spore Save Directory: \n"))
        #savepath = str(path).replace("\\","/")
        #dirs.write(savepath + "\n")
        # Get Spore Data Path
        path = pathlib.Path(input("Spore Data Folder: \n"))
        datapath = str(path).replace("\\","/")
        dirs.write(datapath + "\n")
        # Get GA Data Path
        path = pathlib.Path(input("GA Data Folder: \n"))
        gadatapath = str(path).replace("\\","/")
        dirs.write(gadatapath + "\n")
        # Get ModAPI Path
        path = pathlib.Path(input("Spore Mod API install location: \n"))
        modapidatapath = str(path).replace("\\","/")
        dirs.write(modapidatapath + "\n")
        # Footer
        dirs.write("My Spore Creations - Spore Data - GA Data - Mod API folder")
        dirs.close()
        # Print out all of the directories to make sure the user didn't misinput anything.
        print(f"\nYour My Spore Creations folder is at \n{mscpath}\n")
        #print(f"Your Spore Save folder is at \n{savepath}\n")
        print(f"Your Spore Data folder is at \n{datapath}\n")
        print(f"Your GA Data folder is at \n{gadatapath}\n")
        print(f"Your Modding API folder is at \n{modapidatapath}\n")
        scrap = input("\nIf all looks correct, press enter, otherwise, please close the program \nand clear set directories the next time you open it.")
    else:
        dirs.close()
    # Get directories out of saved directories file.
    dirs2 = open("directories.txt",'r')
    msc = dirs2.readline()
    msc = msc.rstrip()
#    spore = dirs2.readline()
#    spore = spore.rstrip()
    sdata = dirs2.readline()
    sdata = sdata.rstrip()
    gadata = dirs2.readline()
    gadata = gadata.rstrip()
    modapi = dirs2.readline()
    modapi = modapi.rstrip()

    # This is just a debug check to make sure everything was in the right directories
    #print(msc + "\n" + spore + "\n" + sdata + "\n" + gadata + "\n" + modapi)
    #scrap = input("close program pls")
    
    # Delete the backup directory if it exists
    WipeBackup()
    # Backup the My Spore Creations folder
    CopyBackup(msc,backupdir)
    # Backup the Spore Save folder (Outdated)
    #backupdir = cwd + "/Backup/Spore"
    #CopyBackup(spore,backupdir)
    # Backup the Spore Data folder
    backupdir = cwd + "/Backup/Data"
    CopySData(sdata,backupdir)
    # Backup the GA Data folder
    backupdir = cwd + "/Backup/DataEP1"
    CopyGAData(gadata,backupdir)
    # Backup ModAPI data
    CopyModAPI(modapi)
    # Backup files in Save directory
    shutil.copytree(cwd+"/CityMusic",cwd+"/Backup/Save/CityMusic")
    shutil.copytree(cwd+"/Games",cwd+"/Backup/Save/Games")
    shutil.copytree(cwd+"/Preferences",cwd+"/Backup/Save/Preferences")
    # MVJCache and Temp don't seem nescessary.
    shutil.copy2(cwd+"/EditorSaves.package",cwd+"/Backup/Save/EditorSaves.package")
    shutil.copy2(cwd+"/Planets.package",cwd+"/Backup/Save/Planets.package")
    shutil.copy2(cwd+"/Pollination.package",cwd+"/Backup/Save/Pollination.package")
    

# Prompt user to close the program.
    scrap = input("Press Enter to exit.")

# Copy from Source to Destination
def CopyBackup(s,d):
    if not os.path.exists(d):
        if os.path.exists(s): 
            shutil.copytree(s, d)
        else:
            print("Invalid Path.")
    else:
        print("Already exists")

# Copy from Spore Data folder to Destination, ignores most vanilla files
def CopySData(s,d):
    if not os.path.exists(d):
        if os.path.exists(s): 
            shutil.copytree(s, d,ignore=shutil.ignore_patterns("Spore_Audio1.package", "Spore_Audio2.package", "Spore_Content.package", "Spore_Game.package", "Spore_Graphics.package", "Spore_Pack_03.package", "Locale", "version.txt", "properties.txt"))
        else:
            print("Invalid Path.")
    else:
        print("Already exists")

# Copy from GA Data folder to Destination, ignores most vanilla files
def CopyGAData(s,d):
    if not os.path.exists(d):
        if os.path.exists(s): 
            shutil.copytree(s, d,ignore=shutil.ignore_patterns("Spore_EP1_Locale_01.package", "Spore_EP1_Locale_02.package", "Spore_EP1_Content_01.package", "Spore_EP1_Content_02.package", "version.txt", "properties.txt", "Spore_EP1_Data.package"))
        else:
            print("Invalid Path.")
    else:
        print("Already exists")

# What will probably be the most obnoxious bit
# Copy seveal individual files from the Mod API folder
def CopyModAPI(source):
    
    # ModSettings Folder
    cwd = os.getcwd()
    d = cwd + "/Backup/ModAPI/ModSettings"
    s = source + "/ModSettings"
    if not os.path.exists(d):
        if os.path.exists(s):
            shutil.copytree(s, d)
        else:
            print("Invalid Path.")
    else:
        print("Already exists")

    # ModConfigs Folder
    d = cwd + "/Backup/ModAPI/ModConfigs"
    s = source + "/ModConfigs"
    if not os.path.exists(d):
        if os.path.exists(s):
            shutil.copytree(s, d)
        else:
            print("Invalid Path.")
    else:
        print("Already exists")
        
    # mLibs Folder
    d = cwd + "/Backup/ModAPI/mLibs"
    s = source + "/mLibs"
    if not os.path.exists(d):
        if os.path.exists(s):
            shutil.copytree(s, d,ignore=shutil.ignore_patterns("SporeModAPI.dll","SporeModAPI.lib"))
        else:
            print("Invalid Path.")
    else:
        print("Already exists")

    # Copy InstalledMods.config
    d = cwd + "/Backup/ModAPI/InstalledMods.config"
    s = source + "/InstalledMods.config"
    if not os.path.exists(d):
        if os.path.exists(s):
            shutil.copy2(s, d)
        else:
            print("Invalid Path.")
    else:
        print("Already exists")
        

# Wipe backup directory
def WipeBackup():
    cwd = os.getcwd()
    bdir = cwd + "/Backup"
    if os.path.exists(bdir):
        shutil.rmtree(bdir)
    else:
        print("Backup folder will be created.")
# Run main loop
Main()
