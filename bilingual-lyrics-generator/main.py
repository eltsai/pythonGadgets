import tkinter as tk



if __name__ == '__main__':
    def generatelyrics():
        """
        :type inputString: str
        :rtype:str
        """
        
        
        lines = t.get("1.0",'end-1c').splitlines()
        
        for i in range((len(lines)-1)//2):
            timeaxis = lines[2*i+2][:7]
            lines[2*i+1] = timeaxis + lines[2*i+1]
        t.delete("1.0",'end-1c')
        t.insert("1.0", "\n".join(lines))
        
    root = tk.Tk()
    root.title("Bi-Ly-Ge")
    t = tk.Text(root, height=20, width=80)
    t.pack()
    button = tk.Button(root, text='Add Time', width=20, command=generatelyrics)
    button.pack()
    root.mainloop()