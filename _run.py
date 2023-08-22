import os, subprocess, sys, shutil, json, random, time, datetime, pathlib

headertext = "Snowbreak Decryptor AIO"

with open('config.json', 'r') as infile:
    data = json.load(infile)
    pak_dir = data["pak_dir"]
    script_dir = data["script_dir"]

os.system("title " + headertext)

total_time = 0

def terminate_script():
    print("""
██████╗  ██████╗ ███╗   ██╗███████╗██╗
██╔══██╗██╔═══██╗████╗  ██║██╔════╝██║
██║  ██║██║   ██║██╔██╗ ██║█████╗  ██║
██║  ██║██║   ██║██║╚██╗██║██╔══╝  ╚═╝
██████╔╝╚██████╔╝██║ ╚████║███████╗██╗
╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚══════╝╚═╝
""")
    print(f"Script executed in {total_time:.2f} seconds.")
    input("\n\nPress enter key to terminate script...")
    sys.exit()

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
        fr"{pak_dir}\App_Engine-WindowsNoEditor.pak",
        fr"{script_dir}\decrypted",
        ], capture_output=True)

        if res.returncode == 0:
            return key
            break
    return 0

# ----CHANGE CHECK----
start = time.time()
if os.path.isfile("changemaster.json"):
    with open('changemaster.json', 'r') as infile:
        data = json.load(infile)
else:
    data = {}
changed_files = []
for pak_file in [file for file in os.listdir(pak_dir)]:
    last_changed_timestamp = str(pathlib.Path(fr"{pak_dir}\{pak_file}").stat().st_mtime)
    if pak_file in data:
        if data[pak_file] != last_changed_timestamp:
            data[pak_file] = last_changed_timestamp
            changed_files.append(pak_file)
    else:
        data[pak_file] = last_changed_timestamp
        changed_files.append(pak_file)
if not changed_files:
    print(fr"No changed files found in the given path '{pak_dir}': skipping script execution.")
    end = time.time()
    total_time += (end - start)
    terminate_script()
else:
    with open("changemaster.json", 'w') as outfile:
        outfile.write(json.dumps(data, indent=2))
end = time.time()
total_time += (end - start)

# ----AES----
start = time.time()
print("Generating AES key values...")
if os.path.exists(fr"{script_dir}\AES.Key.Finder\Game"): shutil.rmtree(fr"{script_dir}\AES.Key.Finder\Game")
subprocess.run([fr"{script_dir}\AES.Key.Finder\RUN Find 256-bit UE4 AES Key.bat"],stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)

keys=[]

for (dir_path, dir_names, file_names) in os.walk(fr"{script_dir}\AES.Key.Finder\Game"):
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
print(f"AES portion completed in {(end - start):.2f} seconds.")

# ----FOLDERS----
start = time.time()
print("Generating working folders...")
if os.path.exists("decrypted"): 
    print("Deleting old decrypted folder and subdirectories...")
    shutil.rmtree(fr"{script_dir}\decrypted")
    os.makedirs("decrypted")
if not os.path.exists("extracted"): os.makedirs("extracted")
end = time.time()
total_time += (end - start)
print(f"Folders portion completed in {(end - start):.2f} seconds.")

# ----DECRYPT----
start = time.time()
print("Running decryption script...")
scrub_targets = ["Blueprints", "Game_Effects", "Game_Environment", "Game_Maps", "Game_Materials", "Game_Plot", "Game_Props", "Game_Script", "App_PluginEngine", "Wwise"]
target_files = [x for x in changed_files if not any([match in x for match in scrub_targets])]
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
    fr"{pak_dir}\{file}",
    fr"{script_dir}\decrypted",
    ],stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)

end = time.time()
total_time += (end - start)
print(f"Decryption portion completed in {(end - start):.2f} seconds.")

# ----EXTRACT----
start = time.time()
print("Running extraction script...")
os.system(f'cmd /c "py extractor.py"')
end = time.time()
total_time += (end - start)
print(f"Extraction portion completed in {(end - start):.2f} seconds.")

# ----CONSOLIDATE----
start = time.time()
print("Running consolidation script...")
os.system(f'cmd /c "py dataconsolidator.py {script_dir}"')
end = time.time()
total_time += (end - start)
print(f"Consolidation portion completed in {(end - start):.2f} seconds.")

# ----GACHA----
start = time.time()
print("Running gacha script...")
os.system(f'cmd /c "py gacha.py {script_dir}"')
end = time.time()
total_time += (end - start)
print(f"Gacha portion completed in {(end - start):.2f} seconds.")

# ----CLEANUP----
print("Extra cleanup...")
if os.path.isfile("notify.log"):
    os.remove('notify.log')

os.startfile(os.path.realpath(fr"{script_dir}\extracted"))
terminate_script()