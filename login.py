from tkinter import *
from PIL import ImageTk
from tkinter import messagebox
import sqlite3
import os
import email_pass
import smtplib
import time

class Login_System:
    # qwpc worv niuh wnah

    def __init__(self, root):
        self.root = root
        self.root.title("Login System")
        self.root.geometry("1750x700+0+0")
        self.root.config(bg="#fafafa")
        self.otp=''
        self.phone_image = ImageTk.PhotoImage(file="images/phone.png")
        self.lbl_Phone_image = Label(self.root, image=self.phone_image, bd=0).place(x=200, y=50)
        self.employee_id = StringVar()
        self.password = StringVar()
        login_frame = Frame(self.root, bg="white", highlightbackground="grey", highlightthickness=1, bd=2, relief=GROOVE)
        login_frame.place(x=650, y=90, width=350, height=460)
        title = Label(login_frame, text="Login System", font=("times new roman", 30, "bold"), bg="white", fg="black").place(x=0, y=30,relwidth=1)

        lbl_user = Label(login_frame, text="Employee ID", font=("Andalus", 15), bg="white", fg="#767171").place(x=50, y=100)
        txt_username = Entry(login_frame, font=("times new roman", 15),textvariable=self.employee_id, bg="#ECECEC").place(x=50, y=140, width=250)
        lbl_password = Label(login_frame, text="Password", font=("Andalus", 15), bg="white", fg="#767171").place(x=50, y=200)
        txt_password = Entry(login_frame, font=("times new roman", 15), bg="#ECECEC",show="*",textvariable=self.password).place(x=50, y=240, width=250)
        btn_login = Button(login_frame, text="Login",command=self.login, font=("Arial roundeed MT Bold", 15), bg="#00B0F0", fg="white", cursor="hand2",activebackground="#00B0F0",activeforeground="white").place(x=50, y=300, width=250, height=35)
        hr = Label (login_frame, bg="lightgray").place(x=50, y=370, width=250, height=2)
        or_ = Label(login_frame, text="OR", font=("times new roman", 15), bg="white", fg="lightgray").place(x=150, y=357)
        btn_forget= Button(login_frame, text="Forget Password?",command=self.forget_window ,font=("times new roman", 15), bg="white", fg="#00759E", cursor="hand2",bd=0,activeforeground="#00759E",activebackground="white").place(x=50, y=400 , width=250, height=30)
        register_frame = Frame(self.root, bg="white", highlightbackground="grey", highlightthickness=1, bd=2, relief=GROOVE)
        register_frame.place(x=650, y=570, width=350, height=60)
        # lbl_reg = Label(register_frame, text="Don't have an account?", font=("times new roman", 15), bg="white", fg="#767171").place(x=50, y=10)
        # btn_signup = Button(register_frame, text="Sign Up", font=("times new roman", 15,"bold"), bg="white", fg="#00759E", cursor="hand2",bd=0,activebackground="white",activeforeground="#00759E").place(x=235, y=7)

        self.im1 = ImageTk.PhotoImage(file="images/im1.png")
        self.im2 = ImageTk.PhotoImage(file="images/im2.png")
        self.im3 = ImageTk.PhotoImage(file= "images/im3.png")

        self.lbl_change_image = Label(self.root,bg="white")
        self.lbl_change_image.place(x=367, y=153, width=240, height=428)
        self.animate()
    def animate (self):
        self.im = self.im1
        self.im1 = self.im2
        self.im2 = self.im3
        self.im3 = self.im
        self.lbl_change_image.config(image=self.im)
        self.lbl_change_image.after(2000, self.animate)
    def login(self):
        con = sqlite3.connect(database=r"IMS.db")
        cur = con.cursor()
        try:
            if self.employee_id.get() == "" or self.password.get() == "":
                messagebox.showerror("Error", "All fields are required", parent=self.root)
            else:
                cur.execute("select utype from employee where eid=? and pass=?", (self.employee_id.get(), self.password.get()))
                user = cur.fetchone()
                if user == None:
                    messagebox.showerror("Error", "Invalid Username and Password", parent=self.root)
                else:
                    messagebox.showinfo("Success", "Welcome", parent=self.root)
                    if user[0] == "ADMIN":
                        self.root.destroy()
                        os.system("python dashboard.py")
                    else:
                        self.root.destroy()
                        os.system("python billing.py")
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

    def forget_window(self):
        con = sqlite3.connect(database=r"IMS.db")
        cur = con.cursor()
        try:
            if self.employee_id.get() == "":
                messagebox.showerror("Error", "Please enter Employee ID to reset password")
            else:
                cur.execute("select email from employee where eid=?", (self.employee_id.get(),))
                email = cur.fetchone()
                if email == None:
                    messagebox.showerror("Error", "Invalid Employee ID")
                else:
                    self.var_otp = StringVar()
                    self.var_new_pass = StringVar()
                    self.var_conf_pass = StringVar()
                    # call_send_email()
                    chk = self.send_email(email[0])
                    if chk=='f':
                        messagebox.showerror("Error", "Something went wrong", parent=self.root)
                    else:
                        self.forget_win= Toplevel(self.root)
                        self.forget_win.title("Forget Password")
                        self.forget_win.geometry("400x350+500+100")
                        self.forget_win.focus_force()
                        title = Label(self.forget_win, text="Reset Password", font=("goudy old style", 15, "bold"), bg="#3f51b5", fg="white").place(x=0, y=10, relwidth=1)
                        # self.forget_obj = ForgetPassword(self.forget_win)
                        lbl_reset = Label(self.forget_win, text="Enter OTP sent on regitser email", font=("times new roman", 15)).place(x=20, y=60)
                        txt_reset = Entry(self.forget_win, textvariable=self.var_otp, font=("times new roman", 15), bg="lightyellow").place(x=20, y=100, width=250,height =30)
                        self.btn_reset = (Button(self.forget_win, text="Submit",command=self.validate_otp, font=("times new roman", 15), bg="lightblue", fg="black", cursor="hand2"))
                        self.btn_reset .place(x=280, y=100, width=100, height=30)
                        lbl_new_pass = Label(self.forget_win, text="New Password", font=("times new roman", 15)).place(x=20, y=160)
                        txt_new_pass = Entry(self.forget_win, textvariable=self.var_new_pass, font=("times new roman", 15), bg="lightyellow").place(x=20, y=190, width=250,height =30)
                        lbl_conf_pass = Label(self.forget_win, text="Confirm Password", font=("times new roman", 15)).place(x=20, y=225)
                        txt_conf_pass = Entry(self.forget_win, textvariable=self.var_conf_pass, font=("times new roman", 15), bg="lightyellow").place(x=20, y=255, width=250,height =30)
                        self.btn_update = (Button(self.forget_win, text="Update",command=self.update_password,state=DISABLED, font=("times new roman", 15), bg="lightblue", fg="black", cursor="hand2"))
                        self.btn_update .place(x=150, y=300, width=100, height=30)


        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
    def send_email(self,to_):
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        email_= email_pass.email_
        pass_= email_pass.pass_
        s.login(email_, pass_)
        self.otp = int(time.strftime("%H%S%M"))+int(time.strftime("%S"))
        subj="OTP for Reset Password"
        msg=f"Subject:{subj}\n\nYour OTP is:{self.otp}\n\n\n With best regards \n Gunjan"
        msg = "Subject: {}\n\n{}".format(subj, msg)
        s.sendmail(email_,to_,msg)
        chk = s.ehlo()
        if chk[0]==250:
            # messagebox.showinfo("OTP", "OTP Sent")
            # self.btn_reset.config(state=NORMAL)
            # self.btn_update.config(state=NORMAL)
            # s.quit()
            return 's'
        else:
            # messagebox.showerror("Error", "Something went wrong")
            return 'f'

    def update_password(self):
        if self.var_new_pass.get()=='' or self.var_conf_pass.get()=='':
            messagebox.showerror("Error", "All fields are required", parent=self.forget_win)
        elif self.var_new_pass.get() != self.var_conf_pass.get():
            messagebox.showerror("Error", "Password Mismatch", parent=self.forget_win)
        else:
            try:
                con = sqlite3.connect(database=r'ims.db')
                cur = con.cursor()
                cur.execute("UPDATE employee SET pass=? WHERE eid=?", (self.var_new_pass.get(), self.employee_id.get(),))
                con.commit()
                con.close()
                messagebox.showinfo("Success", "Password updated successfully", parent=self.forget_win)
                self.forget_win.destroy()
            except Exception as ex:
                messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
    def validate_otp(self):
        if int(self.otp) == int(self.var_otp.get()):
            self.btn_reset.config(state=DISABLED)
            self.btn_update.config(state=NORMAL)
        else:
            messagebox.showerror("Error", "Invalid OTP", parent=self.forget_win)
if __name__ == "__main__":
    root = Tk()
    obj = Login_System(root)
    root.mainloop()

