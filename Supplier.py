import sqlite3
from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk, messagebox

class supplierClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System")
        self.root.config(bg='white')
        self.root.focus_force()

        # All variables
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()
        self.var_sup_invoice = StringVar()
        self.var_gender = StringVar()
        self.var_contact = StringVar()
        self.var_name = StringVar()
        self.var_dob = StringVar()
        self.var_doj = StringVar()
        self.var_email = StringVar()
        self.var_pass = StringVar()
        self.var_utype = StringVar()
        self.var_salary = StringVar()

        # Search Frame
        # self.root = LabelFrame(self.root, text="Search Supplier", font=("goudy old style", 12, "bold"), bd=2, relief=RIDGE, bg='white')
        # self.root.place(x=250, y=20, width=600, height=70)
        lbl_search = Label(self.root, text="Invoice no.",bg="white" , font=("goudy old style", 12, "bold"))
        lbl_search.place(x=700, y=80)
        txt_search = Entry(self.root, textvariable=self.var_searchtxt, font=("goudy old style", 15), bg="lightyellow").place(x=800, y=80,width=180, height=30)
        btn_search = Button(self.root, text="Search",command=self.search, font=("goudy old style", 15), bg="#4caf50", fg="white", cursor="hand2").place(x=980, y=79, width=100, height=28)

        # Title
        title = Label(self.root, text="Supplier Details", font=("goudy old style", 20,"bold"), bg="#0f4d7d", fg="white").place(x=50, y=10, width=1000,height=40)

        # Labels and Entry Fields
        lbl_invoice = Label(self.root, text="Invoice no.", font=("goudy old style", 15), bg="white").place(x=50, y=80)
        txt_invoice = Entry(self.root, textvariable=self.var_sup_invoice, font=("goudy old style", 15),bg="lightyellow").place(x=180, y=80, width=180)
        lbl_name = Label(self.root, text="Name", font=("goudy old style", 15), bg="white").place(x=50, y=120)
        txt_name = Entry(self.root, textvariable=self.var_name, font=("goudy old style", 15), bg="lightyellow").place(x=180, y=120, width=180)

        lbl_contact = Label(self.root, text="Contact", font=("goudy old style", 15), bg="white").place(x=50, y=160)


        txt_contact = Entry(self.root, textvariable=self.var_contact, font=("goudy old style", 15), bg="lightyellow").place(x=180, y=160, width=180)

        lbl_desc = Label(self.root, text="Description", font=("goudy old style", 15), bg="white").place(x=50, y=200)


        self.txt_desc = Text(self.root, font=("goudy old style", 15), bg="lightyellow")
        self.txt_desc.place(x=180, y=200, width=470, height=130)


        # Buttons
        btn_add = Button(self.root, command=self.add, text="Save", font=("goudy old style", 15), bg="#2196f3", fg="white", cursor="hand2").place(x=180, y=370, width=110, height=35)
        btn_update = Button(self.root, text="Update",command=self.update, font=("goudy old style", 15), bg="#4caf50", fg="white", cursor="hand2").place(x=300, y=370, width=110, height=35)
        btn_delete = Button(self.root, text="Delete",command=self.delete, font=("goudy old style", 15), bg="#f44336", fg="white", cursor="hand2").place(x=420, y=370, width=110, height=35)
        btn_clear = Button(self.root, text="Clear",command=self.clear, font=("goudy old style", 15), bg="#607d8b", fg="white", cursor="hand2").place(x=540, y=370, width=110, height=35)

        # Treeview for Supplier Data
        emp_frame = Frame(self.root, bd=3, relief=RIDGE)
        emp_frame.place(x=700, y=120, width=380, height=350)
        scrolly = Scrollbar(emp_frame, orient=VERTICAL)
        scrollx = Scrollbar(emp_frame, orient=HORIZONTAL)
        self.supplierTable = ttk.Treeview(emp_frame, columns=("invoice", "name", "contact", "desc"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.supplierTable.xview)
        scrolly.config(command=self.supplierTable.yview)
        self.supplierTable.heading("invoice", text="Invoice")
        self.supplierTable.heading("name", text="Name")

        self.supplierTable.heading("contact", text="Contact")

        self.supplierTable.heading("desc", text="Description")
        self.supplierTable["show"] = "headings"
        self.supplierTable.column("invoice", width=90)
        self.supplierTable.column("name", width=100)

        self.supplierTable.column("contact", width=100)

        self.supplierTable.column("desc", width=100)
        self.supplierTable.pack(fill=BOTH, expand=1)
        self.supplierTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()

    def add(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_sup_invoice.get() == "":
                messagebox.showerror("Error", "Invoice must be required", parent=self.root)
            else:
                cur.execute("select * from supplier where invoice=?", (self.var_sup_invoice.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "Invoice already exists, try a different one", parent=self.root)
                else:
                    cur.execute("insert into supplier (invoice, name, contact, desc) values (?, ?, ?, ?)",
                        (
                            self.var_sup_invoice.get(),
                            self.var_name.get(),


                            self.var_contact.get(),

                            self.txt_desc.get('1.0', END),

                        )
                    )
                    con.commit()
                    messagebox.showinfo("Success", "Supplier added successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    def show(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("select * from supplier")
            rows = cur.fetchall()
            self.supplierTable.delete(*self.supplierTable.get_children())
            for row in rows:
                self.supplierTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    def get_data(self, ev):
        f = self.supplierTable.focus()
        content = self.supplierTable.item(f)
        row = content['values']
        self.var_sup_invoice.set(row[0])
        self.var_name.set(row[1])
        self.var_contact.set(row[2])



        self.txt_desc.delete('1.0', END)
        self.txt_desc.insert(END, row[3])

    def update(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_sup_invoice.get() == "":
                messagebox.showerror("Error", "Invoice must be required", parent=self.root)
            else:
                cur.execute("select * from supplier where invoice=?", (self.var_sup_invoice.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "INVALID Invoice No., try a different one", parent=self.root)
                else:
                    cur.execute(
                        "update supplier set name=?,contact=?, desc=? where invoice =?",
                        (

                            self.var_name.get(),


                            self.var_contact.get(),

                            self.txt_desc.get('1.0', END),

                            self.var_sup_invoice.get()
                        )
                    )
                    con.commit()
                    messagebox.showinfo("Success", "Supplier updated successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()
    def clear(self):
        self.var_sup_invoice.set("")
        self.var_name.set("")

        self.var_contact.set("")

        self.txt_desc.delete('1.0',END)

        self.var_searchtxt.set("")

        self.show()

    def delete(self):
        con = sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
                if self.var_sup_invoice.get() == "":
                    messagebox.showerror("Error", "Invoice must be required", parent=self.root)
                else:
                    cur.execute("select * from supplier where  invoice=?", (self.var_sup_invoice.get(),))
                    row = cur.fetchone()
                    if row == None:
                        messagebox.showerror("Error", "INVALID invoice no., try a different one", parent=self.root)
                    else:
                        op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
                        if op == True:
                            cur.execute("delete from supplier where invoice =?",(self.var_sup_invoice.get(),))
                            con.commit()
                            messagebox.showinfo("Delete", "Supplier deleted successfully", parent=self.root)
                            self.clear()

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def search(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_searchtxt.get() == "":
                messagebox.showerror("Error", "Enter INVOICE to search", parent=self.root)
            else:
                # Prepare the query based on the selected search option
                cur.execute("SELECT * FROM supplier WHERE invoice =? ", (self.var_searchtxt.get(),))
                rows = cur.fetchone()
                if rows!= None:
                    self.supplierTable.delete(*self.supplierTable.get_children())
                    self.supplierTable.insert('', END, values=rows)
                else:
                     messagebox.showerror("Error", "Record not found", parent=self.root)



        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

if __name__ == "__main__":
    root = Tk()
    obj = supplierClass(root)
    root.mainloop()