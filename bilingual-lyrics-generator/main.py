import tkinter as tk



if __name__ == '__main__':
    def generatelyrics():
        """
        :type inputString: str
        :rtype:str
        """
        print("hi")
        res = ''
        
        lines = t.get("1.0",'end-1c').splitlines()
        for i in range((len(lines)-1)//2):
            timeaxis = lines[2*i][:7]
            lines[2*i+1].insert(0, timeaxis)
            res += lines[2*i]
            res += '\n'
            res += lines[2*i+1]
            res += '\n'
        t.insert("1.0", res)
        print(res)
    root = tk.Tk()
    root.title("Bi-Ly-Ge")
    t = tk.Text(root, height=50, width=40)
    t.pack()
    button = tk.Button(root, text='Add Time', width=20, command=generatelyrics)
    button.pack()
    root.mainloop()