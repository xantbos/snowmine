import subprocess, os

root=r'X:\python\snow\decrypted\Game\Content'
dirlist = [ item for item in os.listdir(root) if os.path.isdir(os.path.join(root, item)) ]

targetdirs = ["Startup", "UI", "Spine"]

for dir in targetdirs:
    print(f"Extracting from {dir}...")
    subprocess.run([r"umodel\umodel_64.exe", "-game=ue4.26", f"-path=decrypted/Game/Content/{dir}", "-export", fr"-out=extracted\{dir}", "-png", "*.uasset"],stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)