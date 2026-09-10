import os
import shutil
import time
import subprocess

scrDir = os.path.realpath(__file__)
scrDir = os.path.dirname(scrDir)
templatePath = os.path.join(scrDir, "__template.html")
listPath     = os.path.join(scrDir, "list.html")
targetPath   = os.path.join(scrDir, "projects.html")

projectDir   = os.path.join(scrDir, "projects")

with open(templatePath, "r") as f:
    templateContent = f.read()

with open(listPath, "r") as f:
    listContent = f.read()

content  = templateContent
projects = os.listdir(projectDir)
projects.sort(key=lambda x: os.path.getmtime(os.path.join(projectDir, x)), reverse=True)

projectsList = ""
for project in projects:
    projectPath = os.path.join(projectDir, project)
    if not os.path.isdir(projectPath):
        continue

    fileUrl  = f"projects/{project}/{project}.pxc"
    fileSize = os.path.getsize(fileUrl)

    unit    = "b"
    divider = 1
    if fileSize > 1024 * 1024:
        unit    = "mb"
        divider = 1024 * 1024
    elif fileSize > 1024:
        unit    = "kb"
        divider = 1024

    fileSizeStr = f"{(fileSize/divider):2f} {unit}"

    projectStr = listContent.replace("{{PROJECT_NAME}}", project)
    projectStr = projectStr.replace("{{FILE_URL}}",     fileUrl)
    projectStr = projectStr.replace("{{FILE_SIZE}}",    fileSizeStr)

    projectsList += projectStr + "\n"


content = content.replace("{{CONTENT}}", projectsList)

with open(targetPath, "w") as f:
    f.write(content)

subprocess.run(["git", "add", "."])
subprocess.run(["git", "commit", "-m", "Update projects list"])
subprocess.run(["git", "push"])