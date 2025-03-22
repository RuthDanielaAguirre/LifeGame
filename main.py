import tkinter as tk
from ui.login_window import LoginWindow

def main():
    print("🟢 Ejecutando main.py")
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
