import os, shutil, filecmp, sys
from datetime import datetime

script_dir = sys.argv[1]

settings_files_path = fr"{script_dir}\decrypted\Game\Content\Settings"
movies_files_path = fr"{script_dir}\decrypted\Game\Content\Movies"

dir_path = fr"{script_dir}\extracted"

date_dir_timestamp = datetime.today().strftime('%Y-%m-%d')

target_dir = fr"{script_dir}\extracted\_new\_single"
special_target_dir = fr"{script_dir}\extracted\_new\_special"
movies_target_dir = fr"{script_dir}\extracted\_new\_movies"

directories = [target_dir, special_target_dir, movies_target_dir]
print("Moving previous new folders to consolidated...")
for newfolder in directories:
    folders = [x[0] for x in os.walk(newfolder)]
    folders.pop(0)
    for folder in folders:
        shutil.move(folder, folder.replace("_new", "_consolidated"))

if not os.path.exists(fr"{target_dir}\{date_dir_timestamp}"): os.makedirs(fr"{target_dir}\{date_dir_timestamp}")
if not os.path.exists(fr"{special_target_dir}\{date_dir_timestamp}"): os.makedirs(fr"{special_target_dir}\{date_dir_timestamp}")
if not os.path.exists(fr"{movies_target_dir}\{date_dir_timestamp}"): os.makedirs(fr"{movies_target_dir}\{date_dir_timestamp}")

do_not_check_directories = ["_new", "_consolidated"]#, "_single", "_special", "_movies"]

marked_file_contents = [
"UI_Picture_pic_login", 
"House_house", 
"FashionIcon", 
"GirlIcon_GirlIcon", 
"UI_Icon_Monster_pic",
"UI_Picture_Activity",
"UI_Picture_Gacha",
"UI_Pose_Fashion",
"dlc",
"DLC",
"Picture_Gacha",
"Pose_Girl_icon",
"Activity_pic_bp"
]

for (dir_path, dir_names, file_names) in os.walk(dir_path):
    if not any([match in dir_path for match in do_not_check_directories]):
        for file in file_names:
            if file.endswith(".png") or file.endswith(".txt") or file.endswith(".json"):
                safety_prefix = "_".join(dir_path.split("\\")[5:]) + "_"
                target_absolute_path = f"{safety_prefix}{file}"
                if any([match in target_absolute_path for match in marked_file_contents]):
                    #print(fr"Moving {dir_path}\{file} ==> {special_target_dir}\{date_dir_timestamp}\{target_absolute_path}")
                    shutil.move(fr"{dir_path}\{file}", fr"{special_target_dir}\{date_dir_timestamp}\{target_absolute_path}")
                else:
                    #print(fr"Moving {dir_path}\{file} ==> {target_dir}\{date_dir_timestamp}\{target_absolute_path}")
                    shutil.move(fr"{dir_path}\{file}", fr"{target_dir}\{date_dir_timestamp}\{target_absolute_path}")
                
for (dir_path, dir_names, file_names) in os.walk(settings_files_path):
    for file in file_names:
        if "gacha" in file and "txt" in file:
            safety_prefix = "_".join(dir_path.split("\\")[5:]) + "_"
            target_absolute_path = f"{safety_prefix}{file}"
            #print(fr"Moving {dir_path}\{file} ==> {special_target_dir}\{date_dir_timestamp}\{target_absolute_path}")
            shutil.move(fr"{dir_path}\{file}", fr"{special_target_dir}\{date_dir_timestamp}\{target_absolute_path}")
                
for (dir_path, dir_names, file_names) in os.walk(movies_files_path):
    for file in file_names:
        #print(file)
        if "mp4" in file or "avi" in file:
            safety_prefix = "_".join(dir_path.split("\\")[5:]) + "_"
            target_absolute_path = f"{safety_prefix}{file}"
            #print(fr"Moving {dir_path}\{file} ==> {movies_target_dir}\{date_dir_timestamp}\{target_absolute_path}")
            shutil.move(fr"{dir_path}\{file}", fr"{movies_target_dir}\{date_dir_timestamp}\{target_absolute_path}")
            

def check_old_folders_for_file(newpath, filename):
    matches = []
    oldpath = newpath.replace("_new", "_consolidated")
    oldpath = "\\".join(oldpath.split("\\")[:-1])
    oldfolders = [x[0] for x in os.walk(oldpath)]
    oldfolders.pop(0)
    for oldfolder in oldfolders:
        if os.path.isfile(fr"{oldfolder}\{filename}"):
            result = filecmp.cmp(fr"{oldfolder}\{filename}", fr"{newpath}\{filename}")
            matches.append(True) if result else matches.append(False)
    if len(matches) > 0:
        if matches[-1]:
            #print(fr"Deleting matched file {newpath}\{filename}")
            os.remove(fr"{newpath}\{filename}")

print("Pruning existing matching files...")
for newfolder in directories:
    folders = [x[0] for x in os.walk(newfolder)]
    folders.pop(0)
    for folder in folders:
        files = os.listdir(folder)
        for file in files:
            check_old_folders_for_file(folder, file)
                        
            
print("Cleaning house...")
root=fr'{script_dir}\extracted'            
dirlist = [ item for item in os.listdir(root) if os.path.isdir(os.path.join(root, item)) ]
for dir in dirlist:
    if not any([match in dir for match in do_not_check_directories]):
        print(fr"Pruning {root}\{dir}...")
        shutil.rmtree(fr"{root}\{dir}")
