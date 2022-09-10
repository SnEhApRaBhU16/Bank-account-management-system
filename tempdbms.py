import cx_Oracle
conn=cx_Oracle.connect('hr/hr@//localhost:1521/xe')
cur=conn.cursor()
from tkinter import *
from tkinter import messagebox as mb
from tkinter import ttk,Canvas
from PIL import Image,ImageTk
import tkinter as tk

login_screen=Tk()
login_screen.title("Login")
login_screen.geometry("1600x950")
login_screen.state('zoomed')
canvas=Canvas(login_screen,width=1600,height=950)
canvas.pack(fill = "both", expand = True)
canvas.img=ImageTk.PhotoImage(Image.open("bank1.jpg").resize((1600,950)))
canvas.create_image(0,0,image=canvas.img,anchor='nw')
# Create two frames in the window
admin_login = Frame(login_screen)
user_login= Frame(login_screen)
canvas.create_text(700,20,text="Please enter login details",font=("Calibri",28),fill="black")
username=tk.StringVar()
password=tk.StringVar()
# Define a function for switching the frames
def admin_field():
   admin_login.pack(fill='both', expand=1)
   user_login.pack_forget()
   Label(canvas, text="Admin Username",width="20",height="2",bg="black",fg='white',font=("Calibri",18,'bold')).place(x=500,y=150)
   t1=Entry(canvas, textvariable=username,font=("Calibri",20),bg="turquoise2")
   t1.place(x = 510,y = 250,width=280,height=45)
   Label(canvas, text="Admin Password",width="20",height="2",bg="black",fg='white',font=("Calibri",18,'bold')).place(x=500,y=380)
   t2=Entry(canvas, textvariable=password,show='*',font=("Calibri",20),bg="turquoise2")
   t2.place(x = 510,y = 480,width=280,height=45)
   b1=tk.Button(canvas, text="LOGIN",state='normal',command=lambda:validate())
   b1.configure(font=('calibri',22,'bold'),bg="black",fg="white",width=12)
   b1.place(x=550,y=575)
   user=username.get()
   pswd=password.get()
   def validate():
     nonlocal t1,t2
     user=username.get()
     pswd=password.get()
     if user=='admin' and pswd=='abcde':
       t1.delete(0,END)
       t2.delete(0,END)
       AdminWindow(b1,0,admin_login,0)
     else:
       mb.showwarning("showwarning","wrong entry!!!",parent=login_screen)
   admin_login.mainloop()

custid=StringVar()
card_no=StringVar()
def user_field():
   conn=cx_Oracle.connect('hr/hr@//localhost:1521/xe')
   cur=conn.cursor()
   user_login.pack(fill='both', expand=1)
   admin_login.pack_forget()
   dct={}
   cur.execute('SELECT CARD_NO,CUST_ID FROM ATM_CARD')
   for row in cur:
      dct[str(row[0])]=row[1]
   conn.commit()
   Label(canvas, text="Customer Id",width="20",height="2",bg="black",fg='white',font=("Calibri",18,'bold')).place(x=500,y=150)
   t1=Entry(canvas, textvariable=custid,font=("Calibri",20),bg="turquoise2")
   t1.place(x = 510,y = 250,width=280,height=45)
   Label(canvas, text="Customer Card no.",width="20",height="2",bg="black",fg='white',font=("Calibri",18,'bold')).place(x=500,y=380)
   t2=Entry(canvas, textvariable=card_no,show='*',font=("Calibri",20),bg="turquoise2")
   t2.place(x = 510,y = 480,width=280,height=45)
   b1=tk.Button(canvas, text="LOGIN",state='normal',command=lambda:validate())
   b1.configure(font=('calibri',22,'bold'),bg="black",fg="white",width=12)
   b1.place(x=550,y=575)
   cur.close()
   conn.close()
   def validate():
     nonlocal t1,t2,b1
     cid=custid.get()
     num=card_no.get()
     if cid=='' or num=='':
       mb.showwarning("showwarning","Enter info!!!",parent=login_screen)
     elif (str(cid) not in str(dct.values())) or (str(num) not in str(dct.keys())) or str(cid)!=str(dct[num]): 
       mb.showwarning("showwarning","wrong entry!!!",parent=login_screen)
     elif (str(dct[num]))==str(cid) :
       t1.delete(0,END)
       t2.delete(0,END)
       UserWindow(b1,cid,num)
   user_login.mainloop()

# Add a button to switch between two frames
btn1=tk.Button(login_screen, text="Admin Login",command=lambda:admin_field())
btn1.configure(font=('calibri',20,'bold'),bg="black",fg="white",width=16)
btn1.place(x=30,y=50)
btn2=tk.Button(login_screen, text="User Login",command=lambda:user_field())
btn2.configure(font=('calibri',20,'bold'),bg="black",fg="white",width=16)
btn2.place(x=290,y=50)

def Main_page(b1,window):
       b1["state"]='normal'
       window.destroy()
def UserWindow(b1,cid,num):
   conn=cx_Oracle.connect('hr/hr@//localhost:1521/xe')
   cur=conn.cursor()
   b1["state"]="disabled"
   win = Toplevel(login_screen)
   win.title("CUSTOMER INFO")
   win.geometry("1600x950")
   win.configure(bg="black")
   win.state('zoomed')
   style = ttk.Style(win)
   style.theme_use('clam')
   style.configure("Treeview",background="silver",foreground="silver",rowheight=25,fieldbackground="silver")
   style.map("Treeview",background=[('selected','purple')])
   tabControl = ttk.Notebook(win)
   tabControl.place(x=0,y=0)
   def cust():
      nonlocal cid
      tab1=ttk.Frame(tabControl,width=1700,height=690)
      canvas=Canvas(tab1,width=1600,height=950)
      canvas.pack(fill = "both", expand = True)
      canvas.img=ImageTk.PhotoImage(Image.open("bank11.jpg").resize((1600,950)))
      canvas.create_image(0,0,image=canvas.img,anchor='nw')
      tab1_win=canvas.create_window(0,70,anchor="nw",window=tab1)
      tab1.place(x=0,y=70)
      tabControl.add(tab1, text ='CUSTOMER')
      cust_id=tk.StringVar()
      cust_name=tk.StringVar()
      state=tk.StringVar()
      city=tk.StringVar()
      street=tk.StringVar()
      gender=tk.StringVar()
      tree= ttk.Treeview(tab1,selectmode='browse',show='headings',height=3)
      tree.place(x=160,y=103)
      tree["columns"]=("1","2","3","4","5","6")
      tree.heading("1", text = "CUST_ID")
      tree.heading("2", text = "CUST_NAME")
      tree.heading("3", text = "STREET")
      tree.heading("4", text = "CITY")
      tree.heading("5", text = "STATE")
      tree.heading("6", text = "GENDER")
      stmt='SELECT * FROM CUSTOMER WHERE CUST_ID=:1'
      cur.execute(stmt,{'1':cid})
      for row in cur:
        tree.insert('',0,text="",values=(row[0],row[1],row[2],row[3],row[4],row[5]))
      conn.commit()
      def update(tree):
       selected_item=tree.focus()
       if not tree.focus():
            mb.showwarning("showwarning","Select a row",parent=win)
       else:
        updatebtn["state"]="disabled"
        values=tree.item(selected_item,"values")
        f=Frame(tab1,width=400,height=320,background="white")
        f.place(x=100,y=250)

        l2=Label(f,text="CUST_NAME",width=10,font=('Times',11,'bold'))
        e2=Entry(f,textvariable=cust_name,width=25)
        l2.place(x=50,y=70)
        e2.place(x=170,y=70,height=25)

        l3=Label(f,text="STREET",width=8,font=('Times',11,'bold'))
        e3=Entry(f,textvariable=street,width=25)
        l3.place(x=50,y=110)
        e3.place(x=170,y=110,height=25)

        l4=Label(f,text="CITY",width=8,font=('Times',11,'bold'))
        e4=Entry(f,textvariable=city,width=25)
        l4.place(x=50,y=150)
        e4.place(x=170,y=150,height=25)

        l5=Label(f,text="STATE",width=8,font=('Times',11,'bold'))
        e5=Entry(f,textvariable=state,width=25)
        l5.place(x=50,y=190)
        e5.place(x=170,y=190,height=25)

        l6=Label(f,text="GENDER",width=8,font=('Times',11,'bold'))
        e6=Entry(f,textvariable=gender,width=25)
        l6.place(x=50,y=230)
        e6.place(x=170,y=230,height=25)
        e2.insert(0,values[1])
        e3.insert(0,values[2])
        e4.insert(0,values[3])
        e5.insert(0,values[4])
        e6.insert(0,values[5])
        def destroy(f):
           e2.delete(0,END)
           e3.delete(0,END)
           e4.delete(0,END)
           e5.delete(0,END)
           e6.delete(0,END)
           f.destroy()
           updatebtn["state"]="normal"
        def  update_data():
           nonlocal values,e2,e3,e4,e5,e6,selected_item,values
           name=cust_name.get()
           cust_id=values[0]
           cty=city.get()
           st=state.get()
           strt=street.get()
           gen=gender.get()
           if name=="":
               mb.showwarning("warning","ENTER CUSTOMER NAME",parent=win)
           elif gen=="":
               mb.showwarning("warning","ENTER CUSTOMER GENDER",parent=win)
           elif len(gen)!=1:
              mb.showwarning("warning","ENTER EITHER 'M' OR 'F'",parent=window)
           else:
            stmt2='UPDATE CUSTOMER SET CUST_NAME=:2,STREET=:3,CITY=:4,STATE=:5,GENDER=:6 WHERE CUST_ID=:1'
            cur.execute(stmt2,(name,strt,cty,st,gen,cust_id))
            conn.commit()
            tree.item(selected_item,values=(cust_id,name,strt,cty,st,gen))
            mb.showinfo("success","information updated!!",parent=win)
            destroy(f)
           
        savebtn=tk.Button(f,text="Update",command=update_data)
        savebtn.configure(font=('Times',11,'bold'),bg='green',fg='white')
        savebtn.place(x=120,y=260)

        cancelbtn=tk.Button(f,text="Cancel",command=lambda:destroy(f))
        cancelbtn.configure(font=('Times',11,'bold'),bg='red',fg='white')
        cancelbtn.place(x=240,y=260)
         
      updatebtn=tk.Button(tab1,text="UPDATE",command=lambda:update(tree))
      updatebtn.configure(font=('calibri',18,'bold'),bg='black',fg='white')
      updatebtn.place(x=490,y=340)
   def phonenumber():
     nonlocal cid
     tab2=ttk.Frame(tabControl,width=1700,height=690)
     canvas=Canvas(tab2,width=1600,height=950)
     canvas.pack(fill = "both", expand = True)
     canvas.img=ImageTk.PhotoImage(Image.open("bank12.jpg").resize((1600,800)))
     canvas.create_image(0,0,image=canvas.img,anchor='nw')
     tab2_win=canvas.create_window(0,70,anchor="nw",window=tab2)
     tab2.place(x=0,y=70)
     tabControl.add(tab2, text ='PHONE_NO')
     tree = ttk.Treeview(tab2,selectmode='browse', height = 4)
     tree["columns"]=("1","2")
     tree["show"]='headings'
     tree.column("1", anchor = CENTER,stretch=NO,width=350)
     tree.column("2", anchor = CENTER,stretch=NO,width=350)
     tree.place(x=430,y=210)
     tree.heading("1", text = "PHONE_NO")
     tree.heading("2", text = "CUST_ID")
     sb = ttk.Scrollbar(tab2, orient=VERTICAL)
     sb.place(x=1115,y=210,width=20,height=129)
     tree.config(yscrollcommand=sb.set)
     sb.config(command=tree.yview) 
     stmt='SELECT * FROM PHONE_NO WHERE CUST_ID=:1'
     cur.execute(stmt,{'1':cid})
     i=0
     for row in cur:
        tree.insert('',i,text="",values=(row[0],row[1]))
        i+=1
     conn.commit()
     phone_no=tk.IntVar()
     cust_id=tk.StringVar()
     def insert(tree):
       insertbtn["state"]="disabled"
       f=Frame(win,width=400,height=320,background="white")
       f.place(x=100,y=250)
       l1=Label(f,text="PHONE_NO",width=12,font=('Times',11,'bold'))
       e1=Entry(f,textvariable=phone_no,width=28)
       l1.place(x=50,y=30)
       e1.place(x=170,y=30,height=25)
       e1.delete(0,END)
       def destroy(f):
         e1.delete(0,END)
         f.destroy()
         insertbtn["state"]="normal"
       def insert_data():
         nonlocal e1
         phone=phone_no.get()
         if phone=="":
               mb.showwarning("warning","ENTER PHONE NUMBER",parent=win)
         elif len(str(phone))!=10:
               mb.showwarning("warning","ENTER 10 DIGIT PHONE NUMBER!",parent=win)
         else:
          stmt='INSERT INTO PHONE_NO VALUES(:1,:2)'
          cur.execute(stmt,(phone,cid))
          conn.commit()
          tree.insert('','end',text="",values=(phone,cid),tags=('odd',))
          mb.showinfo("Success","successfully inserted!!",parent=win)
          destroy(f)
     
       submitbtn=tk.Button(f,text="submit",command=insert_data)
       submitbtn.configure(font=('Times',11,'bold'),bg='green',fg='white')
       submitbtn.place(x=120,y=260)

       cancelbtn=tk.Button(f,text="cancel",command=lambda:destroy(f))
       cancelbtn.configure(font=('Times',11,'bold'),bg='red',fg='white')
       cancelbtn.place(x=240,y=260)

     def delete(tree):
         if not tree.selection():
            mb.showwarning("showwarning","Select a row",parent=win)
         else:
          selected_item=tree.selection()[0]
          ph=tree.item(selected_item)['values'][0]
          cid=tree.item(selected_item)['values'][1]
          del1="DELETE FROM PHONE_NO WHERE CUST_ID=:id and PHONE_NO=:2"
          cur.execute(del1,(cid,ph))
          conn.commit()
          tree.delete(selected_item)
          mb.showinfo("success","information deleted!!",parent=win)
     def update(tree):
        selected_item=tree.focus()
        if not tree.focus():
            mb.showwarning("showwarning","Select a row",parent=win)
        else:
         updatebtn["state"]="disabled"
         values=tree.item(selected_item,"values")
         f=Frame(tab2,width=400,height=320,background="white")
         f.place(x=100,y=250)
         l1=Label(f,text="PHONE_NO",width=10,font=('Times',11,'bold'))
         e1=Entry(f,textvariable=phone_no,width=25)
         l1.place(x=50,y=30)
         e1.place(x=170,y=30,height=25)
         e1.insert(0,values[0])
         def destroy(f):
            e1.delete(0,END)
            f.destroy()
            updatebtn["state"]="normal"
         def update_data():
           nonlocal values,e1,selected_item,values
           phone=phone_no.get()
           cid=values[1]
           if  phone=="":
               mb.showwarning("warning","ENTER PHONE NUMBER",parent=win)
           elif len(str(phone))!=10:
               mb.showwarning("warning","ENTER 10 DIGIT PHONE NUMBER",parent=win)
           else:
            stmt2='UPDATE PHONE_NO SET PHONE_NO=:1 WHERE CUST_ID=:2'
            cur.execute(stmt2,(phone,cid))
            conn.commit()
            tree.item(selected_item,values=(phone,cid))
            mb.showinfo("success","information updated!!",parent=win)
            destroy(f)

         savebtn=tk.Button(f,text="Update",command=update_data)
         savebtn.configure(font=('calibri',11,'bold'),bg='blue',fg='white')
         savebtn.place(x=120,y=260)

         cancelbtn=tk.Button(f,text="Cancel",command=lambda:destroy(f))
         cancelbtn.configure(font=('Times',11,'bold'),bg='red',fg='white')
         cancelbtn.place(x=240,y=260)
     insertbtn=tk.Button(tab2,text="INSERT",command=lambda:insert(tree))
     insertbtn.configure(font=('calibri',18,'bold'),bg='black',fg='white')
     insertbtn.place(x=500,y=400)

     deletebtn=tk.Button(tab2,text="DELETE",command=lambda:delete(tree))
     deletebtn.configure(font=('calibri',18,'bold'),bg='black',fg='white')
     deletebtn.place(x=600,y=400)

     updatebtn=tk.Button(tab2,text="UPDATE",command=lambda:update(tree))
     updatebtn.configure(font=('calibri',18,'bold'),bg='black',fg='white')
     updatebtn.place(x=700,y=400)   
     
   def account():
     nonlocal cid
     tab3=ttk.Frame(tabControl,width=1700,height=690)
     canvas=Canvas(tab3,width=1600,height=950)
     canvas.pack(fill = "both", expand = True)
     canvas.img=ImageTk.PhotoImage(Image.open("bank13.jpg").resize((1600,950)))
     canvas.create_image(0,0,image=canvas.img,anchor='nw')
     tab3_win=canvas.create_window(0,70,anchor="nw",window=tab3)
     tab3.place(x=0,y=70)
     tabControl.add(tab3, text ='ACCOUNTS')
     tree = ttk.Treeview(tab3,selectmode='browse',height = 5)
     tree.place(x=120,y=200)
     tree["columns"]=("1","2","3","4","5","6","7","8")
     tree["show"]='headings'
     tree.column("1", anchor = CENTER,stretch=NO,width=130)
     tree.column("2", anchor = CENTER,stretch=NO,width=130)
     tree.column("3", anchor = CENTER,stretch=NO,width=130)
     tree.column("4", anchor = CENTER,stretch=NO,width=130)
     tree.column("5", anchor = CENTER,stretch=NO,width=130)
     tree.column("6", anchor = CENTER,stretch=NO,width=130)
     tree.column("7", anchor = CENTER,stretch=NO,width=130)
     tree.column("8", anchor = CENTER,stretch=NO,width=150)
     tree.heading("1", text = "CUST_ID")
     tree.heading("2", text = "ACC_NO")
     tree.heading("3", text = "OPEN_DATE")
     tree.heading("4", text = "ACC_BALANCE")
     tree.heading("5", text = "INTEREST_AMT")
     tree.heading("6", text = "TRANSACTION_LIMIT")
     tree.heading("7", text = "MIN_BAL_AMT")
     tree.heading("8", text = "BUSINESS_TRANSAC_NO")
     sb = ttk.Scrollbar(tab3, orient=VERTICAL)
     sb.place(x=1180,y=200,width=20,height=154)
     tree.config(yscrollcommand=sb.set)
     sb.config(command=tree.yview) 
     stmt='SELECT CUST_ID,ACC_NO,TO_CHAR(OPEN_DATE),ACC_STATUS,INTEREST_AMT,TRANSACTION_LIMIT,MIN_BALANCE_AMT,BUSINESS_TRANSAC_NO FROM ACCOUNTS WHERE CUST_ID=:1'
     cur.execute(stmt,{'1':cid})
     i=0
     for row in cur:
        tree.insert('',i,text="",values=(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7]))
        i+=1
     conn.commit()
   def AtmCard():
     nonlocal num
     tab4=ttk.Frame(tabControl,width=1700,height=690)
     canvas=Canvas(tab4,width=1600,height=950)
     canvas.pack(fill = "both", expand = True)
     canvas.img=ImageTk.PhotoImage(Image.open("bank14.webp").resize((1600,950)))
     canvas.create_image(0,0,image=canvas.img,anchor='nw')
     tab4_win=canvas.create_window(0,70,anchor="nw",window=tab4)
     tab4.place(x=0,y=70)
     tabControl.add(tab4, text ='ATM_CARD')
     tree = ttk.Treeview(tab4, height = 3)
     tree["columns"]=("1","2","3","4","5")
     tree['show']='headings'
     tree.place(x=160,y=150)
     tree.heading("1", text = "CARD_NO")
     tree.heading("2", text = "LIMIT")
     tree.heading("3", text = "BEGIN_DATA")
     tree.heading("4", text = "EXPIRY_DATA")
     tree.heading("5", text = "CUST_ID")
     stmt="SELECT CARD_NO,LIMIT,TO_CHAR(BEGIN_DATE,'DD-MM-YYYY'),TO_CHAR(EXPIRY_DATE,'DD-MM-YYYY'),CUST_ID FROM ATM_CARD WHERE CARD_NO=:1"
     cur.execute(stmt,{'1':num})
     for row in cur:
        tree.insert('',0,text="",values=(row[0],row[1],row[2],row[3],row[4]))
     conn.commit()
   def Transaction():
     nonlocal num
     tab5=ttk.Frame(tabControl,width=1700,height=690)
     canvas=Canvas(tab5,width=1600,height=950)
     canvas.pack(fill = "both", expand = True)
     canvas.img=ImageTk.PhotoImage(Image.open("bank15.jpg").resize((1600,950)))
     canvas.create_image(0,0,image=canvas.img,anchor='nw')
     tab5_win=canvas.create_window(0,70,anchor="nw",window=tab5)
     tab5.place(x=0,y=70)
     tabControl.add(tab5, text ='TRANSACTIONS')
     tree = ttk.Treeview(tab5,selectmode="browse",height = 5)
     tree["columns"]=("1","2","3","4","5","6")
     tree['show']='headings'
     tree.place(x=200,y=240)
     tree.heading("1", text = "TRANSACTION_NO")
     tree.heading("2", text = "TRANSACTION_DATE")
     tree.heading("3", text = "DEPOSIT_CASH")
     tree.heading("4", text = "WITHDRAW_CASH")
     tree.heading("5", text = "CARD_NO")
     tree.heading("6", text = "ACC_NO")
     sb = ttk.Scrollbar(tab5, orient=VERTICAL)
     sb.place(x=1400,y=240,width=20,height=153)
     tree.config(yscrollcommand=sb.set)
     sb.config(command=tree.yview) 
     stmt="SELECT TRANSACTION_NO,TO_CHAR(TRANSACTION_DATE,'DD-MM-YYYY'),DEPOSIT_CASH,WITHDRAW_CASH,CARD_NO,ACC_NO FROM TRANSACTIONS WHERE CARD_NO=:1"
     cur.execute(stmt,{'1':num})
     i=0
     for row in cur:
        tree.insert('',i,text="",values=(row[0],row[1],row[2],row[3],row[4],row[5]))
        i+=1
     conn.commit()
   Button(win, text="BACK",bg="floral white",fg="black",activebackground = "white",width=8,font=('Calibri',18,'bold') ,command=lambda:Main_page(b1,win)).place(x=1423,y=3)
   cust()
   phonenumber()
   account()
   AtmCard()
   Transaction()
   win.mainloop()
   cur.close()
   conn.close()
def AdminWindow(b1,x,f,p):
    conn=cx_Oracle.connect('hr/hr@//localhost:1521/xe')
    cur=conn.cursor()
    b1["state"]="disabled"
    window = Toplevel(login_screen)
    window.title("Bank Account Management")
    window.geometry("1600x950")
    window.configure(bg="black")
    window.state('zoomed')
    tabControl = ttk.Notebook(window)
    tabControl.place(x=0,y=0)
    tab1=Frame(tabControl,width=1600,height=690)
    tab2=ttk.Frame(tabControl,width=1700,height=690)
    tab3=ttk.Frame(tabControl,width=1700,height=690)
    tab4=ttk.Frame(tabControl,width=1700,height=690)
    tab5=ttk.Frame(tabControl,width=1700,height=690)
    tab6=ttk.Frame(tabControl,width=1700,height=690)
    tab7=ttk.Frame(tabControl,width=1700,height=690)
    tab8=ttk.Frame(tabControl,width=1700,height=690)
    tab9=ttk.Frame(tabControl,width=1700,height=690)
    lcst=[]
    lcst1=[]
    lcst2=[]
    laccno=[]
    latmno=[]
    lcno=[]
    lbcode=[]
    ltranno=[]
    laccntno=[]
    def Customer():
     canvas=Canvas(tab1,width=1600,height=950)
     canvas.pack(fill = "both", expand = True)
     canvas.img=ImageTk.PhotoImage(Image.open("bank2.jpg").resize((1600,950)))
     canvas.create_image(0,0,image=canvas.img,anchor='nw')
     tab1_win=canvas.create_window(0,70,anchor="nw",window=tab1)
     style = ttk.Style()
     style.theme_use('clam')
     style.configure("Treeview",background="white",foreground="black",rowheight=25,fieldbackground="white")
     style.map("Treeview",background=[('selected','purple')])
     tabControl.add(tab1,text ='CUSTOMER')
     # Add a Treeview widget
     tree = ttk.Treeview(tab1,selectmode='browse',height=6,style="mystyle.Treeview")
     tree.place(x=160,y=173)
     tree["columns"]=("1","2","3","4","5","6")
     tree["show"]='headings'
     tree.heading("1", text = "CUST_ID")
     tree.heading("2", text = "CUST_NAME")
     tree.heading("3", text = "STREET")
     tree.heading("4", text = "CITY")
     tree.heading("5", text = "STATE")
     tree.heading("6", text = "GENDER")
     cur.execute('SELECT * FROM CUSTOMER')
     tree.tag_configure('odd',background="honeydew3")
     tree.tag_configure('even',background="honeydew2")
     i=0
     for row in cur:
       if i%2==0:
        tree.insert('',i,text="",values=(row[0],row[1],row[2],row[3],row[4],row[5]),tags=('odd',))
        lcst.append(str(row[0]))
       else:
        tree.insert('',i,text="",values=(row[0],row[1],row[2],row[3],row[4],row[5]),tags=('even',))
        lcst.append(str(row[0]))
       i+=1
     conn.commit() 
     sb = ttk.Scrollbar(tab1, orient=VERTICAL,command=tree.yview)
     sb.place(x=1360,y=175,width=20,height=176)
     tree.config(yscrollcommand=sb.set)
     cust_id=tk.StringVar()
     cust_name=tk.StringVar()
     state=tk.StringVar()
     city=tk.StringVar()
     street=tk.StringVar()
     gender=tk.StringVar()
     def insert(tree):
       insertbtn["state"]="disabled"
       f=Frame(tab1,width=400,height=320,background="white")
       f.place(x=100,y=250)
       l1=Label(f,text="CUST_ID",width=8,font=('Times',11,'bold'))
       e1=Entry(f,textvariable=cust_id,width=25)
       l1.place(x=50,y=30)
       e1.place(x=170,y=30,height=25)

       l2=Label(f,text="CUST_NAME",width=10,font=('Times',11,'bold'))
       e2=Entry(f,textvariable=cust_name,width=25)
       l2.place(x=50,y=70)
       e2.place(x=170,y=70,height=25)

       l3=Label(f,text="STREET",width=8,font=('Times',11,'bold'))
       e3=Entry(f,textvariable=street,width=25)
       l3.place(x=50,y=110)
       e3.place(x=170,y=110,height=25)

       l4=Label(f,text="CITY",width=8,font=('Times',11,'bold'))
       e4=Entry(f,textvariable=city,width=25)
       l4.place(x=50,y=150)
       e4.place(x=170,y=150,height=25)

       l5=Label(f,text="STATE",width=8,font=('Times',11,'bold'))
       e5=Entry(f,textvariable=state,width=25)
       l5.place(x=50,y=190)
       e5.place(x=170,y=190,height=25)

       l6=Label(f,text="GENDER",width=8,font=('Times',11,'bold'))
       e6=Entry(f,textvariable=gender,width=25)
       l6.place(x=50,y=230)
       e6.place(x=170,y=230,height=25)

       def destroy(f):
         e1.delete(0,END)
         e2.delete(0,END)
         e3.delete(0,END)
         e4.delete(0,END)
         e5.delete(0,END)
         e6.delete(0,END)
         f.destroy()
         insertbtn["state"]="normal"
       
       def insert_data():
         nonlocal e1,e2,e3,e4,e5,e6,i
         cid=cust_id.get()
         name=cust_name.get()
         cty=city.get()
         st=state.get()
         strt=street.get()
         gen=gender.get()
         if cid=="" :
               mb.showwarning("warning","ENTER CUSTOMER ID ",parent=window)
         elif cid in lcst:
               mb.showwarning("warning","CUSTOMER_ID  ALREADY EXISTS",parent=window)
         elif name=="":
               mb.showwarning("warning","ENTER CUSTOMER NAME ",parent=window)
         elif gen=="":
               mb.showwarning("warning","ENTER CUSTOMER GENDER",parent=window)
         elif len(gen)!=1:
              mb.showwarning("warning","ENTER EITHER 'M' OR 'F'",parent=window)
         else:
          stmt='INSERT INTO CUSTOMER VALUES(:1,:2,:3,:4,:5,:6)'
          cur.execute(stmt,(cid,name,strt,cty,st,gen))
          conn.commit()
          if i%2==0:
           tree.insert('','end',text="",values=(cid,name,strt,cty,st,gen),tags=('odd',))
           lcst.append(str(cid))
          else:
           tree.insert('','end',text="",values=(cid,name,strt,cty,st,gen),tags=('even',))
           lcst.append(str(cid))
          i+=1
          mb.showinfo("Success","successfully inserted!!",parent=window)
          destroy(f)
         
       submitbtn=tk.Button(f,text="submit",command=insert_data)
       submitbtn.configure(font=('Times',11,'bold'),bg='green',fg='white')
       submitbtn.place(x=120,y=260)

       cancelbtn=tk.Button(f,text="cancel",command=lambda:destroy(f))
       cancelbtn.configure(font=('Times',11,'bold'),bg='red',fg='white')
       cancelbtn.place(x=240,y=260)

     def delete(tree):
         nonlocal i
         if not tree.selection():
            mb.showwarning("showwarning","Select a row",parent=window)
         else:
          selected_item=tree.selection()[0]
          cid=tree.item(selected_item)['values'][0]
          del1="DELETE FROM CUSTOMER WHERE CUST_ID=:id"
          cur.execute(del1,{'id':cid})
          conn.commit()
          lcst.remove(str(cid))
          tree.delete(selected_item)
          mb.showinfo("success","information deleted!!",parent=window)
          i-=1
          Refresh(b1,window,0)
     def update(tree):
      if not tree.focus():
            mb.showwarning("showwarning","Select a row",parent=window)
      else:
         updatebtn["state"]="disabled"
         selected_item=tree.focus()
         values=tree.item(selected_item,"values")
         f=Frame(tab1,width=400,height=320,background="white")
         f.place(x=100,y=250)
         l1=Label(f,text="CUST_ID",width=8,font=('Times',11,'bold'))
         e1=Entry(f,textvariable=cust_id,width=25)
         l1.place(x=50,y=30)
         e1.place(x=170,y=30,height=25)

         l2=Label(f,text="CUST_NAME",width=10,font=('Times',11,'bold'))
         e2=Entry(f,textvariable=cust_name,width=25)
         l2.place(x=50,y=70)
         e2.place(x=170,y=70,height=25)

         l3=Label(f,text="STREET",width=8,font=('Times',11,'bold'))
         e3=Entry(f,textvariable=street,width=25)
         l3.place(x=50,y=110)
         e3.place(x=170,y=110,height=25)

         l4=Label(f,text="CITY",width=8,font=('Times',11,'bold'))
         e4=Entry(f,textvariable=city,width=25)
         l4.place(x=50,y=150)
         e4.place(x=170,y=150,height=25)

         l5=Label(f,text="STATE",width=8,font=('Times',11,'bold'))
         e5=Entry(f,textvariable=state,width=25)
         l5.place(x=50,y=190)
         e5.place(x=170,y=190,height=25)

         l6=Label(f,text="GENDER",width=8,font=('Times',11,'bold'))
         e6=Entry(f,textvariable=gender,width=25)
         l6.place(x=50,y=230)
         e6.place(x=170,y=230,height=25)
      
         e1.insert(0,values[0])
         e2.insert(0,values[1])
         e3.insert(0,values[2])
         e4.insert(0,values[3])
         e5.insert(0,values[4])
         e6.insert(0,values[5])
         e1["state"]="disabled"
         def destroy(f):
           e1.configure(state="normal")
           e1.delete(0,END)
           e2.delete(0,END)
           e3.delete(0,END)
           e4.delete(0,END)
           e5.delete(0,END)
           e6.delete(0,END)
           f.destroy()
           updatebtn["state"]="normal"
         def  update_data():
           nonlocal e1,e2,e3,e4,e5,e6,selected_item,values
           cuid=cust_id.get()
           name=cust_name.get()
           cty=city.get()
           st=state.get()
           strt=street.get()
           gen=gender.get()
           if name=="":
               mb.showwarning("warning","ENTER CUSTOMER NAME",parent=window)
           elif gen=="":
               mb.showwarning("warning","ENTER CUSTOMER GENDER",parent=window)
           else:
            stmt2='UPDATE CUSTOMER SET CUST_NAME=:2,STREET=:3,CITY=:4,STATE=:5,GENDER=:6 WHERE CUST_ID=:1'
            cur.execute(stmt2,(name,strt,cty,st,gen,cuid))
            conn.commit()
            tree.item(selected_item,values=(cuid,name,strt,cty,st,gen))
            mb.showinfo("success","information updated!!",parent=window)
            destroy(f)

         savebtn=tk.Button(f,text="Update",command=update_data)
         savebtn.configure(font=('Times',11,'bold'),bg='green',fg='white')
         savebtn.place(x=120,y=260)

         cancelbtn=tk.Button(f,text="Cancel",command=lambda:destroy(f))
         cancelbtn.configure(font=('Times',11,'bold'),bg='red',fg='white')
         cancelbtn.place(x=240,y=260)
         
     insertbtn=tk.Button(tab1,text="INSERT",command=lambda:insert(tree))
     insertbtn.configure(font=('calibri',18,'bold'),bg='black',fg="white")
     insertbtn.place(x=200,y=400)

     deletebtn=tk.Button(tab1,text="DELETE",command=lambda:delete(tree))
     deletebtn.configure(font=('calibri',18,'bold'),bg='black',fg="white")
     deletebtn.place(x=300,y=400)

     updatebtn=tk.Button(tab1,text="UPDATE",command=lambda:update(tree))
     updatebtn.configure(font=('calibri',18,'bold'),bg='black',fg="white")
     updatebtn.place(x=400,y=400)
    def Phone_no():
     canvas=Canvas(tab2,width=1600,height=950)
     canvas.pack(fill = "both", expand = True)
     canvas.img=ImageTk.PhotoImage(Image.open("bank3.webp").resize((1600,950)))
     canvas.create_image(0,0,image=canvas.img,anchor='nw')
     tab2_win=canvas.create_window(0,70,anchor="nw",window=tab2)
     style = ttk.Style()
     style.theme_use('clam')
     style.configure("Treeview",background="white",foreground="black",rowheight=25,fieldbackground="white")
     style.map("Treeview",background=[('selected','purple')])
     tabControl.add(tab2, text ='PHONE NUMBER')
     # Add a Treeview widget
     tree = ttk.Treeview(tab2,selectmode='browse', height = 6)
     tree["columns"]=("1","2")
     tree["show"]='headings'
     tree.column("1", anchor = CENTER,stretch=NO,width=240)
     tree.column("2", anchor = CENTER,stretch=NO,width=250)
     tree.place(x=490,y=173)
     tree.heading("1", text = "PHONE_NO")
     tree.heading("2", text = "CUST_ID")
     cur.execute('SELECT * FROM PHONE_NO')
     tree.tag_configure('odd',background="LightPink3")
     tree.tag_configure('even',background="LightPink2")
     i=0
     for row in cur:
      if i%2==0:
        tree.insert('',i,text="",values=(row[0],row[1]),tags=('odd',))
      else:
        tree.insert('',i,text="",values=(row[0],row[1]),tags=('even',))
      i+=1
     conn.commit()
     sb = ttk.Scrollbar(tab2, orient=VERTICAL)
     sb.place(x=982,y=172,width=20,height=179)

     tree.config(yscrollcommand=sb.set)
     sb.config(command=tree.yview)

     phone_no=tk.StringVar()
     cust_id=tk.StringVar()
     
     def insert(tree):
       insertbtn["state"]="disabled"
       f=Frame(window,width=400,height=320,background="white")
       f.place(x=100,y=250)
       l1=Label(f,text="PHONE_NO",width=12,font=('Times',11,'bold'))
       e1=Entry(f,textvariable=phone_no,width=28)
       l1.place(x=50,y=30)
       e1.place(x=170,y=30,height=25)
       e1.delete(0,END)
       l2=Label(f,text="CUST_ID",width=10,font=('Times',11,'bold'))
       l2.place(x=50,y=70)
       e2=ttk.Combobox(f,value=lcst,textvariable=cust_id,state="readonly",width=25,height=5)
       e2.place(x=170,y=70)
       def destroy(f):

         e1.delete(0,END)
         e2["state"]="normal"
         e2.delete(0,END)
         f.destroy()
         insertbtn["state"]="normal"
       def insert_data():
         nonlocal e1,e2,i
         phone=phone_no.get()
         cid=cust_id.get()
         if cid=="" or phone=="":
               mb.showwarning("warning","ENTER ALL VALUES",parent=window)
         elif len(str(phone))!=10:
               mb.showwarning("warning","ENTER 10 DIGIT PHONE NUMBER!",parent=window)
         else:
          stmt='INSERT INTO PHONE_NO VALUES(:1,:2)'
          cur.execute(stmt,(phone,cid))
          conn.commit()
          tree.insert('','end',text="",values=(phone,cid),tags=('odd',))
          mb.showinfo("Success","successfully inserted!!",parent=window)
          destroy(f)
     
       submitbtn=tk.Button(f,text="submit",command=insert_data)
       submitbtn.configure(font=('Times',11,'bold'),bg='green',fg='white')
       submitbtn.place(x=120,y=260)

       cancelbtn=tk.Button(f,text="cancel",command=lambda:destroy(f))
       cancelbtn.configure(font=('Times',11,'bold'),bg='red',fg='white')
       cancelbtn.place(x=240,y=260)

     def delete(tree):
         nonlocal i
         if not tree.selection():
            mb.showwarning("showwarning","Select a row",parent=window)
         else:
          selected_item=tree.selection()[0]
          ph=tree.item(selected_item)['values'][0]
          cid=tree.item(selected_item)['values'][1]
          del1="DELETE FROM PHONE_NO WHERE CUST_ID=:id AND PHONE_NO=:2"
          cur.execute(del1,(cid,ph))
          conn.commit()
          tree.delete(selected_item)
          mb.showinfo("success","information deleted!!",parent=window)
          i-=1
          Refresh(b1,window,1)
     def update(tree):
        selected_item=tree.focus()
        if not tree.focus():
            mb.showwarning("showwarning","Select a row",parent=window)
        else:
         updatebtn["state"]="disabled"
         values=tree.item(selected_item,"values")
         f=Frame(window,width=400,height=320,background="white")
         f.place(x=100,y=250)
         l1=Label(f,text="PHONE_NO",width=10,font=('Times',11,'bold'))
         e1=Entry(f,textvariable=phone_no,width=25)
         l1.place(x=50,y=30)
         e1.place(x=170,y=30,height=25)

         l2=Label(f,text="CUST_ID",width=10,font=('Times',11,'bold'))
         l2.place(x=50,y=70)
         e2=ttk.Combobox(f,value=lcst,textvariable=cust_id,width=25,height=5)
         e2.place(x=170,y=70)
         e1.delete(0,END)
         e1.insert(0,values[0])
         e2.insert(0,values[1])
         e2["state"]="readonly"
         def destroy(f):
           e1.delete(0,END)
           e2["state"]="normal"
           e2.delete(0,END)
           f.destroy()
           updatebtn["state"]="normal"
         def update_data():
           nonlocal e1,e2,selected_item,values
           phone=phone_no.get()
           cid=cust_id.get()
           if cid=="" or phone=="":
               mb.showwarning("warning","ENTER ALL VALUES",parent=window)
           elif len(str(phone))!=10:
               mb.showwarning("warning","ENTER 10 DIGIT PHONE NUMBER!",parent=window)
           else:
            stmt2='UPDATE PHONE_NO SET PHONE_NO=:1 WHERE CUST_ID=:2'
            cur.execute(stmt2,(phone,cid))
            conn.commit()
            tree.item(selected_item,values=(phone,cid))
            mb.showinfo("success","information updated!!",parent=window)
            destroy(f)

         savebtn=tk.Button(f,text="Update",command=update_data)
         savebtn.configure(font=('Times',11,'bold'),bg='green',fg='white')
         savebtn.place(x=120,y=260)

         cancelbtn=tk.Button(f,text="Cancel",command=lambda:destroy(f))
         cancelbtn.configure(font=('Times',11,'bold'),bg='red',fg='white')
         cancelbtn.place(x=240,y=260)
       
         
     insertbtn=tk.Button(tab2,text="INSERT",command=lambda:insert(tree))
     insertbtn.configure(font=('calibri',18,'bold'),bg='black',fg='white')
     insertbtn.place(x=500,y=400)

     deletebtn=tk.Button(tab2,text="DELETE",command=lambda:delete(tree))
     deletebtn.configure(font=('calibri',18,'bold'),bg='black',fg='white')
     deletebtn.place(x=600,y=400)

     updatebtn=tk.Button(tab2,text="UPDATE",command=lambda:update(tree))
     updatebtn.configure(font=('calibri',18,'bold'),bg='black',fg='white')
     updatebtn.place(x=700,y=400)
     

    def Accounts():
     canvas=Canvas(tab3,width=1600,height=950)
     canvas.pack(fill = "both", expand = True)
     canvas.img=ImageTk.PhotoImage(Image.open("bank4.jpg").resize((1600,950)))
     canvas.create_image(0,0,image=canvas.img,anchor='nw')
     tab3_win=canvas.create_window(0,70,anchor="nw",window=tab3)
     tab3.place(x=0,y=70)
     tabControl.add(tab3, text ='ACCOUNTS')
     # Add a Treeview widget
     tree = ttk.Treeview(tab3,selectmode='browse',height = 6)
     style = ttk.Style()
     style.theme_use('clam')
     style.configure("Treeview",background="white",foreground="black",rowheight=25,fieldbackground="white")
     style.map("Treeview",background=[('selected','purple')])
     tree.place(x=125,y=200)
     tree["columns"]=("1","2","3","4","5","6","7","8")
     tree["show"]='headings'
     tree.column("1", anchor = CENTER,stretch=NO,width=130)
     tree.column("2", anchor = CENTER,stretch=NO,width=130)
     tree.column("3", anchor = CENTER,stretch=NO,width=130)
     tree.column("4", anchor = CENTER,stretch=NO,width=130)
     tree.column("5", anchor = CENTER,stretch=NO,width=190)
     tree.column("6", anchor = CENTER,stretch=NO,width=190)
     tree.column("7", anchor = CENTER,stretch=NO,width=190)
     tree.column("8", anchor = CENTER,stretch=NO,width=190)
     tree.heading("1", text = "CUST_ID")
     tree.heading("2", text = "ACC_NO")
     tree.heading("3", text = "OPEN_DATE")
     tree.heading("4", text = "ACC_BALANCE")
     tree.heading("5", text = "INTEREST_AMT(SAVINGS_ACC)")
     tree.heading("6", text = "TRANSAC_LIMIT(SAVINGS_ACC)")
     tree.heading("7", text = "MIN_BAL_AMT(CURRENT_ACC)")
     tree.heading("8", text = "BIZ_TRANSAC_ID(CURRENT_ACC)")
     tree.tag_configure('odd',background="thistle")
     tree.tag_configure('even',background="thistle1")
     cur.execute("SELECT CUST_ID,ACC_NO,TO_CHAR(OPEN_DATE,'DD-MM-YYYY'),ACC_STATUS,INTEREST_AMT,TRANSACTION_LIMIT,MIN_BALANCE_AMT,BUSINESS_TRANSAC_NO FROM ACCOUNTS")
     i=0
     for row in cur:
      if i%2==0:
        tree.insert('',i,text="",values=(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7]),tags=('odd',))
        laccno.append(str(row[1]))
        lcst1.append(str(row[0]))
      else:
        tree.insert('',i,text="",values=(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7]),tags=('even',))
        laccno.append(str(row[1]))
        lcst1.append(str(row[0]))
      i+=1
     conn.commit()
    
     sb = ttk.Scrollbar(tab3, orient=VERTICAL)
     sb.place(x=1408,y=200,width=20,height=178)

     tree.config(yscrollcommand=sb.set)
     sb.config(command=tree.yview)
     
     acc_no=tk.StringVar()
     cust_id=tk.StringVar()
     open_date=tk.StringVar()
     acc_status=tk.StringVar()
     interest_amt=tk.StringVar()
     transaction_limit=tk.StringVar()
     min_balance_amt=tk.StringVar()
     business_transaction_no=tk.StringVar()
     def insert(tree,x):
       insertbtn1["state"]="disabled"
       insertbtn2["state"]="disabled"
       f=Frame(window,width=400,height=540,background="white")
       f.place(x=100,y=250)

       l10=Label(f,text="CUST_ID",width=9,font=('Times',11,'bold'))
       l10.place(x=0,y=30)
       e10=ttk.Combobox(f,value=lcst,textvariable=cust_id,state="readonly",width=22,height=5)
       e10.place(x=170,y=30)
       
       l1=Label(f,text="ACC_NO",width=8,font=('Times',11,'bold'))
       e1=Entry(f,textvariable=acc_no,width=25)
       l1.place(x=0,y=70)
       e1.place(x=170,y=70,height=25)
       
       l2=Label(f,text="OPEN_DATE(dd-mm-yyyy)",width=20,font=('Times',11,'bold'))
       e2=Entry(f,textvariable=open_date,width=25)
       l2.place(x=0,y=110)
       e2.place(x=190,y=110,height=25)
      
       l4=Label(f,text="ACC_STATUS",width=15,font=('Times',11,'bold'))
       e4=Entry(f,textvariable=acc_status,width=25)
       l4.place(x=0,y=150)
       e4.place(x=170,y=150,height=25)
       e4.delete(0,END)
       l5=Label(f,text="INTEREST_AMT",width=15,font=('Times',11,'bold'))
       e5=Entry(f,textvariable=interest_amt,width=25)
       l5.place(x=0,y=190)
       e5.place(x=170,y=190,height=25)


       l6=Label(f,text="TRANSACTION_LIMIT",width=18,font=('Times',11,'bold'))
       e6=Entry(f,textvariable=transaction_limit,width=25)
       l6.place(x=0,y=230)
       e6.place(x=170,y=230,height=25)
       
       
       l8=Label(f,text="MIN_BALANCE_AMT",width=20,font=('Times',11,'bold'))
       e8=Entry(f,textvariable=min_balance_amt,width=25)
       l8.place(x=0,y=270)
       e8.place(x=180,y=270,height=25)
       
       l9=Label(f,text="BIZ_TRANSAC_ID",width=20,font=('Times',11,'bold'))
       e9=Entry(f,textvariable=business_transaction_no,width=25)
       l9.place(x=0,y=310)
       e9.place(x=180,y=310,height=25)
       
       if x==1:
          e6.insert(INSERT,"100000")
          e6["state"]="disabled"
          l8.destroy()
          e8.destroy()
          l9.destroy()
          e9.destroy()
       elif x==2:
          e8.insert(INSERT,'20000')
          e8["state"]="disabled"
          l5.destroy()
          e5.destroy()
          l6.destroy()
          e6.destroy()
       def destroy(f):
         e10["state"]="normal"
         e10.delete(0,END)
         e1.delete(0,END)
         e2.delete(0,END)
         e4.delete(0,END)
         if x==1:
          e5.delete(0,END)
          e6.configure(state="normal")
          e6.delete(0,END)
         elif x==2:
          e8.configure(state="normal")
          e8.delete(0,END)
          e9.delete(0,END)
         f.destroy()
         insertbtn1["state"]="normal"
         insertbtn2["state"]="normal"
       def insert_data():
         nonlocal e1,e2,e4,e5,e6,e8,e9,x,i
         cid=cust_id.get()
         acc=acc_no.get()
         opndte=open_date.get()
         accsts=acc_status.get()
         if x==1:
          intrstamt=interest_amt.get()
          limit=transaction_limit.get()
          minamt=''
          bsns=''
         elif x==2:
          minamt=min_balance_amt.get()
          bsns=business_transaction_no.get()
          intrstamt=''
          limit=''
         else:
          intrstamt=interest_amt.get()
          limit=transaction_limit.get()
          minamt=min_balance_amt.get()
          bsns=business_transaction_no.get()
         if acc=="" or cid=="":
               mb.showwarning("warning","ENTER BOTH ACCOUNT NUMBER and CUSTOMER ID",parent=window)
         elif acc in laccno:
               mb.showwarning("warning","ACCOUNT NUMBER ALREADY EXISTS",parent=window)
         elif opndte=="" or accsts=="" :
               mb.showwarning("warning","ENTER BOTH ACCOUNT OPEN DATE AND ACCOUNT'S STATUS",parent=window)
         elif not acc.isnumeric():
               mb.showwarning("warning","ACCOUNT NUMBER MUST HAVE ONLY DIGITS",parent=window)
         elif x==1 and intrstamt=="":
                    mb.showwarning("warning","ENTER INTEREST AMOUNT",parent=window)
         elif x==2 and bsns=="":
                    mb.showwarning("warning","ENTER BIZ_TRANSACTION NO.",parent=window)
         else: 
          stmt="INSERT INTO ACCOUNTS VALUES(:1,:2,TO_DATE(:3,'DD-MM-YYYY'),:4,:5,:6,:7,:8)"
          cur.execute(stmt,(cid,acc,opndte,accsts,intrstamt,limit,minamt,bsns))
          conn.commit()
          if i%2==0:
           tree.insert('','end',text="",values=(cid,acc,opndte,accsts,intrstamt,limit,minamt,bsns),tags=('odd',))
           laccno.append(str(acc))
           lcst1.append(str(cid))
          else:
            tree.insert('','end',text="",values=(cid,acc,opndte,accsts,intrstamt,limit,minamt,bsns),tags=('even',))
            laccno.append(str(acc))
            lcst1.append(str(cid))
          i+=1
          mb.showinfo("Success","successfully inserted!!",parent=window)
          destroy(f)  
       submitbtn=tk.Button(f,text="submit",command=insert_data)
       submitbtn.configure(font=('Times',11,'bold'),bg='green',fg='white')
       submitbtn.place(x=120,y=430)

       cancelbtn=tk.Button(f,text="cancel",command=lambda:destroy(f))
       cancelbtn.configure(font=('Times',11,'bold'),bg='red',fg='white')
       cancelbtn.place(x=240,y=430)

     def delete(tree):
         nonlocal i
         if not tree.selection():
            mb.showwarning("showwarning","Select a row",parent=window)
         else:
          selected_item=tree.selection()[0]
          cust_id=tree.item(selected_item)['values'][0]
          accid=tree.item(selected_item)['values'][1]
          if cust_id in lcst2:
             mb.showwarning("showwarning","CANT DELETE ACCOUNT!!! \n(DELETE CUSTOMER'S ATM CARD FIRST)",parent=window)
          else:
           del1="DELETE FROM ACCOUNTS WHERE ACC_NO=:id"
           cur.execute(del1,{'id':accid})
           conn.commit()
           laccno.remove(str(accid))
           lcst1.remove(str(cust_id))
           tree.delete(selected_item)
           mb.showinfo("success","information deleted!!",parent=window)
           i-=1
           Refresh(b1,window,2)
          
     def update(tree):
        selected_item=tree.focus()
        if not tree.focus():
            mb.showwarning("showwarning","Select a row",parent=window)
        else:
         updatebtn["state"]="disabled"
         values=tree.item(selected_item,"values")
         f=Frame(window,width=400,height=500,background="white")
         f.place(x=100,y=250)

         l10=Label(f,text="CUST_ID",width=9,font=('Times',11,'bold'))
         l10.place(x=0,y=30)
         e10=ttk.Combobox(f,value=lcst,textvariable=cust_id,width=25,height=5)
         e10.place(x=170,y=30)
       
         l1=Label(f,text="ACC_NO",width=8,font=('Times',11,'bold'))
         e1=Entry(f,textvariable=acc_no,width=25)
         l1.place(x=0,y=70)
         e1.place(x=170,y=70,height=25)

         l2=Label(f,text="OPEN_DATE(dd-mm-yyyy)",width=20,font=('Times',11,'bold'))
         e2=Entry(f,textvariable=open_date,width=25)
         l2.place(x=0,y=110)
         e2.place(x=190,y=110,height=25)

         l4=Label(f,text="ACC_STATUS",width=15,font=('Times',11,'bold'))
         e4=Entry(f,textvariable=acc_status,width=25)
         l4.place(x=0,y=150)
         e4.place(x=170,y=150,height=25)

         l5=Label(f,text="INTEREST_AMT",width=15,font=('Times',11,'bold'))
         e5=Entry(f,textvariable=interest_amt,width=25)
         l5.place(x=0,y=190)
         e5.place(x=170,y=190,height=25)
          

         l6=Label(f,text="TRANSACTION_LIMIT",width=18,font=('Times',11,'bold'))
         e6=Entry(f,textvariable=transaction_limit,width=25)
         l6.place(x=0,y=230)
         e6.place(x=170,y=230,height=25)
         
         l8=Label(f,text="MIN_BALANCE_AMT",width=20,font=('Times',11,'bold'))
         e8=Entry(f,textvariable=min_balance_amt,width=25)
         l8.place(x=0,y=270)
         e8.place(x=180,y=270,height=25)
         
         l9=Label(f,text="BIZ_TRANSAC_ID",width=20,font=('Times',11,'bold'))
         e9=Entry(f,textvariable=business_transaction_no,width=25)
         l9.place(x=0,y=310)
         e9.place(x=180,y=310,height=25)
       
         if values[6]=='None' or values[6]=='':
          l8.destroy()
          e8.destroy()
          l9.destroy()
          e9.destroy()
         elif values[4]=='None' or values[4]=='':
          l5.destroy()
          e5.destroy()
          l6.destroy()
          e6.destroy()
          
         e10.insert(0,values[0])
         e10["state"]="readonly"
         lcst1.remove(str(values[0]))
         e1.insert(0,values[1])
         e1['state']="disabled"
         e2.insert(0,values[2])
         e4.insert(0,values[3])
         if values[6]=='None' or values[6]=='':
          e5.insert(0,values[4])
          e6.insert(0,values[5])
          e6["state"]="disabled"
         elif values[4]=='None' or values[4]=='':
          e8.insert(0,values[6])
          e8["state"]="disabled"
          e9.insert(0,values[7])
          
         def destroy(f):
           e10["state"]="normal"
           e10.delete(0,END)
           e1.configure(state="normal")
           e1.delete(0,END)
           e2.delete(0,END)
           e4.delete(0,END)
           if values[6]=='None' or values[6]=='':
            e5.delete(0,END)
            e6.configure(state="normal")
            e6.delete(0,END)
           elif values[4]=='None' or values[4]=='':
            e8.configure(state="normal")
            e8.delete(0,END)
            e9.delete(0,END)
           f.destroy()
           updatebtn["state"]="normal"
         def  update_data():
           nonlocal e1,e2,e4,e5,e6,e8,e9,e10,selected_item,values
           cid=cust_id.get()
           lcst1.append(str(cid))
           acc=acc_no.get()
           opndte=open_date.get()
           accsts=acc_status.get()
           if values[6]=='None' or values[6]=='':
            intrstamt=interest_amt.get()
            limit=transaction_limit.get()
            minamt=''
            biz=''
           elif values[4]=='None' or values[4]=='':
            minamt=min_balance_amt.get()
            biz=business_transaction_no.get()
            intrstamt=''
            limit=''
           else:
            intrstamt=interest_amt.get()
            limit=transaction_limit.get()
            minamt=min_balance_amt.get()
            biz=business_transaction_no.get()
           if  cid=="":
               mb.showwarning("warning","ENTER CUSTOMER ID",parent=window)
           elif opndte=="" or accsts=="" :
               mb.showwarning("warning","ENTER BOTH ACCOUNT OPEN DATE AND ACCOUNT'S STATUS",parent=window)
           elif not acc.isnumeric():
               mb.showwarning("warning","ACCOUNT NUMBER MUST HAVE ONLY DIGITS",parent=window)
           else:
            stmt2="UPDATE ACCOUNTS SET CUST_ID=:1,OPEN_DATE=TO_DATE(:3,'DD-MM-YYYY'),ACC_STATUS=:4,INTEREST_AMT=:5,TRANSACTION_LIMIT=:6,MIN_BALANCE_AMT=:7,BUSINESS_TRANSAC_NO=:8 WHERE ACC_NO=:2"
            cur.execute(stmt2,(cid,opndte,accsts,intrstamt,limit,minamt,biz,acc))
            conn.commit()   
            tree.item(selected_item,values=(cid,acc,opndte,accsts,intrstamt,limit,minamt,biz))
            mb.showinfo("success","information updated!!",parent=window)
            destroy(f)
         savebtn=tk.Button(f,text="Update",command=update_data)
         savebtn.configure(font=('Times',11,'bold'),bg='green',fg='white')
         savebtn.place(x=120,y=430)

         cancelbtn=tk.Button(f,text="Cancel",command=lambda:destroy(f))
         cancelbtn.configure(font=('Times',11,'bold'),bg='red',fg='white')
         cancelbtn.place(x=240,y=430) 
         
     insertbtn1=tk.Button(tab3,text="SAVINGS ACC",command=lambda:insert(tree,1))
     insertbtn1.configure(font=('calibri',18,'bold'),bg='black',fg='white')
     insertbtn1.place(x=390,y=450)

     insertbtn2=tk.Button(tab3,text="CURRENT ACC",command=lambda:insert(tree,2))
     insertbtn2.configure(font=('calibri',18,'bold'),bg='black',fg='white')
     insertbtn2.place(x=570,y=450)

     deletebtn=tk.Button(tab3,text="DELETE",command=lambda:delete(tree))
     deletebtn.configure(font=('calibri',18,'bold'),bg='black',fg='white')
     deletebtn.place(x=740,y=450)

     updatebtn=tk.Button(tab3,text="UPDATE",command=lambda:update(tree))
     updatebtn.configure(font=('calibri',18,'bold'),bg='black',fg='white')
     updatebtn.place(x=840,y=450)
     

    def Atm():
     canvas=Canvas(tab4,width=1600,height=950)
     canvas.pack(fill = "both", expand = True)
     canvas.img=ImageTk.PhotoImage(Image.open("bank5.jpg").resize((1600,950)))
     canvas.create_image(0,0,image=canvas.img,anchor='nw')
     tab4_win=canvas.create_window(0,70,anchor="nw",window=tab4)
     tab4.place(x=0,y=70)
     tabControl.add(tab4, text ='ATM')
     # Add a Treeview widget
     tree = ttk.Treeview(tab4, height = 6)
     style = ttk.Style()
     style.theme_use('clam')
     style.configure("Treeview",background="white",foreground="black",rowheight=25,fieldbackground="white")
     style.map("Treeview",background=[('selected','purple')])
     tree["columns"]=("1","2","3","4")
     tree['show']='headings'
     tree.place(x=350,y=200)
     tree.heading("1", text = "ATM_NUMBER")
     tree.heading("2", text = "LOCATION")
     tree.heading("3", text = "CASH_LIMIT")
     tree.heading("4", text = "BANK_CODE")
     tree.tag_configure('odd',background="plum3")
     tree.tag_configure('even',background="plum2")
     cur.execute('SELECT * FROM ATM')
     i=0
     for row in cur:
      if i%2==0:
        tree.insert('',i,text="",values=(row[0],row[1],row[2],row[3]),tags=('odd',))
        latmno.append(str(row[0]))
      else:
        tree.insert('',i,text="",values=(row[0],row[1],row[2],row[3]),tags=('even',))
        latmno.append(str(row[0]))
      i+=1
     conn.commit()
     sb = ttk.Scrollbar(tab4, orient=VERTICAL)
     sb.place(x=1144,y=200,width=20,height=179)

     tree.config(yscrollcommand=sb.set)
     sb.config(command=tree.yview)

     atm_number=tk.StringVar()
     location=tk.StringVar()
     cash_limit=tk.StringVar()
     bank_code=tk.StringVar()
     
     def insert(tree):
       insertbtn["state"]="disabled"
       f=Frame(window,width=400,height=320,background="white")
       f.place(x=100,y=250)
       l1=Label(f,text="ATM_NUMBER",width=12,font=('Times',11,'bold'))
       e1=Entry(f,textvariable=atm_number,width=25)
       l1.place(x=50,y=30)
       e1.place(x=170,y=30,height=25)

       l2=Label(f,text="LOCATION",width=10,font=('Times',11,'bold'))
       e2=Entry(f,textvariable=location,width=25)
       l2.place(x=50,y=70)
       e2.place(x=170,y=70,height=25)

       l3=Label(f,text="CASH_LIMIT",width=12,font=('Times',11,'bold'))
       e3=Entry(f,textvariable=cash_limit,width=25)
       l3.place(x=50,y=110)
       e3.place(x=170,y=110,height=25)
      
       l4=Label(f,text="BANK_CODE",width=12,font=('Times',11,'bold'))
       l4.place(x=50,y=150)
       e4=ttk.Combobox(f,value=lbcode,textvariable=bank_code,state="readonly",width=25,height=5)
       e4.place(x=165,y=150)
       def destroy(f):
         e1.delete(0,END)
         e2.delete(0,END)
         e3.delete(0,END)
         e4["state"]="normal"
         e4.delete(0,END)
         f.destroy()
         insertbtn["state"]="normal"
       def insert_data():
         nonlocal e1,e2,e3,e4,i
         atmno=atm_number.get()
         loc=location.get()
         cashlmt=cash_limit.get()
         bnkcd=bank_code.get()
         if atmno=="" or cashlmt=="":
               mb.showwarning("warning","ENTER BOTH ATM NUMBER AND CASH LIMIT",parent=window)
         elif atmno in latmno:
               mb.showwarning("warning","ATM NUMBER ALREADY EXISTS",parent=window)
         elif bnkcd=="":
               mb.showwarning("warning","ENTER BANK CODE",parent=window)
         else:
          stmt='INSERT INTO ATM VALUES(:1,:2,:3,:4)'
          cur.execute(stmt,(atmno,loc,cashlmt,bnkcd))
          conn.commit()
          if i%2==0:
           tree.insert('','end',text="",values=(atmno,loc,cashlmt,bnkcd),tags=('odd',))
           latmno.append(str(atmno))
          else:
           tree.insert('','end',text="",values=(atmno,loc,cashlmt,bnkcd),tags=('even',))
           latmno.append(str(atmno))
          i+=1
          mb.showinfo("Success","successfully inserted!!",parent=window)
          destroy(f)
         
       submitbtn=tk.Button(f,text="submit",command=insert_data)
       submitbtn.configure(font=('Times',11,'bold'),bg='green',fg='white')
       submitbtn.place(x=120,y=260)

       cancelbtn=tk.Button(f,text="cancel",command=lambda:destroy(f))
       cancelbtn.configure(font=('Times',11,'bold'),bg='red',fg='white')
       cancelbtn.place(x=240,y=260)

     def delete(tree):
         nonlocal i
         if not tree.selection():
            mb.showwarning("showwarning","Select a row",parent=window)
         else:
          selected_item=tree.selection()[0]
          atm_no=tree.item(selected_item)['values'][0]
          del1="DELETE FROM ATM WHERE ATM_NUMBER=:1"
          cur.execute(del1,{'1':atm_no})
          conn.commit()
          tree.delete(selected_item)
          latmno.remove(str(atm_no))
          mb.showinfo("success","information deleted!!",parent=window)
          i-=1
          Refresh(b1,window,3)
     def update(tree):
        selected_item=tree.focus()
        if not tree.focus():
            mb.showwarning("showwarning","Select a row",parent=window)
        else:
         updatebtn["state"]="disabled"
         values=tree.item(selected_item,"values")
         f=Frame(window,width=400,height=320,background="white")
         f.place(x=100,y=250)
         l1=Label(f,text="ATM_NUMBER",width=12,font=('Times',11,'bold'))
         e1=Entry(f,textvariable=atm_number,width=25)
         l1.place(x=50,y=30)
         e1.place(x=170,y=30,height=25)

         l2=Label(f,text="LOCATION",width=10,font=('Times',11,'bold'))
         e2=Entry(f,textvariable=location,width=25)
         l2.place(x=50,y=70)
         e2.place(x=170,y=70,height=25)

         l3=Label(f,text="CASH_LIMIT",width=12,font=('Times',11,'bold'))
         e3=Entry(f,textvariable=cash_limit,width=25)
         l3.place(x=50,y=110)
         e3.place(x=170,y=110,height=25)
   
         l4=Label(f,text="BANK_CODE",width=12,font=('Times',11,'bold'))
         l4.place(x=50,y=150)
         e4=ttk.Combobox(f,value=lbcode,textvariable=bank_code,width=25,height=5)
         e4.place(x=165,y=150)
       
         e1.insert(0,values[0])
         e1["state"]="disabled"
         e2.insert(0,values[1])
         e3.insert(0,values[2])
         e4.insert(0,values[3])
         e4["state"]="readonly"
         def destroy(f):
           e1.configure(state="normal")
           e1.delete(0,END)
           e2.delete(0,END)
           e3.delete(0,END)
           e4["state"]="normal"
           e4.delete(0,END)
           f.destroy()
           updatebtn["state"]="normal"
         def  update_data():
           nonlocal e1,e2,e3,e4,selected_item,values
           atmno=atm_number.get()
           loc=location.get()
           cashlmt=cash_limit.get()
           bnkcd=bank_code.get()
           if cashlmt=="":
               mb.showwarning("warning","ENTER  CASH LIMIT",parent=window)
           elif bnkcd=="":
               mb.showwarning("warning","ENTER BANK CODE",parent=window)
           else:
            stmt2='UPDATE ATM SET LOCATION=:2,CASH_LIMIT=:3,BANK_CODE=:4 WHERE ATM_NUMBER=:1'
            cur.execute(stmt2,(loc,cashlmt,bnkcd,atmno))
            conn.commit()
            tree.item(selected_item,values=(atmno,loc,cashlmt,bnkcd))
            mb.showinfo("success","information updated!!",parent=window)
            destroy(f)
            

         savebtn=tk.Button(f,text="Update",command=update_data)
         savebtn.configure(font=('Times',11,'bold'),bg='green',fg='white')
         savebtn.place(x=120,y=260)

         cancelbtn=tk.Button(f,text="Cancel",command=lambda:destroy(f))
         cancelbtn.configure(font=('Times',11,'bold'),bg='red',fg='white')
         cancelbtn.place(x=240,y=260)
       
     insertbtn=tk.Button(tab4,text="INSERT",command=lambda:insert(tree))
     insertbtn.configure(font=('calibri',18,'bold'),bg='black',fg='white')
     insertbtn.place(x=390,y=440)

     deletebtn=tk.Button(tab4,text="DELETE",command=lambda:delete(tree))
     deletebtn.configure(font=('calibri',18,'bold'),bg='black',fg='white')
     deletebtn.place(x=510,y=440)

     updatebtn=tk.Button(tab4,text="UPDATE",command=lambda:update(tree))
     updatebtn.configure(font=('calibri',18,'bold'),bg='black',fg='white')
     updatebtn.place(x=630,y=440)

       
    def Atm_card():
     canvas=Canvas(tab5,width=1600,height=950)
     canvas.pack(fill = "both", expand = True)
     canvas.img=ImageTk.PhotoImage(Image.open("bank6.jpg").resize((1600,950)))
     canvas.create_image(0,0,image=canvas.img,anchor='nw')
     tab5_win=canvas.create_window(0,70,anchor="nw",window=tab5)
     tab5.place(x=0,y=70)
     tabControl.add(tab5, text ='ATM_CARD')
     # Add a Treeview widget
     tree = ttk.Treeview(tab5, height = 6)
     style = ttk.Style()
     style.theme_use('clam')
     style.configure("Treeview",background="white",foreground="black",rowheight=25,fieldbackground="white")
     style.map("Treeview",background=[('selected','purple')])
     tree.tag_configure('odd',background="pink3")
     tree.tag_configure('even',background="pink2")
     tree["columns"]=("1","2","3","4","5")
     tree['show']='headings'
     tree.column("1", anchor = CENTER,stretch=NO,width=250)
     tree.column("2", anchor = CENTER,stretch=NO,width=250)
     tree.column("3", anchor = CENTER,stretch=NO,width=250)
     tree.column("4", anchor = CENTER,stretch=NO,width=250)
     tree.column("5", anchor = CENTER,stretch=NO,width=200)
     tree.place(x=160,y=150)
     tree.heading("1", text = "CARD_NO")
     tree.heading("2", text = "LIMIT")
     tree.heading("3", text = "BEGIN_DATE")
     tree.heading("4", text = "EXPIRY_DATE")
     tree.heading("5", text = "CUST_ID")
     tree.tag_configure('odd',background="pink3")
     tree.tag_configure('even',background="pink2")
     cur.execute("SELECT CARD_NO,LIMIT,TO_CHAR(BEGIN_DATE,'DD-MM-YYYY'),TO_CHAR(EXPIRY_DATE,'DD-MM-YYYY'),CUST_ID FROM ATM_CARD")
     i=0
     for row in cur:
      if i%2==0:
        tree.insert('',i,text="",values=(row[0],row[1],row[2],row[3],row[4]),tags=('odd',))
        lcno.append(str(row[0]))
        lcst2.append(str(row[4]))
      else:
        tree.insert('',i,text="",values=(row[0],row[1],row[2],row[3],row[4]),tags=('even',))
        lcno.append(str(row[0]))
        lcst2.append(str(row[4]))
      i+=1
     conn.commit()
     sb = ttk.Scrollbar(tab5, orient=VERTICAL)
     sb.place(x=1360,y=152,width=20,height=176)

     tree.config(yscrollcommand=sb.set)
     sb.config(command=tree.yview)      
   
     card_number=tk.StringVar()
     limit=tk.StringVar()
     begin_date=tk.StringVar()
     expiry_date=tk.StringVar()
     cust_id=tk.StringVar()
     
     def insert(tree):
       insertbtn["state"]="disabled"
       f=Frame(window,width=400,height=320,background="white")
       f.place(x=100,y=250)
       l1=Label(f,text="CARD_NO",width=8,font=('Times',11,'bold'))
       e1=Entry(f,textvariable=card_no,width=25)
       l1.place(x=50,y=30)
       e1.place(x=170,y=30,height=25)
       
       l2=Label(f,text="LIMIT",width=8,font=('Times',11,'bold'))
       e2=Entry(f,textvariable=limit,width=25)
       e2.insert(INSERT,"100000")
       e2["state"]="disabled"
       l2.place(x=50,y=70)
       e2.place(x=170,y=70,height=25)
      
       l3=Label(f,text="BEGIN_DATE(dd-mm-yyyy)",width=20,font=('Times',11,'bold'))
       e3=Entry(f,textvariable=begin_date,width=25)
       l3.place(x=8,y=110)
       e3.place(x=195,y=112,height=25)

       l4=Label(f,text="EXPIRY_DATE(dd-mm-yyyy)",width=21,font=('Times',11,'bold'))
       e4=Entry(f,textvariable=expiry_date,width=25)
       l4.place(x=8,y=150)
       e4.place(x=203,y=150,height=25)

       l5=Label(f,text="CUST_ID",width=12,font=('Times',11,'bold'))
       l5.place(x=50,y=190)
       e5=ttk.Combobox(f,value=lcst,textvariable=cust_id,state="readonly",width=25,height=5)
       e5.place(x=166,y=190)
       
       def destroy(f):
         e1.delete(0,END)
         e2.configure(state="normal")
         e2.delete(0,END)
         e3.delete(0,END)
         e4.delete(0,END)
         e5["state"]="normal"
         e5.delete(0,END)
         f.destroy()
         insertbtn["state"]="normal"
       def insert_data():
         nonlocal e1,e2,e3,e4,e5,i
         crdno=card_no.get()
         lmt=limit.get()
         bgndte=begin_date.get()
         exprydte=expiry_date.get()
         cid=cust_id.get()
         if cid not in lcst1:
            mb.showwarning("warning","ACCOUNT DOES NOT EXIST FOR THE GIVEN CUSTOMER ID\nCREATE AN ACCOUNT FIRST",parent=window)
         elif crdno=="":
               mb.showwarning("warning","ENTER  ATM CARD NUMBER",parent=window)
         elif not crdno.isnumeric():
               mb.showwarning("warning"," ATM CARD NUMBER MUST ONLY CONTAIN DIGITS",parent=window)
         elif crdno in lcno:
               mb.showwarning("warning","CARD NUMBER ALREADY EXISTS",parent=window)
         elif cid=="":
               mb.showwarning("warning","ENTER CUSTOMER ID",parent=window)
         else:
          stmt="INSERT INTO ATM_CARD VALUES(:1,:2,TO_DATE(:3,'DD-MM-YYYY'),TO_DATE(:4,'DD-MM-YYYY'),:5)"
          cur.execute(stmt,(crdno,lmt,bgndte,exprydte,cid))
          conn.commit()
          if i%2==0:
           tree.insert('','end',text="",values=(crdno,lmt,bgndte,exprydte,cid),tags=('odd',))
           lcno.append(str(crdno))
           lcst2.append(str(cid))
          else:
           tree.insert('','end',text="",values=(crdno,lmt,bgndte,exprydte,cid),tags=('even',))
           lcno.append(str(crdno))
           lcst2.append(str(cid))
          i+=1
          mb.showinfo("Success","successfully inserted!!",parent=window)
          destroy(f)
          cur.execute('''CREATE OR REPLACE VIEW TRANSACTION AS
                        SELECT ATC.CARD_NO,ACC.ACC_STATUS
                        FROM ACCOUNTS ACC,ATM_CARD ATC
                        WHERE ACC.CUST_ID=ATC.CUST_ID ''')
          conn.commit()
       submitbtn=tk.Button(f,text="submit",command=insert_data)
       submitbtn.configure(font=('Times',11,'bold'),bg='green',fg='white')
       submitbtn.place(x=120,y=260)

       cancelbtn=tk.Button(f,text="cancel",command=lambda:destroy(f))
       cancelbtn.configure(font=('Times',11,'bold'),bg='red',fg='white')
       cancelbtn.place(x=240,y=260)
     def delete(tree):
         nonlocal i
         if not tree.selection():
            mb.showwarning("showwarning","Select a row",parent=window)
         else:
          selected_item=tree.selection()[0]
          cno=tree.item(selected_item)['values'][0]
          cuid=tree.item(selected_item)['values'][4]
          del1="DELETE FROM ATM_CARD WHERE CARD_NO=:id"
          cur.execute(del1,{'id':cno})
          conn.commit()
          tree.delete(selected_item)
          lcno.remove(str(cno))
          lcst2.remove(str(cuid))
          mb.showinfo("success","information deleted!!",parent=window)
          i-=1
          Refresh(b1,window,4)
     def update(tree):
        selected_item=tree.focus()
        if not tree.focus():
            mb.showwarning("showwarning","Select a row",parent=window)
        else:
         updatebtn["state"]="disabled"
         values=tree.item(selected_item,"values")
         f=Frame(window,width=400,height=320,background="white")
         f.place(x=100,y=250)
         l1=Label(f,text="CARD_NO",width=8,font=('Times',11,'bold'))
         e1=Entry(f,textvariable=card_no,width=25)
         l1.place(x=50,y=30)
         e1.place(x=170,y=30,height=25)
         e1.delete(0,END)
         l2=Label(f,text="LIMIT",width=8,font=('Times',11,'bold'))
         e2=Entry(f,textvariable=limit,width=25)
         e2.insert(INSERT,"100000")
         e2["state"]="disabled"
         l2.place(x=50,y=70)
         e2.place(x=170,y=70,height=25)
         e2.delete(0,END)
         l3=Label(f,text="BEGIN_DATE(dd-mm-yyyy)",width=20,font=('Times',11,'bold'))
         e3=Entry(f,textvariable=begin_date,width=25)
         l3.place(x=8,y=110)
         e3.place(x=195,y=110,height=25)

         l4=Label(f,text="EXPIRY_DATE(dd-mm-yyyy)",width=21,font=('Times',11,'bold'))
         e4=Entry(f,textvariable=expiry_date,width=25)
         l4.place(x=8,y=150)
         e4.place(x=206,y=150,height=25)

         l5=Label(f,text="CUST_ID",width=12,font=('Times',11,'bold'))
         l5.place(x=50,y=190)
         e5=ttk.Combobox(f,value=lcst,textvariable=cust_id,width=25,height=5)
         e5.place(x=168,y=190)

         e1.insert(0,values[0])
         e1["state"]="disabled"
         e2.insert(0,values[1])
         e3.insert(0,values[2])
         e4.insert(0,values[3])
         e5.insert(0,values[4])
         e5["state"]="readonly"
         lcst2.remove(str(values[5]))
         
         def destroy(f):
           e1.configure(state="normal")
           e1.delete(0,END)
           e2.configure(state="normal")
           e2.delete(0,END)
           e3.delete(0,END)
           e4.delete(0,END)
           e5["state"]="readonly"
           e5.delete(0,END)
           f.destroy()
           updatebtn["state"]="normal"
         def  update_data():
           nonlocal e1,e2,e3,e4,e5,selected_item,values
           crdno=card_no.get()
           lmt=limit.get()
           bgndte=begin_date.get()
           exprydte=expiry_date.get()
           atmno=atm_number.get()
           cid=cust_id.get()
           if atmno=="":
               mb.showwarning("warning","ENTER ATM NUMBER",parent=window)
           elif cid=="":
               mb.showwarning("warning","ENTER CUSTOMER ID",parent=window)
           else:
            stmt2="UPDATE ATM_CARD SET LIMIT=:2,BEGIN_DATE=TO_DATE(:3,'DD-MM-YYYY'),EXPIRY_DATE=TO_DATE(:4,'DD-MM-YYYY'),CUST_ID=:5 WHERE CARD_NO=:1"
            cur.execute(stmt2,(lmt,bgndte,exprydte,cid,crdno))
            conn.commit()
            tree.item(selected_item,values=(crdno,lmt,bgndte,exprydte,atmno,cid))
            mb.showinfo("success","information updated!!",parent=window)
            destroy(f)
            lcst2.append(str(cid))
           cur.execute('''CREATE OR REPLACE VIEW TRANSACTION AS
                        SELECT ATC.CARD_NO,ACC.ACC_STATUS
                        FROM ACCOUNTS ACC,TRANSACTIONS T,ATM_CARD ATC
                        WHERE ACC.CUST_ID=ATC.CUST_ID AND
                        ATC.CARD_NO=T.CARD_NO''')
           conn.commit()
         savebtn=tk.Button(f,text="Update",command=update_data)
         savebtn.configure(font=('Times',11,'bold'),bg='green',fg='white')
         savebtn.place(x=120,y=260)

         cancelbtn=tk.Button(f,text="Cancel",command=lambda:destroy(f))
         cancelbtn.configure(font=('Times',11,'bold'),bg='red',fg='white')
         cancelbtn.place(x=240,y=260)
       
     insertbtn=tk.Button(tab5,text="INSERT",command=lambda:insert(tree))
     insertbtn.configure(font=('calibri',18,'bold'),bg='black',fg='white')
     insertbtn.place(x=200,y=430)

     deletebtn=tk.Button(tab5,text="DELETE",command=lambda:delete(tree))
     deletebtn.configure(font=('calibri',18,'bold'),bg='black',fg='white')
     deletebtn.place(x=350,y=430)

     updatebtn=tk.Button(tab5,text="UPDATE",command=lambda:update(tree))
     updatebtn.configure(font=('calibri',18,'bold'),bg='black',fg='white')
     updatebtn.place(x=500,y=430)
 
    def Bank():
     canvas=Canvas(tab6,width=1600,height=950)
     canvas.pack(fill = "both", expand = True)
     canvas.img=ImageTk.PhotoImage(Image.open("bank7.jpg").resize((1600,950)))
     canvas.create_image(0,0,image=canvas.img,anchor='nw')
     tab6_win=canvas.create_window(0,70,anchor="nw",window=tab6)
     tab6.place(x=0,y=70)
     tabControl.add(tab6, text ='BANK')
     # Add a Treeview widget
     tree = ttk.Treeview(tab6,selectmode="browse",height = 6)
     style = ttk.Style()
     style.theme_use('clam')
     style.configure("Treeview",background="white",foreground="black",rowheight=25,fieldbackground="white")
     style.map("Treeview",background=[('selected','purple')])
     tree["columns"]=("1","2","3")
     tree['show']='headings'
     tree.column("1", anchor = CENTER,stretch=NO,width=240)
     tree.column("2", anchor = CENTER,stretch=NO,width=289)
     tree.column("3", anchor = CENTER,stretch=NO,width=305)
     tree.place(x=320,y=190)
     tree.heading("1", text = "BANK_CODE")
     tree.heading("2", text = "BANK_NAME")
     tree.heading("3", text = "ADDRESS")
     tree.tag_configure('odd',background="MistyRose3")
     tree.tag_configure('even',background="MistyRose2")
     cur.execute('SELECT * FROM BANK')
     i=0
     for row in cur:
      if i%2==0:
        tree.insert('',i,text="",values=(row[0],row[1],row[2]),tags=('odd',))
        lbcode.append(str(row[0]))
      else:
        tree.insert('',i,text="",values=(row[0],row[1],row[2]),tags=('even',))
        lbcode.append(str(row[0]))
      i+=1
     conn.commit()
     sb = ttk.Scrollbar(tab6, orient=VERTICAL)
     sb.place(x=1150,y=191,width=20,height=179)
     tree.config(yscrollcommand=sb.set)
     sb.config(command=tree.yview)       

     bank_code=tk.StringVar()
     bank_name=tk.StringVar()
     address=tk.StringVar()
     
     def insert(tree):
       insertbtn["state"]="disabled"
       f=Frame(window,width=400,height=320,background="white")
       f.place(x=100,y=250)
       l1=Label(f,text="BANK_CODE",width=10,font=('Times',11,'bold'))
       e1=Entry(f,textvariable=bank_code,width=25)
       l1.place(x=50,y=30)
       e1.place(x=170,y=30,height=25)
      
       l2=Label(f,text="BANK_NAME",width=10,font=('Times',11,'bold'))
       e2=Entry(f,textvariable=bank_name,width=25)
       l2.place(x=50,y=70)
       e2.place(x=170,y=70,height=25)

       l3=Label(f,text="ADDRESS",width=10,font=('Times',11,'bold'))
       e3=Entry(f,textvariable=address,width=25)
       l3.place(x=50,y=110)
       e3.place(x=170,y=110,height=25)
       def destroy(f):
         e1.delete(0,END)
         e2.delete(0,END)
         e3.delete(0,END)
         f.destroy()
         insertbtn["state"]="normal"
       def insert_data():
         nonlocal e1,e2,e3,i
         bnkcd=bank_code.get()
         bnknm=bank_name.get()
         addrs=address.get()
         if bnkcd=="" or bnknm=="":
               mb.showwarning("warning","ENTER BANK CODE AND BANK NAME",parent=window)
         elif bnkcd in lbcode:
               mb.showwarning("warning","BANK CODE  ALREADY EXISTS",parent=window)
         else:
          stmt='INSERT INTO BANK VALUES(:1,:2,:3)'
          cur.execute(stmt,(bnkcd,bnknm,addrs))
          conn.commit()
          if i%2==0:
           tree.insert('','end',text="",values=(bnkcd,bnknm,addrs),tags=('odd',))
           lbcode.append(str(bnkcd))
          else:
           tree.insert('','end',text="",values=(bnkcd,bnknm,addrs),tags=('even',))
           lbcode.append(str(bnkcd))
          i+=1
          mb.showinfo("Success","successfully inserted!!",parent=window)
          destroy(f)
         
       submitbtn=tk.Button(f,text="submit",command=insert_data)
       submitbtn.configure(font=('Times',11,'bold'),bg='green',fg='white')
       submitbtn.place(x=120,y=260)

       cancelbtn=tk.Button(f,text="cancel",command=lambda:destroy(f))
       cancelbtn.configure(font=('Times',11,'bold'),bg='red',fg='white')
       cancelbtn.place(x=240,y=260)
     def delete(tree):
         nonlocal i
         if not tree.selection():
            mb.showwarning("showwarning","Select a row",parent=window)
         else:
          selected_item=tree.selection()[0]
          bank_code=tree.item(selected_item)['values'][0]
          del1="DELETE FROM BANK WHERE BANK_CODE=:1"
          cur.execute(del1,{'1':bank_code})
          conn.commit()
          tree.delete(selected_item)
          lbcode.remove(str(bank_code))
          mb.showinfo("success","information deleted!!",parent=window)
          i-=1
          Refresh(b1,window,5)
     def update(tree):
        selected_item=tree.focus()
        if not tree.focus():
            mb.showwarning("showwarning","Select a row",parent=window)
        else:
         updatebtn["state"]="disabled"
         values=tree.item(selected_item,"values")
         f=Frame(window,width=400,height=320,background="white")
         f.place(x=100,y=250)
         l1=Label(f,text="BANK_CODE",width=10,font=('Times',11,'bold'))
         e1=Entry(f,textvariable=bank_code,width=25)
         l1.place(x=50,y=30)
         e1.place(x=170,y=30,height=25)
         e1.delete(0,END)
         l2=Label(f,text="BANK_NAME",width=10,font=('Times',11,'bold'))
         e2=Entry(f,textvariable=bank_name,width=25)
         l2.place(x=50,y=70)
         e2.place(x=170,y=70,height=25)

         l3=Label(f,text="ADDRESS",width=10,font=('Times',11,'bold'))
         e3=Entry(f,textvariable=address,width=25)
         l3.place(x=50,y=110)
         e3.place(x=170,y=110,height=25)


         e1.insert(0,values[0])
         e1["state"]="disabled"
         e2.insert(0,values[1])
         e3.insert(0,values[2])
         
         def destroy(f):
           e1.configure(state="normal")
           e1.delete(0,END)
           e2.delete(0,END)
           e3.delete(0,END)
           f.destroy()
           updatebtn["state"]="normal"
         def  update_data():
           nonlocal e1,e2,e3,selected_item,values
           bnkcd=bank_code.get()
           bnknm=bank_name.get()
           addrs=address.get()
           if bnknm=="":
               mb.showwarning("warning","ENTER BANK NAME",parent=window)
           else:
            stmt2='UPDATE BANK SET BANK_NAME=:2,ADDRESS=:3 WHERE BANK_CODE=:1'
            cur.execute(stmt2,(bnknm,addrs,bnkcd))
            conn.commit()
            tree.item(selected_item,values=(bnkcd,bnknm,addrs))
            mb.showinfo("success","information updated!!",parent=window)
            destroy(f) 

         savebtn=tk.Button(f,text="Update",command=update_data)
         savebtn.configure(font=('Times',11,'bold'),bg='green',fg='white')
         savebtn.place(x=120,y=260)

         cancelbtn=tk.Button(f,text="Cancel",command=lambda:destroy(f))
         cancelbtn.configure(font=('Times',11,'bold'),bg='red',fg='white')
         cancelbtn.place(x=240,y=260)
       
     insertbtn=tk.Button(tab6,text="INSERT",command=lambda:insert(tree))
     insertbtn.configure(font=('calibri',18,'bold'),bg='LightSalmon4',fg='white')
     insertbtn.place(x=300,y=410)

     deletebtn=tk.Button(tab6,text="DELETE",command=lambda:delete(tree))
     deletebtn.configure(font=('calibri',18,'bold'),bg='LightSalmon4',fg='white')
     deletebtn.place(x=400,y=410)

     updatebtn=tk.Button(tab6,text="UPDATE",command=lambda:update(tree))
     updatebtn.configure(font=('calibri',18,'bold'),bg='LightSalmon4',fg='white')
     updatebtn.place(x=500,y=410)
 

    def Transactions():
     canvas=Canvas(tab7,width=1600,height=950)
     canvas.pack(fill = "both", expand = True)
     canvas.img=ImageTk.PhotoImage(Image.open("bank8.jpg").resize((1600,950)))
     canvas.create_image(0,0,image=canvas.img,anchor='nw')
     tab7_win=canvas.create_window(0,70,anchor="nw",window=tab7)
     tab7.place(x=0,y=70)
     tabControl.add(tab7, text ='TRANSACTIONS')
     dcttransac={} 
     cur.execute('SELECT CARD_NO,ACC_STATUS FROM TRANSACTION')
     conn.commit()
     for row in cur:
           dcttransac[str(row[0])]=str(row[1])
     # Add a Treeview widget
     tree = ttk.Treeview(tab7,selectmode="browse",height = 6)
     style = ttk.Style()
     style.theme_use('clam')
     style.configure("Treeview",background="white",foreground="black",rowheight=25,fieldbackground="white")
     style.map("Treeview",background=[('selected','purple')])
     tree["columns"]=("1","2","3","4","5","6")
     tree['show']='headings'
     tree.place(x=200,y=200)
     tree.heading("1", text = "TRANSACTION_NO")
     tree.heading("2", text = "TRANSACTION_DATE")
     tree.heading("3", text = "DEPOSIT_CASH")
     tree.heading("4", text = "WITHDRAW_CASH")
     tree.heading("5", text = "CARD_NO")
     tree.heading("6", text = "ACC_NO")
     tree.tag_configure('odd',background="PaleTurquoise2")
     tree.tag_configure('even',background="PaleTurquoise1")
     cur.execute("SELECT TRANSACTION_NO,TO_CHAR(TRANSACTION_DATE,'DD-MM-YYYY'),DEPOSIT_CASH,WITHDRAW_CASH,CARD_NO,ACC_NO FROM TRANSACTIONS")
     i=0
     for row in cur:
      if i%2==0:
        tree.insert('',i,text="",values=(row[0],row[1],row[2],row[3],row[4],row[5]),tags=('odd',))
        ltranno.append(str(row[0]))
      else:
        tree.insert('',i,text="",values=(row[0],row[1],row[2],row[3],row[4],row[5]),tags=('even',))
        ltranno.append(str(row[0]))
      i+=1
     conn.commit()
     
     sb = ttk.Scrollbar(tab7, orient=VERTICAL)
     sb.place(x=1393,y=200,width=20,height=177)
     
     tree.config(yscrollcommand=sb.set)
     sb.config(command=tree.yview)
        
     transaction_no=tk.StringVar()
     transaction_date=tk.StringVar()
     deposit_cash=tk.StringVar()
     withdraw_cash=tk.StringVar()
     card_no=tk.StringVar()
     acc_no=tk.StringVar()
     def insert(tree,x):
       insertbtn["state"]="disabled"
       insertbtn1["state"]="disabled"
       f=Frame(window,width=400,height=370,background="white")
       f.place(x=100,y=250)
       l1=Label(f,text="TRANSACTION_NO",width=20,font=('Times',11,'bold'))
       e1=Entry(f,textvariable=transaction_no,width=25)
       l1.place(x=30,y=30)
       e1.place(x=195,y=30,height=25)
       
       l2=Label(f,text="TRANSAC_DATE(dd-mm-yyyy)",width=25,font=('Times',11,'bold'))
       e2=Entry(f,textvariable=transaction_date,width=25)
       l2.place(x=0,y=85)
       e2.place(x=223,y=85,height=25)

       l3=Label(f,text="DEPOSIT_CASH",width=15,font=('Times',11,'bold'))
       e3=Entry(f,textvariable=deposit_cash,width=25)
       l3.place(x=30,y=130)
       e3.place(x=195,y=130,height=25)
      
       l4=Label(f,text="WITHDRAW_CASH",width=18,font=('Times',11,'bold'))
       e4=Entry(f,textvariable=withdraw_cash,width=25)
       l4.place(x=30,y=130)
       e4.place(x=195,y=130,height=25)

       l5=Label(f,text="CARD_NO",width=8,font=('Times',11,'bold'))
       l5.place(x=30,y=190)
       e5=ttk.Combobox(f,value=lcno,textvariable=card_no,state="readonly",width=25,height=5)
       e5.place(x=188,y=190)
       if x==0:
          l4.destroy()
          e4.destroy()
       else:
          l3.destroy()
          e3.destroy()
       def destroy(f):
         nonlocal x
         e1.delete(0,END)
         e2.delete(0,END)
         if x==0:
          e3.delete(0,END)
         else:
          e4.delete(0,END)
         e5["state"]="normal"
         e5.delete(0,END)
         f.destroy()
         insertbtn["state"]="normal"
         insertbtn1["state"]="normal"
       def insert_data():
         nonlocal e1,e2,e3,e4,e5,x,i
         transctno=transaction_no.get()
         transctdte=transaction_date.get()
         if x==0:
          dpstcsh=deposit_cash.get()
          withdrwcsh=''
         else:
          dpstcsh=''   
          withdrwcsh=withdraw_cash.get()
          w=int(withdrwcsh)
         
         crdno=card_no.get()
         stmt="SELECT ACC_NO FROM ACCOUNTS WHERE CUST_ID=(SELECT CUST_ID FROM ATM_CARD WHERE CARD_NO=:id)"
         cur.execute(stmt,{'id':crdno})
         for ele in cur:
          acno=ele[0]
         cur.execute('SELECT CARD_NO,ACC_STATUS FROM TRANSACTION')
         conn.commit()
         for row in cur:
           dcttransac[str(row[0])]=str(row[1])
         d=dcttransac[str(crdno)]
         if transctno=="" or transctdte=="":
               mb.showwarning("warning","ENTER BOTH TRANSACTION NUMBER AND TRANSACTION DATE",parent=window)
         elif transctno in ltranno:
               mb.showwarning("warning","TRANSACTION NUMBER  ALREADY EXISTS",parent=window)
         elif len(transctno)>12:
               mb.showwarning("warning","TRANSACTION NUMBER EXCEEDED LIMIT",parent=window)
         elif crdno==""  or acno=="":
               mb.showwarning("warning","ENTER BOTH CARD NUMBER AND ACCOUNT NUMBER",parent=window)
         elif x==0 and dpstcsh=="":
                    mb.showwarning("warning","ENTER DEPOSIT CASH",parent=window)
         elif x==1 and withdrwcsh=="":
                    mb.showwarning("warning","ENTER WITHDRAW CASH",parent=window)
         elif x==1 and w>int(d):
                    mb.showwarning("warning","WITHDRAW CASH GREATER THAN ACCOUNT BALANCE\n(ACC _STATUS: "+str(d)+")",parent=window)
         else: 
          stmt="INSERT INTO TRANSACTIONS VALUES(:1,TO_DATE(:2,'DD-MM-YYYY'),:3,:4,:5,:6)"
          cur.execute(stmt,(transctno,transctdte,dpstcsh,withdrwcsh,crdno,acno))
          conn.commit()
          if i%2==0:
           tree.insert('','end',text="",values=(transctno,transctdte,dpstcsh,withdrwcsh,crdno,acno),tags=('odd',))
           ltranno.append(str(transctno))
          else:
           tree.insert('','end',text="",values=(transctno,transctdte,dpstcsh,withdrwcsh,crdno,acno),tags=('odd',))
           ltranno.append(str(transctno))
          i+=1
          mb.showinfo("Success","successfully inserted!!",parent=window)
          destroy(f)
          stmtt="""CREATE OR REPLACE VIEW ACCOUNT AS
                    SELECT T.TRANSACTION_NO,ATC.CARD_NO,A.ACC_NO
                    FROM TRANSACTIONS T,ATM_CARD ATC,ACCOUNTS A
                    WHERE ATC.CARD_NO=T.CARD_NO
                    AND ATC.CUST_ID=A.CUST_ID"""
          cur.execute(stmtt)
          conn.commit()
          cur.execute("SELECT TRANSACTION_NO,ACC_NO FROM ACCOUNT")
          conn.commit()
          dctacc={}
          for row in cur:
             dctacc[row[0]]=row[1]
          account_no=dctacc[str(transctno)]
          if x==1 :
           stmt1="""UPDATE ACCOUNTS SET ACC_STATUS=ACC_STATUS-(SELECT WITHDRAW_CASH
                                                       FROM TRANSACTIONS T
                                                       WHERE T.TRANSACTION_NO=:1
                                                       AND T.WITHDRAW_CASH=:2)
                     WHERE  ACC_NO=:3 """
           cur.execute(stmt1,(transctno,withdrwcsh,account_no))
           conn.commit()     
           Refresh(b1,window,6)
          elif x==0 :
            stmt2="""UPDATE ACCOUNTS SET ACC_STATUS=ACC_STATUS+(SELECT DEPOSIT_CASH
                                                       FROM TRANSACTIONS T
                                                       WHERE T.TRANSACTION_NO=:1
                                                       AND T.DEPOSIT_CASH=:2)
                     WHERE ACC_NO=:3"""
            cur.execute(stmt2,(transctno,dpstcsh,account_no))
            conn.commit()
            Refresh(b1,window,6)
       submitbtn=tk.Button(f,text="submit",command=insert_data)
       submitbtn.configure(font=('Times',11,'bold'),bg='green',fg='white')
       submitbtn.place(x=120,y=290)

       cancelbtn=tk.Button(f,text="cancel",command=lambda:destroy(f))
       cancelbtn.configure(font=('Times',11,'bold'),bg='red',fg='white')
       cancelbtn.place(x=240,y=290)
        
     def delete(tree):
         nonlocal i
         if not tree.selection():
            mb.showwarning("showwarning","Select a row",parent=window)
         else:
          selected_item=tree.selection()[0]
          tran_no=tree.item(selected_item)['values'][0]
          del1="DELETE FROM TRANSACTIONS WHERE TRANSACTION_NO=:id"
          cur.execute(del1,{'id':tran_no})
          conn.commit()
          tree.delete(selected_item)
          ltranno.remove(str(tran_no))
          mb.showinfo("success","information deleted!!",parent=window)
          i-=1
          Refresh(b1,window,6)
     def update(tree):
        selected_item=tree.focus()
        if not tree.focus():
            mb.showwarning("showwarning","Select a row",parent=window)
        else:
          updatebtn["state"]="disabled"
          values=tree.item(selected_item,"values")
          f=Frame(window,width=400,height=370,background="white")
          f.place(x=100,y=250)
          l1=Label(f,text="TRANSACTION_NO",width=20,font=('Times',11,'bold'))
          e1=Entry(f,textvariable=transaction_no,width=25)
          l1.place(x=30,y=30)
          e1.place(x=195,y=30,height=25)

          l2=Label(f,text="TRANSAC_DATE(dd-mm-yyyy)",width=25,font=('Times',11,'bold'))
          e2=Entry(f,textvariable=transaction_date,width=25)
          l2.place(x=0,y=85)
          e2.place(x=223,y=85,height=25)

          l3=Label(f,text="DEPOSIT_CASH",width=15,font=('Times',11,'bold'))
          e3=Entry(f,textvariable=deposit_cash,width=25)
          l3.place(x=30,y=130)
          e3.place(x=195,y=130,height=25)
          
          l4=Label(f,text="WITHDRAW_CASH",width=18,font=('Times',11,'bold'))
          e4=Entry(f,textvariable=withdraw_cash,width=25)
          l4.place(x=30,y=130)
          e4.place(x=195,y=130,height=25)
          
          l5=Label(f,text="CARD_NO",width=8,font=('Times',11,'bold'))
          l5.place(x=30,y=190)
          e5=ttk.Combobox(f,value=lcno,textvariable=card_no,width=25,height=5)
          e5.place(x=188,y=190)

          l6=Label(f,text="ACC_NO",width=8,font=('Times',11,'bold'))
          l6.place(x=30,y=250)
          e6=Entry(f,textvariable=acc_no,width=25)
          e6.place(x=188,y=250)
          if values[3]=='None' or values[3]=='':
           l4.destroy()
           e4.destroy()
          elif values[2]=='None' or values[2]=='':
           l3.destroy()
           e3.destroy()

          e1.insert(0,values[0])
          e1["state"]="disabled"
          e2.insert(0,values[1])
          if values[3]=='None' or values[3]=='':
            e3.insert(0,values[2])
            dcsh=values[2]
          elif values[2]=='None' or values[2]=='':
            e4.insert(0,values[3])
            wcsh=values[3]
          e5.insert(0,values[4])
          e5["state"]="readonly"
          e6.insert(0,values[5])
          e6["state"]="disabled"
        def destroy(f):
           nonlocal values
           e1.configure(state="normal")
           e1.delete(0,END)
           e2.delete(0,END)
           if values[2]=='None' or values[2]=='':
            e4.delete(0,END)
           elif values[3]=='None' or values[3]=='':
            e3.delete(0,END)
           e5["state"]="normal"
           e5.delete(0,END)
           e6["state"]="normal"
           e6.delete(0,END)
           f.destroy()
           updatebtn["state"]="normal"
        def  update_data():
           nonlocal e1,e2,e3,e4,e5,e6,selected_item,values,wcsh,dcsh
           transctno=transaction_no.get()
           transctdte=transaction_date.get()
           if values[3]=='None' or values[3]=='':
            dpstcsh=deposit_cash.get()
            withdrwcsh=''
            w=0
           elif values[2]=='None' or values[2]=='':
            dpstcsh=''
            withdrwcsh=withdraw_cash.get()
            w=int(withdrwcsh)
           crdno=card_no.get()
           stmt="SELECT ACC_NO FROM ACCOUNTS WHERE CUST_ID=(SELECT CUST_ID FROM ATM_CARD WHERE CARD_NO=:id)"
           cur.execute(stmt,{'id':crdno})
           for ele in cur:
            acno=ele[0]
           e6["state"]="disabled"
           d=dcttransac[str(crdno)]
           if transctdte=="" :
               mb.showwarning("warning","ENTER TRANSACTION DATE",parent=window)
           elif len(transctno)>12:
               mb.showwarning("warning","TRANSACTION NUMBER EXCEEDED LIMIT",parent=window)
           elif crdno=="" or acc_no=="" :
               mb.showwarning("warning","ENTER BOTH CARD NUMBER AND ACCOUNT NUMBER",parent=window)
          
           elif int(w)>int(d):
                    mb.showwarning("warning","WITHDRAW CASH GREATER THAN ACCOUNT BALANCE\n(ACC _STATUS: "+str(d)+")",parent=window)
           else:
            stmt2="UPDATE TRANSACTIONS SET TRANSACTION_DATE=TO_DATE(:2,'DD-MM-YYYY'),DEPOSIT_CASH=:3,WITHDRAW_CASH=:4,CARD_NO=:5,ACC_NO=:6 WHERE TRANSACTION_NO=:1"
            cur.execute(stmt2,(transctdte,dpstcsh,withdrwcsh,crdno,acno,transctno))
            conn.commit()
            tree.item(selected_item,values=(transctno,transctdte,dpstcsh,withdrwcsh,crdno,acno))
            mb.showinfo("success","information updated!!",parent=window)
            destroy(f)
            stmtt="""CREATE OR REPLACE VIEW ACCOUNT AS
                    SELECT T.TRANSACTION_NO,ATC.CARD_NO,A.ACC_NO
                    FROM TRANSACTIONS T,ATM_CARD ATC,ACCOUNTS A
                    WHERE ATC.CARD_NO=T.CARD_NO
                    AND ATC.CUST_ID=A.CUST_ID"""
            cur.execute(stmtt)
            conn.commit()
            cur.execute("SELECT TRANSACTION_NO,ACC_NO FROM ACCOUNT")
            conn.commit()
            dctacc={}
            for row in cur:
              dctacc[row[0]]=row[1]
            account_no=dctacc[str(transctno)]
            if values[2]=='None' or values[2]=='':
              stmt="""UPDATE ACCOUNTS SET ACC_STATUS=ACC_STATUS+:1
                     WHERE ACC_NO=:3"""
              cur.execute(stmt,(wcsh,account_no))
              conn.commit()
              stmt1='''UPDATE ACCOUNTS SET ACC_STATUS=ACC_STATUS-(SELECT WITHDRAW_CASH
                                                       FROM TRANSACTIONS T
                                                       WHERE T.TRANSACTION_NO=:1
                                                       AND T.WITHDRAW_CASH=:2)
                  WHERE ACC_NO=:3'''
              cur.execute(stmt1,(transctno,withdrwcsh,account_no))
              conn.commit()
              Refresh(b1,window,6)
            elif values[3]=='None' or values[3]=='':
               stmt="""UPDATE ACCOUNTS SET ACC_STATUS=ACC_STATUS-:1
                      WHERE ACC_NO=:2"""
               cur.execute(stmt,(dcsh,account_no))
               conn.commit()
               stmt1='''UPDATE ACCOUNTS SET ACC_STATUS=ACC_STATUS+(SELECT DEPOSIT_CASH
                                                       FROM TRANSACTIONS T
                                                       WHERE T.TRANSACTION_NO=:1
                                                       AND T.DEPOSIT_CASH=:2)
                  WHERE ACC_NO=:3'''
               cur.execute(stmt1,(transctno,dpstcsh,account_no))
               conn.commit()
               Refresh(b1,window,6)
        savebtn=tk.Button(f,text="Update",command=update_data)
        savebtn.configure(font=('Times',11,'bold'),bg='green',fg='white')
        savebtn.place(x=120,y=310)

        cancelbtn=tk.Button(f,text="Cancel",command=lambda:destroy(f))
        cancelbtn.configure(font=('Times',11,'bold'),bg='red',fg='white')
        cancelbtn.place(x=240,y=310)
       
         
     insertbtn=tk.Button(tab7,text="DEPOSIT",command=lambda:insert(tree,0))
     insertbtn.configure(font=('calibri',18,'bold'),bg='black',fg='white')
     insertbtn.place(x=200,y=430)

     insertbtn1=tk.Button(tab7,text="WITHDRAW",command=lambda:insert(tree,1))
     insertbtn1.configure(font=('calibri',18,'bold'),bg='black',fg='white')
     insertbtn1.place(x=350,y=430)

     deletebtn=tk.Button(tab7,text="DELETE",command=lambda:delete(tree))
     deletebtn.configure(font=('calibri',18,'bold'),bg='black',fg='white')
     deletebtn.place(x=520,y=430)

     updatebtn=tk.Button(tab7,text="UPDATE",command=lambda:update(tree))
     updatebtn.configure(font=('calibri',18,'bold'),bg='black',fg='white')
     updatebtn.place(x=660,y=430)
     

    def Accountant():
     canvas=Canvas(tab8,width=1600,height=950)
     canvas.pack(fill = "both", expand = True)
     canvas.img=ImageTk.PhotoImage(Image.open("bank9.jpg").resize((1600,950)))
     canvas.create_image(0,0,image=canvas.img,anchor='nw')
     tab8_win=canvas.create_window(0,70,anchor="nw",window=tab8)
     tab8.place(x=0,y=70)
     tabControl.add(tab8, text ='ACCOUNTANT')
     # Add a Treeview widget
     tree = ttk.Treeview(tab8,selectmode="browse",height = 6)
     style = ttk.Style()
     style.theme_use('clam')
     style.configure("Treeview",background="white",foreground="black",rowheight=25,fieldbackground="white")
     style.map("Treeview",background=[('selected','purple')])
     tree["columns"]=("1","2","3")
     tree['show']='headings'
     tree.column("1", anchor = CENTER,stretch=NO,width=360)
     tree.column("2", anchor = CENTER,stretch=NO,width=300)
     tree.column("3", anchor = CENTER,stretch=NO,width=400)
     tree.place(x=250,y=200)
     tree.heading("1", text = "ACCOUNTANT_ID")
     tree.heading("2", text = "ACCOUNTANT_REC_NO")
     tree.heading("3", text = "BANK_CODE")
     tree.tag_configure('odd',background="lightsalmon3")
     tree.tag_configure('even',background="lightsalmon2")
     cur.execute('SELECT * FROM ACCOUNTANT')
     i=0
     for row in cur:
      if i%2==0:
        tree.insert('',i,text="",values=(row[0],row[1],row[2]),tags=('odd',))
        laccntno.append(str(row[0]))
      else:
         tree.insert('',i,text="",values=(row[0],row[1],row[2]),tags=('even',))
         laccntno.append(str(row[0]))
      i+=1
     conn.commit()
     
     sb = ttk.Scrollbar(tab8, orient=VERTICAL)
     sb.place(x=1312,y=200,width=20,height=180)

     tree.config(yscrollcommand=sb.set)
     sb.config(command=tree.yview)      

     accountant_id=tk.StringVar()
     payment_records=tk.StringVar()
     bank_code=tk.StringVar()
     
     def insert(tree):
       insertbtn["state"]="disabled"
       f=Frame(window,width=400,height=320,background="white")
       f.place(x=100,y=250)
       l1=Label(f,text="ACCOUNTANT_ID",width=17,font=('Times',11,'bold'))
       e1=Entry(f,textvariable=accountant_id,width=25)
       l1.place(x=30,y=30)
       e1.place(x=185,y=30,height=25)
       
       l3=Label(f,text="ACCOUNTANT_REC_NO",width=18,font=('Times',11,'bold'))
       e3=Entry(f,textvariable=payment_records,width=25)
       l3.place(x=30,y=70)
       e3.place(x=189,y=70,height=25)
       
       l4=Label(f,text="BANK_CODE",width=10,font=('Times',11,'bold'))
       l4.place(x=30,y=110)
       e4=ttk.Combobox(f,value=lbcode,textvariable=bank_code,state="readonly",width=25,height=5)
       e4.place(x=189,y=110)
       def destroy(f):
         e1.delete(0,END)
         e3["state"]="normal"
         e3.delete(0,END)
         e4["state"]="normal"
         e4.delete(0,END)
         f.destroy()
         insertbtn["state"]="normal"
       def insert_data():
         nonlocal e1,e3,e4,i
         acctid=accountant_id.get()
         pymntrcd=payment_records.get()
         bnkcd=bank_code.get()
         if acctid=="" :
               mb.showwarning("warning","ENTER  ACCOUNTANT ID ",parent=window)
         elif acctid in laccntno:
               mb.showwarning("warning","ACCOUNTANT ID  ALREADY EXISTS",parent=window)   
         elif pymntrcd=="":
               mb.showwarning("warning","ENTER  ACCOUNTANT REC NUMBER",parent=window)
         elif bnkcd=="":
               mb.showwarning("warning","ENTER  PAYMENTS BANK CODE",parent=window)
         elif len(str(acctid))!=6:
               mb.showwarning("warning","ACCOUNTANT ID MUST BE 6 DIGIT",parent=window)
         else:
          stmt='INSERT INTO ACCOUNTANT VALUES(:1,:2,:3)'
          cur.execute(stmt,(acctid,pymntrcd,bnkcd))
          conn.commit()
          if i%2==0:
           tree.insert('','end',text="",values=(acctid,pymntrcd,bnkcd),tags=('odd',))
           laccntno.append(str(acctid))
          else:
           tree.insert('','end',text="",values=(acctid,pymntrcd,bnkcd),tags=('even',))
           laccntno.append(str(acctid))
          i+=1
          mb.showinfo("Success","successfully inserted!!",parent=window)
          destroy(f)
      
       submitbtn=tk.Button(f,text="submit",command=insert_data)
       submitbtn.configure(font=('Times',11,'bold'),bg='green',fg='white')
       submitbtn.place(x=120,y=260)

       cancelbtn=tk.Button(f,text="cancel",command=lambda:destroy(f))
       cancelbtn.configure(font=('Times',11,'bold'),bg='red',fg='white')
       cancelbtn.place(x=240,y=260)
     def delete(tree):
         nonlocal i
         if not tree.selection():
            mb.showwarning("showwarning","Select a row",parent=window)
         else:
          selected_item=tree.selection()[0]
          acc_id=tree.item(selected_item)['values'][0]
          del1="DELETE FROM ACCOUNTANT WHERE ACCOUNTANT_ID=:1"
          cur.execute(del1,{'1':acc_id})
          conn.commit()
          tree.delete(selected_item)
          laccntno.remove(str(acc_id))
          mb.showinfo("success","information deleted!!",parent=window)
          i-=1
          Refresh(b1,window,7)
     def update(tree):
        selected_item=tree.focus()
        if not tree.focus():
            mb.showwarning("showwarning","Select a row",parent=window)
        else:
         updatebtn["state"]="disabled"
         values=tree.item(selected_item,"values")
         f=Frame(window,width=400,height=320,background="white")
         f.place(x=100,y=250)
         l1=Label(f,text="ACCOUNTANT_ID",width=17,font=('Times',11,'bold'))
         e1=Entry(f,textvariable=accountant_id,width=25)
         l1.place(x=30,y=30)
         e1.place(x=185,y=30,height=25)
        
         l3=Label(f,text="ACCOUNTANT_REC_NO",width=18,font=('Times',11,'bold'))
         e3=Entry(f,textvariable=payment_records,width=25)
         l3.place(x=30,y=80)
         e3.place(x=189,y=80,height=25)
   
         l4=Label(f,text="BANK_CODE",width=10,font=('Times',11,'bold'))
         l4.place(x=30,y=130)
         e4=ttk.Combobox(f,value=lbcode,textvariable=bank_code,width=25,height=5)
         e4.place(x=185,y=130)
         
         e1.insert(0,values[0])
         e1["state"]="disabled"
         e3.insert(0,values[1])
         e4.insert(0,values[2])
         e4["state"]="readonly"
         def destroy(f):
           e1.configure(state="normal")
           e1.delete(0,END)
           e3.delete(0,END)
           e4["state"]="normal"
           e4.delete(0,END)
           f.destroy()
           updatebtn["state"]="normal"
         def  update_data():
           nonlocal e1,e3,e4,selected_item,values
           acctid=accountant_id.get()
           pymntrcd=payment_records.get()
           bnkcd=bank_code.get()
           if pymntrcd=="":
               mb.showwarning("warning","ENTER  ACCOUNTANT RECORDS NUMBER",parent=window)
           elif bnkcd=="":
               mb.showwarning("warning","ENTER  PAYMENTS BANK CODE",parent=window)
           elif len(acctid)!=6:
               mb.showwarning("warning","ACCOUNT ID MUST BE 6 DIGIT",parent=window)
           else:
            stmt2='UPDATE ACCOUNTANT SET PAYMENT_RECORDS=:2,BANK_CODE=:3 WHERE ACCOUNTANT_ID=:1'
            cur.execute(stmt2,(pymntrcd,bnkcd,acctid))
            conn.commit()
            tree.item(selected_item,values=(acctid,pymntrcd,bnkcd))
            mb.showinfo("success","information updated!!",parent=window)
            destroy(f)

         savebtn=tk.Button(f,text="Update",command=update_data)
         savebtn.configure(font=('Times',11,'bold'),bg='green',fg='white')
         savebtn.place(x=120,y=260)

         cancelbtn=tk.Button(f,text="Cancel",command=lambda:destroy(f))
         cancelbtn.configure(font=('Times',11,'bold'),bg='red',fg='white')
         cancelbtn.place(x=240,y=260)
       
         
     insertbtn=tk.Button(tab8,text="INSERT",command=lambda:insert(tree))
     insertbtn.configure(font=('calibri',18,'bold'),bg='DarkOrange3',fg='white')
     insertbtn.place(x=300,y=430)

     deletebtn=tk.Button(tab8,text="DELETE",command=lambda:delete(tree))
     deletebtn.configure(font=('calibri',18,'bold'),bg='DarkOrange3',fg='white')
     deletebtn.place(x=400,y=430)

     updatebtn=tk.Button(tab8,text="UPDATE",command=lambda:update(tree))
     updatebtn.configure(font=('calibri',18,'bold'),bg='DarkOrange3',fg='white')
     updatebtn.place(x=500,y=430)

    def Managed_by():
     canvas=Canvas(tab9,width=1600,height=950)
     canvas.pack(fill = "both", expand = True)
     canvas.img=ImageTk.PhotoImage(Image.open("bank10.jpg").resize((1600,950)))
     canvas.create_image(0,0,image=canvas.img,anchor='nw')
     tab9_win=canvas.create_window(0,70,anchor="nw",window=tab9)
     tab9.place(x=0,y=70)
     tabControl.add(tab9, text ='MANAGED_BY')
     # Add a Treeview widget
     tree = ttk.Treeview(tab9,selectmode="browse",height = 6)
     style = ttk.Style()
     style.theme_use('clam')
     style.configure("Treeview",background="white",foreground="black",rowheight=25,fieldbackground="white")
     style.map("Treeview",background=[('selected','blue')])
     tree["columns"]=("1","2")
     tree['show']='headings'
     tree.column("1", anchor = CENTER,stretch=NO,width=300)
     tree.column("2", anchor = CENTER,stretch=NO,width=352)
     tree.place(x=415,y=200)
     tree.heading("1", text = "TRANSACTION_NO")
     tree.heading("2", text = "ACCOUNTANT_ID")
     tree.tag_configure('odd',background="snow3")
     tree.tag_configure('even',background="snow2")
     cur.execute('SELECT * FROM MANAGED_BY')
     i=0
     for row in cur:
       if i%2==0:
        tree.insert('',i,text="",values=(row[0],row[1]),tags=('odd',))
       else:
         tree.insert('',i,text="",values=(row[0],row[1]),tags=('even',))
       i+=1
     conn.commit()
     sb = ttk.Scrollbar(tab9, orient=VERTICAL)
     sb.place(x=1068,y=200,width=20,height=178)  

     tree.config(yscrollcommand=sb.set)
     sb.config(command=tree.yview)
    
     transaction_no=tk.StringVar()
     accountant_id=tk.StringVar()
     
     def insert(tree):
       insertbtn["state"]="disabled"
       f=Frame(window,width=400,height=320,background="white")
       f.place(x=100,y=250)
       l1=Label(f,text="TRANSACTION_NO",width=20,font=('Times',11,'bold'))
       l1.place(x=20,y=30)
       e1=ttk.Combobox(f,value=ltranno,textvariable=transaction_no,state="readonly",width=25,height=5)
       e1.place(x=188,y=30)

       l2=Label(f,text="ACCOUNTANT_ID",width=18,font=('Times',11,'bold'))
       l2.place(x=20,y=70)
       e2=ttk.Combobox(f,value=laccntno,textvariable=accountant_id,state="readonly",width=25,height=5)
       e2.place(x=185,y=70)
       def destroy(f):
         e1["state"]="normal"
         e1.delete(0,END)
         e2["state"]="normal"
         e2.delete(0,END)
         f.destroy()
         insertbtn["state"]="normal"
         
       def insert_data():
         nonlocal e1,e2,i
         transctno=transaction_no.get()
         acctid=accountant_id.get()
         if transctno=="" or acctid=="":
               mb.showwarning("warning","ENTER BOTH TRANSACTION NUMBER AND ACCOUNT ID",parent=window)
         else:
          stmt='INSERT INTO MANAGED_BY VALUES(:1,:2)'
          cur.execute(stmt,(transctno,acctid))
          conn.commit()
          if i%2==0:
           tree.insert('','end',text="",values=(transctno,acctid),tags=('odd',))
          else:
            tree.insert('','end',text="",values=(transctno,acctid),tags=('even',))
          i+=1
          mb.showinfo("Success","successfully inserted!!",parent=window)
          destroy(f)
       submitbtn=tk.Button(f,text="submit",command=insert_data)
       submitbtn.configure(font=('Times',11,'bold'),bg='green',fg='white')
       submitbtn.place(x=120,y=260)

       cancelbtn=tk.Button(f,text="cancel",command=lambda:destroy(f))
       cancelbtn.configure(font=('Times',11,'bold'),bg='red',fg='white')
       cancelbtn.place(x=240,y=260)

     def delete(tree):
         nonlocal i
         if not tree.selection():
            mb.showwarning("showwarning","Select a row",parent=window)
         else:
          selected_item=tree.selection()[0]
          tran_no=tree.item(selected_item)['values'][0]
          accnt_id=tree.item(selected_item)['values'][1]
          del1="DELETE FROM MANAGED_BY WHERE TRANSACTION_NO=:1 AND ACCOUNTANT_ID=:2"
          cur.execute(del1,(tran_no,accnt_id))
          conn.commit()
          tree.delete(selected_item)
          mb.showinfo("success","information deleted!!",parent=window)
          i-=1
          Refresh(b1,window,8)
     def update(tree):
        selected_item=tree.focus()
        if not tree.focus():
            mb.showwarning("showwarning","Select a row",parent=window)
        else:
         updatebtn["state"]="disabled"
         values=tree.item(selected_item,"values")
         f=Frame(window,width=400,height=320,background="white")
         f.place(x=100,y=250)
         l1=Label(f,text="TRANSACTION_NO",width=20,font=('Times',11,'bold'))
         l1.place(x=20,y=30)
         e1=ttk.Combobox(f,value=ltranno,textvariable=transaction_no,width=25,height=5)
         e1.place(x=188,y=30)

         l2=Label(f,text="ACCOUNTANT_ID",width=18,font=('Times',11,'bold'))
         l2.place(x=20,y=70)
         e2=ttk.Combobox(f,value=laccntno,textvariable=accountant_id,width=25,height=5)
         e2.place(x=184,y=70)
         e1.insert(0,values[0])
         e1["state"]="readonly"
         e2.insert(0,values[1])
         e2["state"]="readonly"
         def destroy(f):
           e1["state"]="normal"
           e1.delete(0,END)
           e2["state"]="normal"
           e2.delete(0,END)
           f.destroy()
           updatebtn["state"]="normal"
         def update_data():
           nonlocal e1,e2,selected_item,values
           transctno=transaction_no.get()
           acctid=accountant_id.get()
           if transctno=="" or acctid=="":
               mb.showwarning("warning","ENTER BOTH TRANSACTION NUMBER AND ACCOUNT ID",parent=window)
           else:
            stmt2='UPDATE MANAGED_BY SET ACCOUNTANT_ID=:2 WHERE TRANSACTION_NO=:1'
            cur.execute(stmt2,(acctid,transctno))
            conn.commit()
            tree.item(selected_item,values=(transctno,acctid))
            mb.showinfo("success","information updated!!",parent=window)
            destroy(f) 

         savebtn=tk.Button(f,text="Update",command=update_data)
         savebtn.configure(font=('Times',11,'bold'),bg='green',fg='white')
         savebtn.place(x=120,y=260)

         cancelbtn=tk.Button(f,text="Cancel",command=lambda:destroy(f))
         cancelbtn.configure(font=('Times',11,'bold'),bg='red',fg='white')
         cancelbtn.place(x=240,y=260)
       
         
     insertbtn=tk.Button(tab9,text="INSERT",command=lambda:insert(tree))
     insertbtn.configure(font=('calibri',18,'bold'),bg='black',fg='white')
     insertbtn.place(x=300,y=430)

     deletebtn=tk.Button(tab9,text="DELETE",command=lambda:delete(tree))
     deletebtn.configure(font=('calibri',18,'bold'),bg='black',fg='white')
     deletebtn.place(x=400,y=430)

     updatebtn=tk.Button(tab9,text="UPDATE",command=lambda:update(tree))
     updatebtn.configure(font=('calibri',18,'bold'),bg='black',fg='white')
     updatebtn.place(x=500,y=430)

    def Refresh(b1,window1,p):
        AdminWindow(b1,1,window1,p)
        
    Button(window, text="BACK",bg="floral white",fg="black",activebackground = "white",width=8,font=('Calibri',20,'bold'),command=lambda:Main_page(b1,window)).place(x=1415,y=0)
    Button(window, text="REFRESH",bg="floral white",fg="black",activebackground = "white",width=8,font=('Calibri',20,'bold'),command=lambda:Refresh(b1,window,0)).place(x=1276,y=0)
    Customer()
    Phone_no()
    Accounts()
    Atm()
    Atm_card()
    Bank()
    Transactions()
    Accountant()
    Managed_by()
    if x==1:
       f.destroy()
    if p==0:
       tabControl.select(tab1)
    elif p==1:
       tabControl.select(tab2)
    elif p==2:
       tabControl.select(tab3)
    elif p==3:
       tabControl.select(tab4)
    elif p==4:
       tabControl.select(tab5)
    elif p==5:
       tabControl.select(tab6)
    elif p==6:
       tabControl.select(tab7)
    elif p==7:
       tabControl.select(tab8)
    elif p==8:
       tabControl.select(tab9)
    window.mainloop()
    cur.close()
    conn.close()

   
cur.close()
conn.close()
