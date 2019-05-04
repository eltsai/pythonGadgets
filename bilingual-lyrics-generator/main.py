import tkinter as tk



    
class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Bi-Ly-Ge")
        self.geometry("400x800")
        self.text = tk.Text(self, height=40, width=80)
        self.text.pack(side=tk.TOP, fill=tk.X)
        self.text.focus_set()
        self.button = tk.Button(self, text='Add Time', command=self.generatelyrics)
        self.button.pack(side=tk.BOTTOM, pady=3)

    def generatelyrics(self):
        lines = self.text.get("1.0",'end-1c').splitlines()
        
        for i in range((len(lines)-1)//2):
            timeaxis = lines[2*i+2][:7]
            lines[2*i+1] = timeaxis + lines[2*i+1]
        self.text.delete("1.0",'end-1c')
        self.text.insert("1.0", "\n".join(lines))


if __name__ == '__main__':   
    root = Window()
    root.mainloop()