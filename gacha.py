import os, re, json, shutil, sys
from datetime import datetime

script_dir = sys.argv[1]

date_dir_timestamp = datetime.today().strftime('%Y-%m-%d')

with open(fr"{script_dir}\extracted\_new\_special\{date_dir_timestamp}\Content_Settings_all_language_ui_gacha.txt", 'r', encoding='utf-8') as file:
    lines = file.readlines()
    keys = {}
    cLine = 0
    for line in lines:
        parsed = line.split("\t")
        if cLine > 1:
            template = {
                "en_US": parsed[5]
            }
            keys[parsed[0]] = template
        cLine+=1
        
    # compare keys to existing keys file
    if os.path.isfile("data.json"):
        with open('data.json', 'r') as infile:
            data = json.load(infile)
        keychanges = {}
        for key in keys:
            if key in data:
                # key exists in old data, check for update
                if data[key]["en_US"] != keys[key]["en_US"]:
                    # old key data updated in the new batch
                    template = {
                        "en_US_old": data[key]["en_US"],
                        "en_US_new": keys[key]["en_US"]
                    }
                    keychanges[key] = template
            else:
                # key does not exist in old data, new stuff!
                template = {
                    "en_US": keys[key]["en_US"]
                }
                keychanges[key] = template
                   
        json_object = json.dumps(keychanges, indent=2)
        
        with open("datachanges.json", 'w') as outfile:
            outfile.write(json_object)
            
        shutil.copyfile(fr"{script_dir}\datachanges.json", fr"X:\python\snow\extracted\_new\_special\{date_dir_timestamp}\_gachadatachanges.json")
       
    json_object = json.dumps(keys, indent=2)
    
    with open("data.json", 'w') as outfile:
        outfile.write(json_object)
        
    shutil.copyfile(fr"{script_dir}\data.json", fr"X:\python\snow\extracted\_new\_special\{date_dir_timestamp}\_gachadata.json")
        