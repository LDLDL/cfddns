Set ws = CreateObject("Wscript.Shell")
ws.CurrentDirectory = "c:\cfddns"
ws.run "python c:\cfddns\cfddns.py", vbhide