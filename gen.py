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
    if os.path.isdir(projectPath):
        projectLink = f'<li><a href="projects/{project}/">{project}</a></li>'
        projectsList += projectLink + "\n"

content = content.replace("{{CONTENT}}", projectsList)

with open(targetPath, "w") as f:
    f.write(content)

subprocess.run(["git", "add", "."])
subprocess.run(["git", "commit", "-m", "Update projects list"])
subprocess.run(["git", "push"])