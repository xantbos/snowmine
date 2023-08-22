import subprocess, os

targetdirs = ["Startup", "UI", "Spine"]

for dir in targetdirs:
    print(f"Extracting from {dir}...")
    subprocess.run([r"umodel\umodel_64.exe", "-game=ue4.26", f"-path=decrypted/Game/Content/{dir}", "-export", fr"-out=extracted\{dir}", "-png", "*.uasset"],stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)