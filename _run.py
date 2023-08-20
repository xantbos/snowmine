import os, subprocess, sys, shutil, json, random, time

headertext = "Snowbreak Decryptor AIO"

os.system("title " + headertext)

total_time = 0

def find_good_aes_key(keys):
        
    for key in keys:
        print(f"Trying key {key}...")
        encoded_key = bytes(key, 'utf-8')
        res = subprocess.run([
        r"quickbms\quickbms_4gb_files.exe",
        "-C",
        "-Y",
        "-o",
        "-Q",
        "-0",
        "-F",
        "{}.pak",
        "-a",
        encoded_key,
        r"quickbms\unreal_tournament_4_0.4.27e_snowbreak.bms",
        fr"D:\Snow\data\game\Game\Content\Paks\App_Engine-WindowsNoEditor.pak",
        r"X:\python\snow\decrypted",
        ], capture_output=True)

        if res.returncode == 0:
            return key
            break
    return 0

# ----AES----
start = time.time()
print("Generating AES key values...")
if os.path.exists(r"X:\python\snow\AES.Key.Finder\Game"): shutil.rmtree(r"X:\python\snow\AES.Key.Finder\Game")
subprocess.run([r"X:\python\snow\AES.Key.Finder\RUN Find 256-bit UE4 AES Key.bat"],stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)

keys=[]

for (dir_path, dir_names, file_names) in os.walk(r"X:\python\snow\AES.Key.Finder\Game"):
    for file in file_names:
        print(f"Potential Key found: {file}")
        keys.append(file)
        
key = find_good_aes_key(keys)

if key == 0:
    print("Good key not found. RIN RU TIME BBY")
    input("Press any key to terminate script...")
    sys.exit()
    
else: print(f"Good AES key found: {key}")
end = time.time()
total_time += (end - start)
print(f"AES portion completed in {str(end - start)} seconds.")

# ----FOLDERS----
start = time.time()
print("Generating working folders...")
if os.path.exists("decrypted"): 
    print("Deleting old decrypted folder and subdirectories...")
    shutil.rmtree(r"X:\python\snow\decrypted")
    os.makedirs("decrypted")
if not os.path.exists("extracted"): os.makedirs("extracted")
end = time.time()
total_time += (end - start)
print(f"Folders portion completed in {str(end - start)} seconds.")

# ----DECRYPT----
start = time.time()
print("Running decryption script...")
dir = r"D:\Snow\data\game\Game\Content\Paks"
working_files = [file for file in os.listdir(dir) if os.path.isfile(os.path.join(dir, file))]
scrub_targets = ["Blueprints", "Game_Effects", "Game_Environment", "Game_Maps", "Game_Materials", "Game_Plot", "Game_Props", "Game_Script", "App_PluginEngine", "Wwise"]
target_files = [x for x in working_files if not any([match in x for match in scrub_targets])]
print(f"Trimmed out {len(working_files) - len(target_files)} files based on scrub targets...")
cFile = 0
for file in target_files:
    cFile += 1
    print(f"Decrypting ({cFile:03d} of {len(target_files)}): {file}...")
    encoded_key = bytes(key, 'utf-8')
    subprocess.run([
    r"quickbms\quickbms_4gb_files.exe",
    "-C",
    "-Y",
    "-o",
    "-Q",
    "-F",
    "{}.pak",
    "-a",
    encoded_key,
    r"quickbms\unreal_tournament_4_0.4.27e_snowbreak.bms",
    fr"D:\Snow\data\game\Game\Content\Paks\{file}",
    r"X:\python\snow\decrypted",
    ],stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)

end = time.time()
total_time += (end - start)
print(f"Decryption portion completed in {str(end - start)} seconds.")

# ----EXTRACT----
start = time.time()
print("Running extraction script...")
os.system(f'cmd /c "py extractor.py"')
end = time.time()
total_time += (end - start)
print(f"Extraction portion completed in {str(end - start)} seconds.")

# ----CONSOLIDATE----
start = time.time()
print("Running consolidation script...")
os.system(f'cmd /c "py dataconsolidator.py"')
end = time.time()
total_time += (end - start)
print(f"Consolidation portion completed in {str(end - start)} seconds.")

# ----GACHA----
start = time.time()
print("Running gacha script...")
os.system(f'cmd /c "py gacha.py"')
end = time.time()
total_time += (end - start)
print(f"Gacha portion completed in {str(end - start)} seconds.")

# ----CLEANUP----
print("Extra cleanup...")
if os.path.isfile("notify.log"):
    os.remove('notify.log')

            
print("""
██████╗  ██████╗ ███╗   ██╗███████╗██╗
██╔══██╗██╔═══██╗████╗  ██║██╔════╝██║
██║  ██║██║   ██║██╔██╗ ██║█████╗  ██║
██║  ██║██║   ██║██║╚██╗██║██╔══╝  ╚═╝
██████╔╝╚██████╔╝██║ ╚████║███████╗██╗
╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚══════╝╚═╝
""")
print(f"Script executed in {total_time} seconds.")
os.startfile(os.path.realpath(r"X:\python\snow\extracted"))
input("\n\nPress enter key to terminate script...")