import tkinter as tk

class MasterWindow(tk.Tk):
    def __init__(self,master=None):
        tk.Tk.__init__(self,master)
        self.geometry("170x20"+c.INITIAL_POS)
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.resizable(width=False, height=False)
        self.title(c.TITLE)
        self.bind('<Button-1>',self.clickwin)   # Click for dragging Window
        self.bind('<B1-Motion>',self.dragwin)   # Drag the Window
        my_menu = MyMenu(self, False)
        self.bind('<Button-3>',my_menu.popup)
        etiqueta = Label(self, text='', api_url=c.BINANCE_API_URL,
                         coin=c.BTCEUR)
