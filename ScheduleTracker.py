import os, pathlib, subprocess

def CheckValidTask(creator, task):  # <-- changed: corrected typo from CheckVaildTask to CheckValidTask
    allowlist = ["Microsoft", "Mozilla", "Adobe Systems Incorporated"]
    extensions = [".exe", ".py", ".dll"]  # <-- changed: fixed typo from .dil to .dll

    # Check if creator is trusted (boolean)  # <-- added
    trusted = any(creator.startswith(x) for x in allowlist)  # <-- changed: was list comprehension returning list, now boolean

    # Check if task has an allowed extension (boolean)  # <-- added
    executable = any(ext in task.lower() for ext in extensions)  # <-- changed: make lowercase and boolean check

    if executable:
        exe = task.split(" ")[0].strip("\"")  # <-- changed: strip quotes to handle paths like "C:\Program Files\App.exe"
        p = os.path.expandvars(exe).lower()  # <-- added: expand environment variables and lowercase for comparison

        # Corrected system32 path check and removed unnecessary backslash
        if p.startswith(r"c:\windows\system32"):  # <-- changed: fixed typo "systems32"
            return True
        else:
            return trusted  # <-- changed: return boolean instead of list
    else:
        return True  # <-- unchanged: allow tasks without the specified extensions

# Get scheduled tasks output
output = subprocess.check_output(
    "schtasks /query /v /fo csv /nh",  # <-- unchanged
    shell=True
).decode('utf-8').splitlines()  # <-- changed: decode bytes and split into lines instead of splitting "\\r\\n"

results = [o.split(',') for o in output]

for res in results:
    result = [x.strip("\"") for x in res]
    if len(result) > 8:
        name = result[1]
        creator = result[7]
        task = result[8]
        if not CheckValidTask(creator, task):
            print("%s, %s, %s" % (name, creator, task))  # <-- unchanged: print suspicious tasks
