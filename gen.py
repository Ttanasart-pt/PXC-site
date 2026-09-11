import os
import shutil
import time
import subprocess

scrDir = os.path.realpath(__file__)
scrDir = os.path.dirname(scrDir)
templatePath = os.path.join(scrDir, "__showcases_template.html")
listPath     = os.path.join(scrDir, "list.html")
targetPath   = os.path.join(scrDir, "showcases.html")

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

    fileDir  = os.path.join(projectDir, project)
    fileList = os.listdir(fileDir)
    fileUrl  = ""
    for _f in fileList:
        if _f.endswith(".pxc"):
            fileUrl = _f
    if fileUrl == "":
        continue

    fileUrl_local = os.path.join(fileDir, fileUrl)
    fileUrl_web   = os.path.join("./projects", project, fileUrl)

    fileSize = os.path.getsize(fileUrl_local)
    unit    = "b"
    divider = 1
    if fileSize > 1024 * 1024:
        unit    = "mb"
        divider = 1024 * 1024
    elif fileSize > 1024:
        unit    = "kb"
        divider = 1024

    fileSizeStr = f"{(fileSize/divider):.2f} {unit}"

    contentUrl  = os.path.join("./projects", project, "projectView.html")

    projectStr = listContent.replace("{{PROJECT_NAME}}", project)
    projectStr = projectStr.replace("{{CONTENT_URL}}",   contentUrl)
    projectStr = projectStr.replace("{{FILE_URL}}",      fileUrl_web)
    projectStr = projectStr.replace("{{FILE_SIZE}}",     fileSizeStr)

    projectsList += projectStr + "\n"


content = content.replace("{{CONTENT}}", projectsList)

with open(targetPath, "w") as f:
    f.write(content)

subprocess.run(["git", "add", "."])
subprocess.run(["git", "commit", "-m", "Update projects list"])
subprocess.run(["git", "push"])