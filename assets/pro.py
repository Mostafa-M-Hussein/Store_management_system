from tkinter import *
import tkinter as tk

class Image_viewer:
    
    def __init__(self, win):
        self.root = win
        self.root.title('Root Window')
        self.root.geometry('200x150+600+200')
        
        self.lblHeading = tk.Label(self.root,
                                   text = 'Root Window',
                                   font = ('Times New Roman', 14),
                                   bg = 'White')
        self.lblHeading.pack(side = tk.TOP)
        self.lblHeading.focus()
        
        self.btnView = tk.Button(self.root, text = 'Image Viewer', command = self.view)
        self.btnView.place(relx = 0.5, rely = 0.9, anchor = tk.SE)
        self.btnClose = tk.Button(self.root, text = 'Close', command = self.close)
        self.btnClose.place(relx = 0.8, rely = 0.9, anchor = tk.SE)

   #function for inserting image based off selection
    def listboxinsert(self):
        self.imgas = tk.PhotoImage(file = 'print.png')
        self.imggr = tk.PhotoImage(file = 'icon.png')
        cs = self.Lb.curselection()
        
        if self.Lb.get(cs) == 0:
                #creates textbox to insert image into 
                self.mytext = tk.Text(self.top)
                self.mytext.place(relx = 0.5, rely = 0.80, height=150, width=200, anchor = tk.CENTER)
                #inserts image into textbox
                self.mytext.image_create(tk.END, image = self.imgas) 
        elif self.Lb.get(cs) == 1:
                #creates textbox to insert image into  
                self.mytext = tk.Text(self.top)
                self.mytext.place(relx = 0.5, rely = 0.80, height=150, width=200, anchor = tk.CENTER)
                #inserts image into textbox
                self.mytext.image_create(tk.END, image = self.imggr)
    def view(self):
        #creating top level
        self.top = Toplevel()
        self.top.title('Top Level')
        self.top.geometry('500x500')
        #Quit Button
        self.btnClose2 = Button(self.top, text="Quit", command= self.top.destroy)
        self.btnClose2.place(relx = 0.9, rely = 0.1, anchor = tk.SE)
        #initializing listbox
        self.Lb = Listbox(self.top, height=6) 
        self.Lb.place(relx = 0.3, rely = 0.3, anchor = tk.SE)
        #binding event to listbox selection
        self.Lb.bind('<<ListboxSelect>>', self.listboxinsert)

        # Inserting items in Listbox 
        self.Lb.insert(0, 'as') 
        self.Lb.insert(1, 'gr')
   
    def close(self):
        self.root.destroy()
      
def main():
    root = tk.Tk()
    Image_viewer(root)
    root.mainloop()
    
if __name__ == '__main__':
    main()
