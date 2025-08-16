import os

# Small script to generate the ASImanager bat file
file = open("Run Instance Manager.bat", 'w') 
file.write("cd "+os.getcwd()+"\npython ASImanager.py\npause")

file2 = open("Run ASBtool.bat", 'w') 
file2.write("cd "+os.getcwd()+"\npython ASBtool.py")
