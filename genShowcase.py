import os
import shutil
import time
import subprocess
import json5

scrDir = os.path.realpath(__file__)
scrDir = os.path.dirname(scrDir)

templatePath = os.path.join(scrDir, "__showcase_template.html")
listPath     = os.path.join(scrDir, "__showcase_list.html")
targetPath   = os.path.join(scrDir, "showcase.html")

showcaseDir  = os.path.join(scrDir, "showcase")

def generate_showcases():
    with open(templatePath, "r") as f:
        templateContent = f.read()

    with open(listPath, "r") as f:
        listContent = f.read()

    content  = templateContent
    projects = os.listdir(showcaseDir)
    projects.sort(key=lambda x: os.path.getctime(os.path.join(showcaseDir, x)), reverse=True)

    projectsList = ""
    for project in projects:
        if project.startswith("__"):
            continue

        projectPath = os.path.join(showcaseDir, project)
        if not os.path.isdir(projectPath):
            continue

        infoPath = f"{showcaseDir}/{project}/info.json"
        if not os.path.exists(infoPath):
            continue

        with open(infoPath, "r") as f:
            info = json5.load(f)

        thumbnailUrl = f"showcase/{project}/thumbnail.png"

        title  = info.get("title", "")
        ptype  = info.get("type", "")
        author = info.get("author", "")
        desc   = info.get("desc", "")
        link   = info.get("link", "")

        screenShots = ""
        screenShotDir = f"{showcaseDir}/{project}/screenshots"
        if os.path.exists(screenShotDir):
            scrs = os.listdir(screenShotDir)
            for s in scrs:
                if s.endswith(".png") or s.endswith(".gif"):
                    screenShots += f'<img class="preview" src="showcase/{project}/screenshots/{s}" alt="">\n'

        projectStr = listContent
        projectStr = projectStr.replace("{{THUMBNAIL}}", thumbnailUrl)
        projectStr = projectStr.replace("{{TITLE}}", title)
        projectStr = projectStr.replace("{{TYPE}}", ptype)
        projectStr = projectStr.replace("{{AUTHOR}}", author)
        projectStr = projectStr.replace("{{DESC}}", desc)
        projectStr = projectStr.replace("{{LINK}}", link)
        projectStr = projectStr.replace("{{SCREENSHOTS}}", screenShots)
        
        projectsList += projectStr + "\n"


    content = content.replace("{{CONTENT}}", projectsList)

    with open(targetPath, "w") as f:
        f.write(content)

    subprocess.run(["git", "add", "."], cwd=scrDir)
    subprocess.run(["git", "commit", "-m", "Auto push from gen.py"], cwd=scrDir)
    subprocess.run(["git", "push"], cwd=scrDir)

def main():
    generate_showcases()

if __name__ == "__main__":
    main()