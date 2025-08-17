# Imports
import os
import re
import pathlib
import shutil

# Constants
cwd = os.getcwd()
cwd = cwd.replace("\\","/")
# I had a lot of nice colors going, but they don't show if running as admin >:V
# On the off chance someone wants to use these for something, I've left the
# original colors commented out.
color_default = '' #"\033[0m"
color_green = '' #"\033[92m"
color_red = '' #"\033[31m"
color_yellow = '' #"\033[33m"
color_cyan = '' #"\033[36m"
color_blue = '' #"\033[34m"
color_active = '' #"\033[96m"

# Initial Program loop
def Main():
    # Create the directories.txt file if it does not exist
    try:
        with open("directories.txt", 'x') as file:
            file.write("")
    except FileExistsError:
        pass
    print(cwd)
    # Welcome blurb
    print(color_blue + "------------------------------------------------------------------------")
    print(color_green + "Welcome to the Abysmal Spore Instance Manager. \n(0.1.2) - Instance Swap Rework\n"
          + "Sorry this probably sucks, I don't have the budget for a GUI."
          + "\n\nPlease make sure to run as administrator to ensure files can be"
          + "\nmoved properly! This can be done by running Run Instance Manager.bat \n"
          + "as admin or creating a shortcut set to run it as Administrator.")
    print(color_blue + "------------------------------------------------------------------------\n\n"
          + color_red + "!!THIS PROGRAM IS EXPERIMENTAL!!\n"
          + color_yellow + "Please backup your files before using it!\n" + color_green)
    
    # Check for if the backup tool has been used yet or if the directories file is blank,
    # do not run if it hasn't.
    
    backupdir = cwd + "/Backup"
    dirs = open("directories.txt",'r')
    
    # Runs when no backup directory files are detected or the directory isnt set.
    if not os.path.exists(backupdir):
        print(color_cyan + "It appears as though you do not currently have a backup of your files.\n"
              + "Please run ASBtool.py and back up your Spore files.\n"+color_default)
        #scrap = input("Press Enter to exit.")
    elif dirs.read() == '':
        print(color_cyan + "It appears as though you do not currently have your Spore installation\n"
              + "directories set. Please run ASBtool.py and set them by making a backup.\n"+color_default)
        dirs.close()
        #scrap = input("Press Enter to exit.")
    else:
        dirs.close()
        # Ensure the Instances directory exists
        try:
            os.mkdir("Instances")
            print("You do not currently have any instances set up. Creating directory.")
            try:
                with open("Instances/active.txt", 'x') as file:
                    file.write("Default")
            except FileExistsError:
                pass
            os.mkdir("Instances/Default")
            os.mkdir("Instances/Instances.Backup")
        except FileExistsError:
            pass
        # Set up user input variable
        command = "Wow, you could put a swear word in this part and it would change nothing"
        while (command != "x"):
            # Print the instances and prompt user input
            PrintInstances()
            print(color_green + "\nWhat would you like to do?\n")
            command = input(color_cyan +"n = new instance, s = switch instance, d = delete instance, i = info, \n"
                            +"x = exit\n"+color_default)
            if command == "n":
                NewInstance()
            elif command == "s":
                SwitchInstance()
            elif command == "d":
                DelInstance()
            elif command == "i":
                print(color_blue+"\n------------------------------------------------------------------------")
                print(color_green+"Welcome to the Abysmal Spore Instance Manager. Please read the\n"
                      + "README.txt file to make sure that you set everything up correctly.\n"
                      + "(0.1.2) - Instance Swap Rework\n"
                      + color_blue+"------------------------------------------------------------------------"
                      + color_active+"\n\n  This is a mod instance manager I created for Spore because I \n"
                      + "needed one and nobody seemed to have made one prior to this.\n\n"
                      + "  I can't guarantee this will continue to work if Spore or the\n"
                      + "Modding API update-- though i don't see a reason it wouldnt-- so\n"
                      + "Please keep a backup of your files while using this, outside of\n"
                      + "What the ASBtool does (The backup it creates is trimmed down to\n"
                      + "only include files nescessary for instances as to not bloat the\n"
                      + "filesize unnescessarily.) just in case something happens to\n"
                      + "go wrong.\n\n"
                      + "  I'd reccomend not using this if anyone's made a better instance\n"
                      + "manager or whatever you'd call this, though it should be usable\n"
                      + "if nobody has yet. I cobbled this together as a command line\n"
                      + "python thing because it's basically all that I know how to write\n"
                      + "something from scratch in. Worse for the end user, though. No GUI.\n")
                scrap = input (color_cyan+"(Press enter to continue.)"+color_default)

# Command to print the list of Instances
def PrintInstances():
        print(color_blue +"------------------------------------------------------------------------")
        print(color_green +"Your current Spore instances are:")
        print(color_blue +"------------------------------------------------------------------------")
        # create a list of the instances in the instance directory
        instances = os.listdir(cwd+"/Instances")
        # Get the active Instance from active.txt
        activetxt = open("Instances/active.txt",'r')
        active = activetxt.readline()
        activetxt.close()
        # Print out the current instances
        for i in instances:
            if i != "active.txt" and i != "Instances.Backup":
                if i == active:
                    print(color_active +f"{i} <-- CURRENT")
                else:
                    print(color_cyan +f"{i}")
        print(color_blue + "------------------------------------------------------------------------")

# Script for creating a new instance
def NewInstance():
    print(color_green+"Do you wish to create a new instance? (y/n)")
    command = input(color_default)
    if command == "y" or command == "Y" or command == "yes" or command == "Yes":
        cont = "no"
        print(color_green+"What would you like to call your new instance? Only letters will be kept.")
        while (cont != "y"
               and cont != "Y"
               and cont != "yes"
               and cont != "Yes"):
            command = input(color_default)
            command = re.sub(r'[^a-zA-Z]', '', command)
            cont = input(color_green+f"You wish to call your instance \"{command}\"? (y/n)\n"+color_default)
            if os.path.exists(cwd + "/Instances/" + command):
                print(color_yellow+"\nAn instance with that name already exists!\n")
                cont = "error"
            if (cont != "y"
                and cont != "Y"
                and cont != "yes"
                and cont != "Yes"):
                print(color_green+"What would you like to call your new instance?")
        print(color_cyan+"Creating Instance...\n")
        GenInstance(command)
        print(color_green+f"Instance \"{command}\" has been created.\n")

# Script for deleting an instance. New to 0.1.1. Not that 0.1.0 was public (it was broken)
def DelInstance():
    print(color_green+"Do you wish to delete an instance? (y/n)")
    command = input(color_default)
    if command == "y" or command == "Y" or command == "yes" or command == "Yes":
        activetxt = open("Instances/active.txt",'r')
        active = activetxt.readline()
        activetxt.close()
        print("Which instance do you want to delete?")
        command = input()
        # Only include letters
        command = re.sub(r'[^a-zA-Z]', '', command)
        if command == active:
            print(f"{active} is your active instance! \nSwitch to a different one before deleting it.")
        elif os.path.exists(cwd + "/Instances/" + command) and command != '':
            command2 = input(f"Really delete {command}!? (y/n)\n")
            if command2 == "y" or command2 == "Y" or command2 == "yes" or command2 == "Yes":
                print(f"Deleting {command}!")
                WipeFolder(cwd + "/Instances/" + command)
                print(f"{command} deleted.")
        else:
            print(f"{command} isn't an instance!")
        
# Script for switching between instances
def SwitchInstance():
    print(color_yellow + "!! MAKE SURE SPORE AND THE MOD API ARE CLOSED WHILE YOU DO THIS !!\n"
        + color_green+ "Do you wish to switch your active instance? (y/n)")
    command = input(color_default)
    if command == "y" or command == "Y" or command == "yes" or command == "Yes":
        activetxt = open("Instances/active.txt",'r')
        active = activetxt.readline()
        activetxt.close()
        cont = "true"
        # Get the instance to switch to
        while (cont == "true"):
            print(color_green+"Which instance would you like to switch to?")
            command = input(color_default)
            command = re.sub(r'[^a-zA-Z]', '', command)
            if command == active:
                print("This is your active instance.")
                PrintInstances()
            elif os.path.exists(cwd + "/Instances/" + command) and command != '':
                cont = "false"
            else:
                print("Instance does not exist.")
                PrintInstances()
        # Set aside all of the spore directories to use later
        dirs2 = open("directories.txt",'r')
        msc = dirs2.readline()
        msc = msc.rstrip()
        sdata = dirs2.readline()
        sdata = sdata.rstrip()
        gadata = dirs2.readline()
        gadata = gadata.rstrip()
        modapi = dirs2.readline()
        modapi = modapi.rstrip()
        dirs2.close()

        # Prompt user to ask if they want to back up their spore files.
        print("Would you like to back up your Spore files before proceeding? (y/n)")
        backupcheck = input()
        if backupcheck == "y" or backupcheck == "Y" or backupcheck == "yes" or backupcheck == "Yes":
            
            # Reworked code from the backup tool lol
            print(color_cyan+"\nCreating backup...\n")
            WipeFolder(cwd + "/Instances/Instances.Backup")

            # My Spore Creations
            backupdir = cwd + "/Instances/Instances.Backup/My Spore Creations"
            CopyFolder(msc,backupdir)

            # Backup the Spore Data folder
            backupdir = cwd + "/Instances/Instances.Backup/Data"
            CopySData(sdata,backupdir)
            
            # Backup the GA Data folder
            backupdir = cwd + "/Instances/Instances.Backup/DataEP1"
            CopyGAData(gadata,backupdir)
            
            # Backup ModAPI data
            backupdir = cwd + "/Instances/Instances.Backup/ModAPI"
            CopyModAPI(modapi,backupdir)

            # Backup Spore Save
            shutil.copytree(cwd+"/CityMusic",cwd+"/Instances/Instances.Backup/Save/CityMusic")
            shutil.copytree(cwd+"/Games",cwd+"/Instances/Instances.Backup/Save/Games")
            shutil.copytree(cwd+"/Preferences",cwd+"/Instances/Instances.Backup/Save/Preferences")
            # MVJCache and Temp don't seem nescessary.
            shutil.copy2(cwd+"/EditorSaves.package",cwd+"/Instances/Instances.Backup/Save/EditorSaves.package")
            shutil.copy2(cwd+"/Planets.package",cwd+"/Instances/Instances.Backup/Save/Planets.package")
            shutil.copy2(cwd+"/Pollination.package",cwd+"/Instances/Instances.Backup/Save/Pollination.package")

            print(color_cyan+"\nBackup Created.\n(Press enter to continue.)")
            scrap = input()

        # Move Spore Files to currently "Active" instance
        print("Archiving active instance files...")
        
        # My Spore Creations
        movedir = cwd + "/Instances/" + active + "/My Spore Creations"
        MoveFolderContent(msc,movedir)
        print("Archived My Spore Creations. (1/5)")

        # Spore Data Folder
        movedir = cwd + "/Instances/" + active + "/Data"
        MoveSdataContent(sdata,movedir)
        print("Archived Spore Data files. (2/5)")

        # GA Data Folder
        movedir = cwd + "/Instances/" + active + "/DataEP1"
        MoveGAdataContent(gadata,movedir)
        print("Archived GA Data files. (3/5)")

        # ModAPI Files
        movedir = cwd + "/Instances/" + active + "/ModAPI"
        MoveModAPIContent(modapi,movedir)
        print("Archived Mod API files. (4/5)")

        # Spore Save Files
        try:
            os.mkdir(cwd+"/Instances/"+active)
        except FileExistsError:
            pass
        try:
            shutil.move(cwd+"/CityMusic",cwd+"/Instances/"+active+"/Save/CityMusic")
        except FileNotFoundError:
            pass
        try:
            shutil.move(cwd+"/Games",cwd+"/Instances/"+active+"/Save/Games")
        except FileNotFoundError:
            pass
        try:
            shutil.move(cwd+"/Preferences",cwd+"/Instances/"+active+"/Save/Preferences")
        except FileNotFoundError:
            pass
        # MVJCache and Temp don't seem nescessary.
        try:
            shutil.move(cwd+"/EditorSaves.package",cwd+"/Instances/"+active+"/Save/EditorSaves.package")
        except FileNotFoundError:
            pass
        try:
            shutil.move(cwd+"/Planets.package",cwd+"/Instances/"+active+"/Save/Planets.package")
        except FileNotFoundError:
            pass
        try:
            shutil.move(cwd+"/Pollination.package",cwd+"/Instances/"+active+"/Save/Pollination.package")
        except FileNotFoundError:
            pass
        print("Archived Spore Save files. (5/5)")
        
        # Move "activating" instance files to Spore directories
        print(f"Unarchiving {command} Instance...")
        
        # My Spore Creations
        movedir = cwd + "/Instances/" + command + "/My Spore Creations"
        MoveFolderContent(movedir,msc)
        print("Unarchived My Spore Creations. (1/5)")
        
        # Spore Data Folder
        movedir = cwd + "/Instances/" + command + "/Data"
        MoveSdataContent(movedir,sdata)
        print("Unarchived Spore Data files. (2/5)")

        # GA Data Folder
        movedir = cwd + "/Instances/" + command + "/DataEP1"
        MoveGAdataContent(movedir,gadata)
        print("Unarchived GA Data files. (3/5)")

        # ModAPI Files
        movedir = cwd + "/Instances/" + command + "/ModAPI"
        MoveModAPIContent(movedir,modapi)
        print("Unarchived Mod API files. (4/5)")

        # Spore Save Files
        try:
            shutil.move(cwd+"/Instances/"+command+"/Save/CityMusic",cwd+"/CityMusic")
        except FileNotFoundError:
            pass
        try:
            shutil.move(cwd+"/Instances/"+command+"/Save/Games",cwd+"/Games")
        except FileNotFoundError:
            pass
        try:
            shutil.move(cwd+"/Instances/"+command+"/Save/Preferences",cwd+"/Preferences")
        except FileNotFoundError:
            pass
        # MVJCache and Temp don't seem nescessary.
        try:
            shutil.move(cwd+"/Instances/"+command+"/Save/EditorSaves.package",cwd+"/EditorSaves.package")
        except FileNotFoundError:
            pass
        try:
            shutil.move(cwd+"/Instances/"+command+"/Save/Planets.package",cwd+"/Planets.package")
        except FileNotFoundError:
            pass
        try:
            shutil.move(cwd+"/Instances/"+command+"/Save/Pollination.package",cwd+"/Pollination.package")
        except FileNotFoundError:
            pass
        print("Unarchived Spore Save files. (5/5)")

        # Finally, now that ALL OF THIS is done, switch the active directory file.
        activetxt = open("Instances/active.txt", 'w')
        activetxt.write(command)
        activetxt.close
        scrap = input(color_green+"Active Spore instance swapped, press enter to continue.\n"+color_default)

# Instance Swapping Related Funcitons
        
# Script to move the full contents of a folder
def MoveFolderContent(src,dst):
    try:
        os.mkdir(dst)
    except FileExistsError:
        pass
    srcdir = os.listdir(src)
    for i in srcdir:
            # Move current file or folder.
            print(f"Moving {i} from \n{src} to \n{dst}")
            copysrc = src + '/' + i
            copydst = dst + '/' + i
            shutil.move(copysrc,copydst)

# Script to move files in the Spore Data folder, ignores most vanilla files
def MoveSdataContent(src,dst):
    try:
        os.mkdir(dst)
    except FileExistsError:
        pass
    srcdir = os.listdir(src)
    for i in srcdir:
        if not(i == "Spore_Audio1.package"
                or i == "Spore_Audio2.package"
                or i == "Spore_Content.package"
                or i == "Spore_Game.package"
                or i == "Spore_Graphics.package"
                or i == "Spore_Pack_03.package"
                or i == "Locale"
                or i == "version.txt"
                or i == "properties.txt"
                or i == "Config"):
            # Move current file or folder.
            print(f"Moving {i} from \n{src} to \n{dst}")
            copysrc = src + '/' + i
            copydst = dst + '/' + i
            shutil.move(copysrc,copydst)
        else:
            # Print message when file or folder is skipped.
            print(f"{i} Skipped")

# Script to move files in the GA Data folder, ignores most vanilla files
def MoveGAdataContent(src,dst):
    try:
        os.mkdir(dst)
    except FileExistsError:
        pass
    srcdir = os.listdir(src)
    for i in srcdir:
        if not(i == "Spore_EP1_Locale_01.package"
                or i == "Spore_EP1_Locale_02.package"
                or i == "Spore_EP1_Content_01.package"
                or i == "Spore_EP1_Content_02.package"
                or i == "Spore_EP1_Data.package"
                or i == "version.txt"
                or i == "properties.txt"
                or i == "Config"):
            # Move current file or folder.
            print(f"Moving {i} from \n{src} to \n{dst}")
            copysrc = src + '/' + i
            copydst = dst + '/' + i
            shutil.move(copysrc,copydst)
        else:
            # Print message when file or folder is skipped.
            print(f"{i} Skipped")

# Script to move ModAPI files
def MoveModAPIContent(source,dest):
    try:
        os.mkdir(dest)
    except FileExistsError:
        pass
    # ModSettings Folder
    d = dest + "/ModSettings"
    s = source + "/ModSettings"
    try:
        os.mkdir(d)
    except FileExistsError:
        pass
    shutil.move(s,d)
    
    # ModConfigs Folder
    d = dest + "/ModConfigs"
    s = source + "/ModConfigs"
    try:
        os.mkdir(d)
    except FileExistsError:
        pass
    shutil.move(s,d)
    
    # mLibs Folder
    d = dest + "/mLibs"
    s = source + "/mLibs"
    try:
        os.mkdir(d)
    except FileExistsError:
        pass
    srcdir = os.listdir(s)
    for i in srcdir:
        if not(i == "SporeModAPI.dll"
               or i == "SporeModAPI.lib"):
            # Move current file or folder.
            copysrc = s + '/' + i
            copydst = d + '/' + i
            shutil.move(copysrc,copydst)
        else:
            pass
    
    # InstalledMods.config
    d = dest + "/InstalledMods.config"
    s = source + "/InstalledMods.config"
    shutil.move(s,d)

# Old Script for switching between instances. Unreferenced.
# Used Copy/Delete a bunch instead of a move function.
def SwitchInstanceOld():
    print(color_yellow + "!! MAKE SURE SPORE AND THE MOD API ARE CLOSED WHILE YOU DO THIS !!\n"
        + color_green+ "Do you wish to switch your active instance? (y/n)")
    command = input(color_default)
    if command == "y" or command == "Y" or command == "yes" or command == "Yes":
        activetxt = open("Instances/active.txt",'r')
        active = activetxt.readline()
        activetxt.close()
        cont = "true"
        # Get the instance to switch to
        while (cont == "true"):
            print(color_green+"Which instance would you like to switch to?")
            command = input(color_default)
            command = re.sub(r'[^a-zA-Z]', '', command)
            if command == active:
                print("This is your active instance.")
                PrintInstances()
            elif os.path.exists(cwd + "/Instances/" + command) and command != '':
                cont = "false"
            else:
                print("Instance does not exist.")
                PrintInstances()
        # Set aside all of the spore directories to use later
        dirs2 = open("directories.txt",'r')
        msc = dirs2.readline()
        msc = msc.rstrip()
        #sav = dirs2.readline()
        #sav = sav.rstrip()
        sdata = dirs2.readline()
        sdata = sdata.rstrip()
        gadata = dirs2.readline()
        gadata = gadata.rstrip()
        modapi = dirs2.readline()
        modapi = modapi.rstrip()
        dirs2.close()
        
        # Copy active folder to instance backup
        print(color_cyan+"\nCreating backup...\n")
        WipeFolder(cwd + "/Instances/Instances.Backup")
        CopyFolder(cwd + "/Instances/" + active, cwd + "/Instances/Instances.Backup")
        
        # Copy spore files to active folder
        print(color_cyan+"Moving game files...\n")
        WipeFolder(cwd + "/Instances/" + active)
        # the following code is mostly copied from the ABStool, with some tweaks.
        
        # Backup the My Spore Creations folder
        backupdir = cwd + "/Instances/" + active + "/My Spore Creations"
        CopyFolder(msc,backupdir)
        
        # Backup the Spore Save folder
        backupdir = cwd + "/Instances/" + active + "/Save"
        # Folders
        shutil.copytree(cwd+"/CityMusic", backupdir+"/CityMusic")
        shutil.copytree(cwd+"/Games", backupdir+"/Games")
        shutil.copytree(cwd+"/Preferences", backupdir+"/Preferences")
        # Individual files now
        shutil.copy2(cwd+"/EditorSaves.package", backupdir+"/EditorSaves.package")
        shutil.copy2(cwd+"/Planets.package", backupdir+"/Planets.package")
        shutil.copy2(cwd+"/Pollination.package", backupdir+"/Pollination.package")

        # Backup the Spore Data folder
        backupdir = cwd + "/Instances/" + active + "/Data"
        CopySData(sdata,backupdir)
        # Backup the GA Data folder
        backupdir = cwd + "/Instances/" + active + "/DataEP1"
        CopyGAData(gadata,backupdir)
        # Backup ModAPI data
        backupdir = cwd + "/Instances/" + active + "/ModAPI"
        CopyModAPI(modapi,backupdir)

        # This part TERRIFIES ME. we're /deleting/ the spore files
        # to import the ones from the new instance.
        print(color_cyan+"Changing active instance...\n")
        # I absolutely HATE HATE HATE doing this but it's the only
        # way I can think to do this.
        
        # Start with replacing the Data folders, these are generally
        # in a protected directory and I want to catch permission errors 
        # without already having replaced half of the damn files so if 
        # something happens to go wrong.
        print(color_blue+"Swapping Spore Data folder...")
        DelSData(sdata)
        backupdir = cwd + "/Instances/" + command + "/Data"
        CopySData(backupdir,sdata)
        print(color_cyan+"Spore Data Swapped.")
        # Repeat previous step, but with GA files
        print(color_blue+"Swapping GA Data folder...")
        DelGAData(gadata)
        backupdir = cwd + "/Instances/" + command + "/DataEP1"
        CopyGAData(backupdir,gadata)
        print(color_cyan+"GA Data Swapped.")
        # Run the script for replacing the ModAPI files
        print(color_blue+"Swapping ModAPI files...")
        DelModAPI(modapi)
        backupdir = cwd + "/Instances/" + command + "/ModAPI"
        CopyModAPI(backupdir,modapi)
        print(color_cyan+"Mod API files swapped.")
        
        # Now that anything that might trip admin access is done, copy the other two things.
        print(color_blue+"Swapping Remaining My Spore Creations folder...")
        # My Spore Creations folder
        WipeFolder(msc)
        backupdir = cwd + "/Instances/" + command + "/My Spore Creations"
        CopyFolder(backupdir,msc)
        print(color_cyan+"My Spore Creations Swapped.")
        # This was the original attempt at switching the save data. for some fucking reason this caused problems.
        #scrap = input("about to wipe save data")
        #WipeFolder(sav)
        #scrap = input("Folder wiped")
        #backupdir = cwd + "/Instances/" + command + "/Spore"
        #scrap = input("Copying folder contents")
        #CopyFolder(backupdir,sav)
        #scrap = input("Folder copied")
        #print(color_cyan+"Spore Save Data Swapped. (2/2)")

        # ACTUALLY save data swap routine. PRAYING THAT THIS ACTUALLY FUCKING WORKS.
        print("Swapping Save Data... (0/6)")
        # not a chance in hell we need this but i'm trying to avoid save data problems so we're doing this to be safe.
        cwd2 = os.getcwd()
        cwd2 = cwd.replace("\\","/")
        swapdir = cwd + "/Instances/" + command + "/Save"

        # CityMusic Folder
        if os.path.exists(cwd2+"/CityMusic"):
            shutil.rmtree(cwd2+"/CityMusic")
        else:
            print("CityMusic Does Not Exist?")
        shutil.copytree(swapdir+"/Citymusic",cwd2+"/CityMusic")
        print("Swapping Save Data... (1/6)")

        # Games Folder
        if os.path.exists(cwd2+"/Games"):
            shutil.rmtree(cwd2+"/Games")
        else:
            print("Games Does Not Exist?")
        shutil.copytree(swapdir+"/Games",cwd2+"/Games")
        print("Swapping Save Data... (2/6)")

        # Preferences Folder
        if os.path.exists(cwd2+"/Preferences"):
            shutil.rmtree(cwd2+"/Preferences")
        else:
            print("Preferences Does Not Exist?")
        shutil.copytree(swapdir+"/Preferences",cwd2+"/Preferences")
        print("Swapping Save Data... (3/6)")

        # EditorSaves
        if os.path.exists(cwd2+"/EditorSaves.package"):
            os.remove(cwd2+"/EditorSaves.package")
        else:
            print("EditorSaves.package Does Not Exist?")
        shutil.copy2(swapdir+"/EditorSaves.package",cwd2+"/EditorSaves.package")
        print("Swapping Save Data... (4/6)")

        # Planets
        if os.path.exists(cwd2+"/Planets.package"):
            os.remove(cwd2+"/Planets.package")
        else:
            print("Planets.package Does Not Exist?")
        shutil.copy2(swapdir+"/Planets.package",cwd2+"/Planets.package")
        print("Swapping Save Data... (5/6)")

        # Pollination
        if os.path.exists(cwd2+"/Pollination.package"):
            os.remove(cwd2+"/Pollination.package")
        else:
            print("Pollination.package Does Not Exist?")
        shutil.copy2(swapdir+"/Pollination.package",cwd2+"/Pollination.package")
        print("Swapping Save Data... (6/6)")
        
        # Finally, now that ALL OF THIS is done, switch the active directory file.
        activetxt = open("Instances/active.txt", 'w')
        activetxt.write(command)
        activetxt.close
        scrap = input(color_green+"Active Spore instance swapped, press enter to continue.\n"+color_default)

# General functions, some of these are old and unused

# Copy Spore Save
def CopySav(src,sav):
    copydir = os.listdir(src)
    for i in copydir:
        if (os.path.isfile(sav + '/' + i)):
            # Copy code for a file
            print(src + '/' + i + " COPY FILE TO \n" + sav + '/' + i)
            copysrc = src + '/' + i
            copysav = sav + '/' + i
            shutil.copy2(copysrc,copysav)
        else:
            # Copy code for a folder
            print(src + '/' + i + " COPY FOLDER TO\n" + sav + '/' + i)
            copysrc = src + '/' + i
            copysav = sav + '/' + i
            shutil.copytree(copysrc,copysav)
            
# Wipe Spore Save
def WipeSav(sav):
    deldir = os.listdir(sav)
    for i in deldir:
        if (os.path.isfile(sav + '/' + i)):
            # Delete code for a file
            print(sav + '/' + i + " IS A FILE")
            #os.remove(wdir + '/' + i)
        else:
            # Delete code for a folder
            print(sav + '/' + i + " IS A FOLDER")
            #shutil.rmtree(sav + '/' + i)
# Copy from Source to Destination
def CopyFolder(s,d):
    if not os.path.exists(d):
        if os.path.exists(s): 
            shutil.copytree(s, d)
        else:
            print(color_red+"Invalid Path.")
    else:
        print(color_red+"Already exists")

# Wipe a given folder
def WipeFolder(bdir):
    if os.path.exists(bdir):
        shutil.rmtree(bdir)
    else:
        pass

# Copy from Spore Data folder to Destination, ignores most vanilla files
def CopySData(s,d):
    #if not os.path.exists(d):
        if os.path.exists(s): 
            shutil.copytree(s, d, dirs_exist_ok=True, ignore=shutil.ignore_patterns("Config","Spore_Audio1.package", "Spore_Audio2.package", "Spore_Content.package", "Spore_Game.package", "Spore_Graphics.package", "Spore_Pack_03.package", "Locale", "version.txt", "properties.txt"))
        else:
            print(color_red+"Invalid Path.")
    #else:
    #    print("Already exists")

# Delte from Spore Data folder, ignores most vanilla files
def DelSData(wdir):
    # Get the list of files in the wdir directory
    deldir = os.listdir(wdir)
    for i in deldir:
        # ignore ALL OF THESE FILES
        if not (i == "Spore_Audio1.package"
                or i == "Spore_Audio2.package"
                or i == "Spore_Content.package"
                or i == "Spore_Game.package"
                or i == "Spore_Graphics.package"
                or i == "Spore_Pack_03.package"
                or i == "Locale"
                or i == "version.txt"
                or i == "properties.txt"
                or i == "Config"):
            # Check if this is a directory or a file
            if (os.path.isfile(wdir + '/' + i)):
                # Delete code for a file
                os.remove(wdir + '/' + i)
            else:
                # Delete code for a folder
                shutil.rmtree(wdir + '/' + i)
        else:
            print(color_blue+f"Skip {i}")

# Copy from GA Data folder to Destination, ignores most vanilla files
def CopyGAData(s,d):
#    if not os.path.exists(d):
        if os.path.exists(s): 
            shutil.copytree(s, d, dirs_exist_ok=True, ignore=shutil.ignore_patterns("Config","Spore_EP1_Locale_01.package", "Spore_EP1_Locale_02.package", "Spore_EP1_Content_01.package", "Spore_EP1_Content_02.package", "version.txt", "properties.txt", "Spore_EP1_Data.package"))
        else:
            print(color_red+"Invalid Path.")
#    else:
#        print("Already exists")

# Delte from Spore Data folder, ignores most vanilla files
def DelGAData(wdir):
    # Get the list of files in the wdir directory
    deldir = os.listdir(wdir)
    for i in deldir:
        # ignore ALL OF THESE FILES
        if not (i == "Spore_EP1_Locale_01.package"
                or i == "Spore_EP1_Locale_02.package"
                or i == "Spore_EP1_Content_01.package"
                or i == "Spore_EP1_Content_02.package"
                or i == "Spore_EP1_Data.package"
                or i == "version.txt"
                or i == "properties.txt"
                or i == "Config"):
            # Check if this is a directory or a file
            if (os.path.isfile(wdir + '/' + i)):
                # Delete code for a file
                os.remove(wdir + '/' + i)
            else:
                # Delete code for a folder
                shutil.rmtree(wdir + '/' + i)
        else:
            print(color_blue+f"Skip {i}")

# Copy seveal individual files from the Mod API folder
# Edited from the original version to be less hardcoded
def CopyModAPI(source,dest):
    
    # ModSettings Folder
    d = dest + "/ModSettings"
    s = source + "/ModSettings"
    if not os.path.exists(d):
        if os.path.exists(s):
            shutil.copytree(s, d)
        else:
            print(color_red+"Invalid Path.")
    else:
        print(color_red+"Already exists")

    # ModConfigs Folder
    d = dest + "/ModConfigs"
    s = source + "/ModConfigs"
    if not os.path.exists(d):
        if os.path.exists(s):
            shutil.copytree(s, d)
        else:
            print(color_red+"Invalid Path.")
    else:
        print(color_red+"Already exists")
        
    # mLibs Folder
    d = dest + "/mLibs"
    s = source + "/mLibs"
    #if not os.path.exists(d):
    if os.path.exists(s):
        shutil.copytree(s, d, dirs_exist_ok=True, ignore=shutil.ignore_patterns("SporeModAPI.dll","SporeModAPI.lib"))
    else:
            print(color_red+"Invalid Path.")
    #else:
    #    print("Already exists")

    # Copy InstalledMods.config
    d = dest + "/InstalledMods.config"
    s = source + "/InstalledMods.config"
    if not os.path.exists(d):
        if os.path.exists(s):
            shutil.copy2(s, d)
        else:
            print("Invalid Path.")
    else:
        print("Already exists")

# Deletes the ModAPI files that need to be deleted
def DelModAPI(apidir):
    # Wipe ModSettings folder
    wdir = apidir + "/ModSettings"
    WipeFolder(wdir)
    # Wipe ModConfigs folder
    wdir = apidir + "/ModConfigs"
    WipeFolder(wdir)
    # Deal with mLibs folder
    wdir = apidir + "/mLibs"
    deldir = os.listdir(wdir)
    for i in deldir:
        # ignore ALL OF THESE FILES
        if not (i == "SporeModAPI.dll"
                or i == "SporeModAPI.lib"):
            # Check if this is a directory or a file
            if (os.path.isfile(wdir + '/' + i)):
                # Delete code for a file
                os.remove(wdir + '/' + i)
            else:
                # Delete code for a folder
                shutil.rmtree(wdir + '/' + i)
        else:
            print(color_blue+f"Skip {i}")
    # Delete InstalledMods.config
    wdir = apidir + "/InstalledMods.config"
    os.remove(wdir)

# Generate instance by copying backup
def GenInstance(name):
    bdir = cwd + "/Backup"
    ddir = cwd + "/Instances/" + name
    if not os.path.exists(ddir):
        shutil.copytree(bdir, ddir)
    else:
        print(color_red+"error.")

# Run main loop
Main()
