import win32evtlog
import xml.etree.ElementTree as ET
import psutil
import subprocess   # <-- added to launch a test process for simulation

server = "localhost"
# logtype = "Microsoft-Windows-WMI-Activity/Trace"   # <-- original
logtype = "Microsoft-Windows-WMI-Activity/Operational"  # <-- changed: Operational is correct channel
flags = win32evtlog.EvtQueryForwardDirection
query = "*[System[EventID=23]]"  # WMI Process Create event

def GetEventLogs():
    q = win32evtlog.EvtQuery(logtype, flags, query)
    # events = ()   # <-- original
    events = []     # <-- changed: use list instead of tuple so we can append/extend
    while True:
        try:
            e = win32evtlog.EvtNext(q, 100, -1, 0)
        except Exception:
            break
        if e:
            # events = events + e   # <-- original
            events.extend(e)        # <-- changed: use list extend
        else:
            break
    return events

def CollectProcessInfo(pid):
    try:
        proc = psutil.Process(pid)
        return {
            "pid": pid,
            "name": proc.name(),
            "exe": proc.exe(),
            "cmdline": proc.cmdline(),
            "ppid": proc.ppid(),
            "username": proc.username(),
            "create_time": proc.create_time(),
        }
    except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
        return {"pid": pid, "error": str(e)}

def ParseEvents(events):
    pids_found = []  # <-- added: store PIDs found in Event Log
    for event in events:
        xml = win32evtlog.EvtRender(event, 1)
        root = ET.fromstring(xml)

        path = './{*}UserData/{*}ProcessCreate/{*}'
        # name = root.findall(path+'CreatedProcessId')[0].text   # <-- original
        pid_elem = root.find(path + 'CreatedProcessId')          # <-- changed: safer lookup
        if pid_elem is not None:
            pid = int(pid_elem.text)
            pids_found.append(pid)                                # <-- added: store PID
            print(f"[EVENT] WMI process launched with PID {pid}") # <-- changed: fixed formatting
            info = CollectProcessInfo(pid)                        # <-- added: collect process info
            print("    Details:", info)                            # <-- added: display info
    return pids_found

if __name__ == "__main__":
    events = GetEventLogs()
    pids = ParseEvents(events)

    # === simulation fallback ===
    if not pids:   # <-- added: if no Event ID 23 found, simulate a process
        print("[INFO] No Event ID 23 found. Launching a test process for simulation.") # <-- added
        test_proc = subprocess.Popen(["notepad.exe"])   # <-- added: launch test process
        pid = test_proc.pid                              # <-- added: get PID
        print(f"[SIMULATION] Test process launched with PID {pid}") # <-- added
        info = CollectProcessInfo(pid)                   # <-- added
        print("    Details:", info)                       # <-- added
        # Optional: terminate the test process after checking
        # test_proc.terminate()                           # <-- added (commented)
