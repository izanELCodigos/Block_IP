#Importaciones
import customtkinter as tk
from PIL import Image as img
import os
import ctypes
import subprocess as sp


#File path
mainPath=os.path.dirname(os.path.abspath(__file__))

#Background management



#POO management
class dotLabel():
    def __init__(self, position):
        self.label=tk.CTkLabel(frame1, text=".",
                            font=tk.CTkFont(family="Cascadia Mono",
                            size=20))

        self.label.grid(row=0, column=position+1, pady=10)

class entry():
    def __init__(self, position):
        self.entry=tk.CTkEntry(frame1, font=tk.CTkFont(family="Cascadia Mono", size=15), width=50)
        self.position=position
        self.keyDown=False
        self.entry.grid(row=0, column=position+1)

        self.entry.bind("<KeyPress>", self.pressKey)
        self.entry.bind("<KeyRelease>", self.releaseKey)

    def get(self):
        return self.entry.get()

    def pressKey(self, event):
            key=event.keysym
            try:
                currentLen=len(self.entry.get())
                #Key filter
                if not key.isdigit() and (key not in ["BackSpace", "Delete", "Right", "Left", "Tab"] and event.char !="."):
                    return "break"

                if self.keyDown or (self.position==6 and currentLen==3 and key.isdigit()):
                    return "break"

                #Var definition
                self.keyDown=True
                mousePosition=self.entry.index("insert")

                #Backwards
                if key in ("BackSpace", "Left") and mousePosition==0:
                    if self.position > 0:
                        previousEntry=elementArray[self.position - 2].entry
                        if key=="BackSpace" and len(previousEntry.get())==3:
                            previousEntry.delete(len(previousEntry.get())-1, "end")
                        previousEntry.focus()
                    return "break"
                
                elif (key=="Right" and mousePosition==currentLen) or (key=="Tab" or event.char=="."):
                    if self.position < 6:
                        nextEntry=elementArray[self.position+2].entry
                        nextEntry.focus()
                    return "break"

                #3 digit auto-nextEntry insert
                elif key.isdigit() and currentLen==3 and self.position<6:
                    if int(self.entry.get())>255:
                        self.entry.delete(0, "end")
                        self.entry.insert(0, "255")
                    nextEntry=elementArray[self.position+2].entry
                    if len(nextEntry.get())!=3:
                        nextEntry.insert("end", event.char)
                    nextEntry.focus()
                    return "break"

                return False
            
            except Exception as e:
                print(f"Error: {e}")
                return False

    def releaseKey(self, event):
            try:
                currentLen=len(self.entry.get())
                if currentLen==3 and self.position==6:
                    if int(self.entry.get())>255:
                        self.entry.delete(0, "end")
                        self.entry.insert(0, "255")

                if self.keyDown:
                    self.keyDown=False                
            except Exception as e:
                print(f"Error: {e}")
                return False
            

#Functions management
def validateIP():
    octets=[
        elementArray[0].get().strip(),
        elementArray[2].get().strip(),
        elementArray[4].get().strip(),
        elementArray[6].get().strip()
    ]
    
    fullIp='.'.join(octets)

    if len(octets)!=4:
        raise ValueError("4 octets")

    for octet in octets:
        if not octet.isdigit():
            raise ValueError("Should be number")
        if not (0 <= int(octet) <= 255):
            raise ValueError("Should be between 0 and 255")

    first_octet = int(octets[0])
    
    #Validate IP
    if first_octet == 127:
        raise ValueError("Cannot block localhost adress (127.x.x.x)")
        
    if 224 <= first_octet <= 239:
        raise ValueError("Cannot block multicast adresses (224-239)")
        
    noValidIP = {
        "0.0.0.0", 
        "255.255.255.255", 
        "1.1.1.1", 
        "8.8.8.8"
    }
    
    if fullIp in noValidIP:
        raise ValueError(f"Cannot block {fullIp}: may harm device communication")

    blockIP(fullIp)
    return True


def blockIP(ip: str):
    checkComand = 'Get-NetFirewallRule -Name "Block_IP"'
    groupExists = False
    
    try:
        process = sp.run(
            ["powershell", "-NoProfile", "-Command", checkComand],
            capture_output=True,
            text=True,
            creationflags=sp.CREATE_NO_WINDOW
        )
        if process.returncode == 0:
            groupExists = True
    except Exception as e:
        print(f"Error: {e}")

    try:
        if groupExists:
            executeCommand = f"$current = @((Get-NetFirewallRule -Name 'Block_IP' | Get-NetFirewallAddressFilter).RemoteAddress); Set-NetFirewallRule -Name 'Block_IP' -RemoteAddress ($current + '{ip}')"
        else:
            executeCommand=f"New-NetFirewallRule -Name 'Block_IP' -DisplayName 'Block_IP' -Group 'Block_IP_Group' -Direction 'Inbound' -Action Block -RemoteAddress '{ip}'"

        resultado = ctypes.windll.shell32.ShellExecuteW(
            None, 
            "runas",
            "powershell.exe",
            f"-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -Command {executeCommand}",
            None,
            0
        )

        if resultado>32:
            print("Success")
            return True
        else:
            print("Unexpected error happened.")
            return False

    except Exception as e:
        print(f"Error: {e}")

#TK items
mainWindow=tk.CTk()
mainWindow.geometry("300x450+500+200")
mainWindow.grid_columnconfigure(0, weight=1)
mainWindow.grid_columnconfigure(1, weight=1)
mainWindow.resizable(False, False)

frame1=tk.CTkFrame(mainWindow, fg_color="transparent")

title=tk.CTkLabel(mainWindow,
                text="Block IP",
                font=tk.CTkFont(family="Cascadia Mono", size=20),
                fg_color="transparent")

entryLabel=tk.CTkLabel(frame1,
                        text="IP: ",
                        font=tk.CTkFont(family="Cascadia Mono", size=15))

blockButton=tk.CTkButton(mainWindow,
                            fg_color="darkred",
                            font=tk.CTkFont(family="Cascadia Mono", size=15),
                            text="Block IP",
                            corner_radius=5,
                            border_color="firebrick",
                            command=validateIP)


#Grid layout
title.grid(row=0, column=0, pady=20)
frame1.grid(row=1, column=0, pady=20)
entryLabel.grid(row=0, column=0, padx=5)
blockButton.grid(row=2, column=0)


#Start layout
elementArray={}
for x in range(7):
    elementArray[x]=entry(x) if x %2 == 0 else dotLabel(x)

mainWindow.mainloop()