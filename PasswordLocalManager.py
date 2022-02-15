import tkinter as tk
from PIL import ImageTk, Image
import constants as c

class MasterWindow(tk.Tk):
    def __init__(self,master=None):
        tk.Tk.__init__(self,master)
        self.geometry("1000x1000")
        self.resizable(width=False, height=False)
        self.title("PasswordLocalManager")
        self.iconbitmap(c.LOCK_ICO)
        #Creates a Tkinter-compatible photo image, which can
        #be used everywhere Tkinter expects an image object.
        img = ImageTk.PhotoImage(Image.open('lock.png'))
        #The Label widget is a standard Tkinter widget ç
        #used to display a text or image on the screen.
        etiqueta1 = tk.Label(image=img)
        #The Pack geometry manager packs widgets in rows or columns.
        etiqueta1.pack()


if __name__ == '__main__':
    Win = MasterWindow()
    Win.mainloop()
