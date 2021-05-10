import sqlite3
import psutil
import tkinter
import tkinter as tk
import random
import string
import sys
import datetime
from tkinter import ttk
from tkinter import *
from tkinter.ttk import Notebook
from tkinter import messagebox
from  tkinter import font
from time import sleep
from PIL import Image, ImageTk
from time import strftime
import tempfile
import os
import csv
import pandas
from threading import Thread, ThreadError


class database:
    data = []

    try:

        path = 'database.db'
        p = os.popen('attrib -h ' + path)
        conn = sqlite3.connect('database.db', timeout=10)
        c = conn.cursor()

        c.execute("CREATE TABLE IF NOT EXISTS COSTS (name TEXT NOT NULL , costs INT NOT NULL)")
        c.execute("CREATE TABLE IF NOT EXISTS products (products TEXT NOT NULL,cost INT NOT NULL)")
        admin = [('admin'), (12345)]
        c.execute("CREATE TABLE IF NOT EXISTS admin (NAME TEXT NOT NULL,password INT NOT NULL)")
        c.execute("DELETE FROM admin WHERE 0 NOT IN (SELECT NAME FROM admin ) ")
        c.executemany("INSERT INTO admin(NAME , password) VALUES (? , ?) " , (admin , ))
        c.execute("SELECT rowid , * FROM admin ")
        conn.commit()
    except sqlite3.Error as e:
        print(e)

    # connection.total_changes()
    def is_open(self):
        path = os.path.abspath(self.path)
        try:
            for proc in psutil.process_iter():
                _files = proc.open_files()
                for _file in _files:
                    if _file.path == path:
                        break;
                    return True
        except (psutil.NoSuchProcess, psutil.AccessDenied) as err:
            print(err)

        return False

    def delet_table(self):
        self.c.execute("DROP TABLE COSTS")

    def delete_record(self, pro_id):
        if pro_id == None:
            messagebox.showwarning("", " ")
        self.c.execute("DELETE FROM products WHERE products =?", (pro_id,))
        self.conn.commit()

    def get_records(self, id_num):
        self.c.execute("SELECT * from products WHERE products = ? ", (id_num))

    # c.execute("DELETE from admin WHERE ROWID = (?)", (str(id_num)))

    def add_record(self, product_name, product_cost):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        # c.execute("DROP TABLE products")
        if len(product_cost) <= 0 and len(str(product_cost)) < 0:
            messagebox.showwarning("Error", "you cannot Enter a Empty Items ")
        data = [(product_name, product_cost)]
        self.c.execute("CREATE TABLE IF NOT EXISTS products (products  NOT NULL,cost INT NOT NULL)")
        self.c.executemany("INSERT INTO products (products , cost) VALUES(? , ? )", data)
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def call_cost_table(self, COSTS):

        self.c.execute("CREATE TABLE IF NOT EXISTS COSTS (name TEXT NOT NULL , costs INT NOT NULL) UNIQUE(name , costs )")
        self.c.execute("INSERT INTO COSTS VALUES ?", COSTS)
        self.conn.commit()

        print()


class app_win(tk.Tk, database):

    def __init__(self):
        tk.Tk.__init__(self)


        self.iconbitmap("assets/icon.ico")
        # self.overrideredirect(True)
        self.title("Cinzel")
       # self.bind('<Alt-c>' , lambda S:self.destroy())
        screen_state = self.fullScreenState = True
        self.attributes('-fullscreen', screen_state)
        self.configure(bg='#262626')

        bg, fg, font, relief = [
            ("#262626"),
            ('whitesmoke'),
            ('Calibri', 20, "bold"),
            ('flat')

        ]
        login_data = self.c.fetchall()
        username = []
        passwords = []
        for rowid, admin, password in login_data:
            username.append(admin)
            passwords.append(str(password))

        self.img = ImageTk.PhotoImage(Image.open("assets/login_icon.ico"))
        exit_but = Button(text='Login', bg=bg, relief='groove', width=120, height=120, fg=fg, font=font, bd=0,
                          image=self.img, command=lambda: self.destroy(), activeforeground="white", activebackground=bg)

        erro_label = Label(self, text="", bg=bg, fg=fg, font=font)
        lab = Label(self, text="Username:", bg=bg, fg=fg, font=font)
        lab1 = Label(self, text="password:", bg=bg, fg=fg, font=font)

        use_ent = Entry(self, text="Username:", bg=bg, fg=fg, font=font, width=30)

        use_ent.focus()
        password_ent = Entry(self, text="Password:", bg=bg, fg=fg, font=font, show="*", width=30)
        self.head_img = ImageTk.PhotoImage(Image.open("assets/icon.ico"))
        icon_lab = Button(self, width=250, height=250, bg=bg, image=self.head_img, bd=0, activeforeground='#262626',
                          activebackground='#262626')

        def command():

            if use_ent.get() in username and password_ent.get() in passwords:
                self.destroy()
                S = Thread(target= self.main_win , args = ( sys.argv ) )
                S.start()




            else:
                erro_label.configure(text="login Failed . Checked your password and try again ", relief='flat')
                messagebox.showwarning("Error", "login Failed")
                erro_label.after(2000, erro_label.configure(text=""))
                use_ent.delete(0 , END )
                password_ent.delete(0, END )


        re = 0.4
        b1 = Button(text='Login', bg=bg, relief='groove', width=20, fg=fg, font=font, command=command, bd=1,
                    activebackground='whitesmoke', activeforeground='black', )
        # pack the button into Window
        erro_label.place(relx=re, rely=0.1)
        lab.place(relx=re, rely=0.2)
        use_ent.place(relx=re, rely=0.3)
        lab1.place(relx=re, rely=0.4)
        password_ent.place(relx=re, rely=0.5)
        b1.place(relx=re, rely=0.6, )
        exit_but.place(relx=0.9, rely=0.8)

        icon_lab.place(relx=0.2, rely=0.4)

    @property
    def main_win(self):
        tkinter.Tk.__init__(self)
        self.title("Cinzel")
        # height =   str(self.winfo_screenwidth() )
        # width  = str(self.winfo_screenwidth() )
        # self.geometry("{0}x{1}+-10+-10".format(width , height))
        self.attributes('-fullscreen', True)
        # self.bind("<F1>", lambda s: self.destroy())
        self.resizable(0, 0)
        self.iconbitmap("assets/accounting.ico")
        self.configure(bg="#262626")
        self.resizable(2, 2)
        self.img = ImageTk.PhotoImage(Image.open("assets/icon.ico"))
        exit_img = ImageTk.PhotoImage(Image.open("assets/shutdown.png"))

        bg, fg, font, relief = [
            ("#262626"),
            ('grey'),
            ('Calibri', 20, "bold"),
            ('flat')

        ]
        notebook = ttk.Notebook(self)
        notebook.pack(fil='both', expand=True, )

        # create frames
        h, w = (self.winfo_height(), self.winfo_width())
        frame1 = ttk.Frame(notebook)
        frame2 = ttk.Frame(notebook)

        frame1.pack(fill='both', expand=True)
        frame2.pack(fill='both', expand=True)

        # add frames to notebook

        notebook.add(frame1, text='General')
        notebook.add(frame2, text='AddProducts')

        def add_new_pro():

            def change_state():
                sucess_lab.configure(text="")

            if len(e1.get()) <= 0 & len(e2.get()) <= 0:
                messagebox.showwarning("Error", "you Cannot add a Empty Product")
            elif e2.get().isdigit() == False:
                messagebox.showwarning("Error", "should enter a Correct numbers")
            elif e1.get().isalpha() == False:
                messagebox.showwarning('Error', "should enter a Valid product ")
            else:
                self.add_record(e1.get(), e2.get())
                sucess_lab = Label(l2, text="Add Successfully", font=font, fg=fg, bg=bg)
                sucess_lab.pack(side=BOTTOM)
                sucess_lab.after(3000, change_state)
            e1.delete(0, END)
            e2.delete(0, END)

        # images
        delete_img = ImageTk.PhotoImage(Image.open("assets/remove1_db.png"))
        add_img = ImageTk.PhotoImage(Image.open("assets/add_db.png"))
        add_img2 = ImageTk.PhotoImage(Image.open("assets/add_but2.png"))
        print_image = ImageTk.PhotoImage(Image.open("assets/print.png"))
        # first Window
        l1 = LabelFrame(frame1, bg='#262626', fg='whitesmoke', relief=relief , borderwidth  = 0 , highlightthickness  = 0 , bd = -2  )
        l1.pack(side=LEFT, expand=True, fill='both')
        l2 = LabelFrame(frame2, bg='#262626', fg='whitesmoke', relief=relief, width=w, height=h , borderwidth  = 0 , highlightthickness  = 0 )
        l2.pack(side=TOP, expand=True, fill='both')
        Te = Label(l2, text="Products Name ", font=font, fg=fg, bg=bg)
        e1 = Entry(l2, fg=fg, font=font, width=90, bg=bg)
        e2 = Entry(l2, bg=bg, fg=fg, font=font, width=90)
        Te1 = Label(l2, text="Costs", font=font, fg=fg, bg=bg)
        add_but = Button(l2, image=add_img, text='add', bg=bg , relief=relief, width=125, height=125, fg=fg, font=font,
                         bd=0,
                         command=lambda: [add_new_pro(), get_all_pro()], activebackground="#262626",
                         activeforeground="#262626", )

        def get_all_pro():
            prod_list.delete(0, END)
            try:
                self.c.execute("SELECT rowid , * FROM products ")
                for rowid, name, cost in self.c.fetchall():
                    prod_list.insert(rowid, name)
            except sqlite3.Error as e:
                print(e)

        def get_selected_item():
            if prod_list.curselection():
                get_active = str(prod_list.get(ACTIVE).split(" ")[0])
                if get_active is None or get_active == " ":
                    messagebox.showwarning(" ", " ")

                return get_active


        prod_list = Listbox(l1, selectmode=BROWSE, bg=bg, fg='grey', width=200, height=150, relief=relief,
                            selectbackground="white", font=('Helvetica', 20 ), activestyle = None)
        delete_but = Button(l1, image=delete_img, text='add', bg=bg, relief=relief, width=125, height=125, fg=fg,
                            font=font,
                            bd=0,
                            command=lambda: [self.delete_record(get_selected_item()), get_all_pro],
                            activebackground="#262626",
                            activeforeground="#262626", )

        get_all_pro()
        su_img = ImageTk.PhotoImage(Image.open("assets/Success_40973.png"))
        message = Label(l1, text="", font=font, fg=fg, bg=bg , bd= 0 )

        def call_cost_table():
            message.configure(text = "add Succesfully")
            message.bind(3000  , message.configure(text = "") )
            if prod_list.curselection():
                get_active = str(prod_list.get(ACTIVE).split(" ")[0])
                self.c.execute("SELECT products , cost FROM products WHERE products = ?", (get_active,))
                last_cost = []
                pro_name = []
                for pro, cost in self.c.fetchall():
                    last_cost.append(cost)
                    pro_name.append(pro)
                self.c.execute("CREATE TABLE IF NOT EXISTS COSTS (name TEXT NOT NULL , costs INT NOT NULL)")
                self.c.execute("INSERT INTO COSTS VALUES (? , ?) ", (pro_name[0], last_cost[0]))
                self.conn.commit()











        def check_out():

            #self.c.execute("CREATE TABLE IF NOT EXISTS COSTS (name TEXT NOT NULL , costs INT NOT NULL) UNIQUE(name , costs )")
            self.c.execute("SELECT name , costs FROM COSTS")
            total = 0
            order_data = []
            

            text = ''

            for names, i in self.c.fetchall():
                total += i
                text += names

            if len(text) <= 0:
                messagebox.showwarning(" ", " ")
            else:
                date = datetime.date.today()
                current_date = date.strftime("%Y /%H %m/%d")
                message = f"""
                              Cinzel Report 
    
                          Date {current_date}
                          from Docmuntion {random.randint(1000 ,2000)}
                          to documntion {random.randint(1000 ,2000)}
                          ---------------------
                          User sales: {random.randint(0, 1000)}
                          ---------------------
                          Cash: \t 03213
                          ---------------------
                          Total returns 10
                          ---------------------
                          Total:{total}
                          {text}
                          
                          ------------------------
                               Client Copy 
                          ________________________
    
    
                          """
                print(message)
                doc_file = "cash.doc"
                with open(doc_file, "w+") as f:
                    f.write(message)
                x, path2 = tempfile.mkstemp('.doc')

                if os.path.exists(doc_file):
                    os.startfile(doc_file, 'print')
                    os.popen("attrib +h"+doc_file )

                    # for p in psutil.process_iter():
                    #     if "WINWORD.EXE" in str(p):
                    #         p.kill()

                def End_of_dat():

                    for p in psutil.process_iter():
                        if "EXCEL.EXE" in str(p):
                            p.kill()

                    current_date = datetime.date.today()
                    date = current_date.strftime("%m/%d/%Y, %H:%M:%S")
                    print(date)
                    self.c.execute("SELECT name , costs FROM COSTS")
                    all_data = self.c.fetchall()
                    x = ["sdsd", "dsds", "dsdas"]

                    def add_row(new_text, new_text2, datetime):

                        writer.writerow({"produts": new_text, "cost": new_text2, 'date': datetime})



                    csv_file = 'test.csv'
                    if os.path.exists(csv_file) == True :pass
                    else:
                        open(csv_file , "w")
                    fieldnames = ["produts", "cost", 'date']


                    with open(csv_file, 'a+', newline='\n') as csvfile:
                        writer = csv.DictWriter(csvfile , fieldnames=fieldnames)

                        total_end_of_day = 0
                        for pro, cos in all_data:
                            add_row(pro, cos, date)


                    csvfile.close()



                End_of_dat()
                self.c.execute("DROP TABLE COSTS")

        ##########################
        check_out_but = Button(l1, image=add_img2, text='add', bg=bg, relief='groove', width=125, height=125, fg=fg,
                               font=font,
                               bd=0,
                               command=call_cost_table, activebackground="#262626", activeforeground="#262626")

        add_but2 = Button(l1, image=print_image, text='add', bg=bg, relief='groove', width=125, height=125, fg=fg,
                          font=font,
                          bd=0,
                          command=check_out, activebackground="#262626", activeforeground="#262626")




        exit_butt = Button(l1, image=exit_img, text='add', bg=bg, relief=relief, width=125, height=125, fg=fg, font=font,
                         bd=0,
                         activebackground="#262626",
                         activeforeground="#262626",
                            command= self.destroy )

        add_but2.place(rely=0.8, relx=0.8, bordermode=OUTSIDE)
        delete_but.place(rely=0.8, relx=0.6, bordermode=OUTSIDE)
        check_out_but.place(rely=0.8, relx=0.7, bordermode=OUTSIDE)
        prod_list.pack(side=LEFT, expand=True, fill='y')
        exit_butt.place(rely = 0.8 , relx= 0.9 , x = 1 , y = 10  )
        # exit_butt.pack(side=TOP)










        Te.pack(side=TOP, anchor='n')
        e1.pack(side=TOP)

        Te1.pack(side=TOP, anchor='n')
        e2.pack(side=TOP)
        add_but.place(bordermode=OUTSIDE, rely=0.8, relx=0.8)


        self.mainloop()

    def __del__(self):
        #self.c.execute("DROP TABLE COSTS")

        print("See u Later ")


# Connect to db


if __name__ == "__main__":
    myapp = app_win()
    myapp.mainloop()
    del myapp
