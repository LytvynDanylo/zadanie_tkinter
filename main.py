import tkinter as tk

from ui import PhysicsFormulaApp

def main():
    root = tk.Tk()
    app = PhysicsFormulaApp(root)
    root.mainloop()
    return app


if __name__ == "__main__":
    main()
