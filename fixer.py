import os
import shutil

dirr = "./projects"
folders = os.listdir(dirr)

com = '<a class="" href="../../community.html">Community</a>'
shw = '<a class="" href="../../showcase.html">Showcase</a>'
comshw = com + "\n" + shw

for f in folders:
    fpath = os.path.join(dirr, f)
    ppath = os.path.join(fpath, "index.html")

    if not os.path.exists(ppath):
        continue

    content = open(ppath).read()
    content = content.replace(com, comshw)

    with open(ppath, "w") as f:
        f.write(content)