from tkinter import *
from tkinter import messagebox
import ast
from PIL import ImageTk
from PIL import Image
import time

def splash_screen():
    # Create the splash screen window
    splash = Tk()
    splash_width = 427
    splash_height = 250
    screen_width = splash.winfo_screenwidth()
    screen_height = splash.winfo_screenheight()
    x_coordinate = (screen_width/2) - (splash_width/2)
    y_coordinate = (screen_height/2) - (splash_height/2)
    splash.geometry("%dx%d+%d+%d" % (splash_width, splash_height, x_coordinate, y_coordinate))
    splash.overrideredirect(1)  # Hide titlebar

    # Create the labels and configure them
    Frame(splash, width=splash_width, height=splash_height, bg='#272727').place(x=0, y=0)
    label1 = Label(splash, text='NOUSHARE', fg='white', bg='#272727')
    label1.configure(font=("Game Of Squids", 24, "bold"))
    label1.place(x=120, y=90)
    label2 = Label(splash, text='Loading...', fg='white', bg='#272727')
    label2.configure(font=("Calibri", 11))
    label2.place(x=10, y=215)

    # Define the image paths
    image_paths = ['c1.png', 'c2.png','c3.png']
    images = [ImageTk.PhotoImage(Image.open(image_path)) for image_path in image_paths]

    # Create the loading animation
    num_images = len(images)
    for i in range(5):  # 5 loops
        for j in range(num_images):
            label = Label(splash, image=images[j], border=0, relief=SUNKEN)
            label.place(x=180 + j * 20, y=145)
            splash.update_idletasks()
            time.sleep(0.5)
            label.destroy()
    
    # Close the splash screen
    splash.destroy()

# Call the splash screen function
splash_screen()

# Continue with your login code


root=Tk()
root.title('Login')
root.geometry('925x500')
root.configure(bg='#fff')
root.resizable(False,False)

def signin():
    username=user.get()
    password=code.get()
    file=open('datasheet.txt','r')
    d=file.read()
    r=ast.literal_eval(d)
    file.close()

    ## print(r.keys())
    ## print(r.values())

#App
    if username in r.keys() and password==r[username]:
        root.destroy()
        import home #Home pageS
    else:
        messagebox.showerror('Invalid','Wrong credentials')
#-----------------------------------------------------------------

def signup_command():
    window=Toplevel(root)
    window.title("SignUp")
    window.geometry('925x500')
    window.configure(bg='#fff')
    window.resizable(False,False)

    def signup():
        username=user.get()
        password=code.get()
        confirm_password=confirm_code.get()
        if password==confirm_password:
            try:
                file=open('datasheet.txt','r+')
                d=file.read()
                r=ast.literal_eval(d)

                dict2={username:password}
                r.update(dict2)
                file.truncate(0)
                file.close()

                file=open('datasheet.txt','w')
                w=file.write(str(r))

                messagebox.showinfo('signup','Sucessfully sign up')
                window.destroy()  
            except:
                file=open('datasheet.txt','w')
                pp=str({'Username':'password'})
                file.write(pp)
                file.close()

        else:
            messagebox.showerror('Invaild','Password dont match')        

    def signin():
        window.destroy()


    img=PhotoImage(file='signup.png')
    Label(window,image=img,border='0',bg='white').place(x=50,y=90)
    frame=Frame(window,width=350,height=390,bg='#fff')
    frame.place(x=480,y=50)

    heading=Label(frame,text='signup',fg='#57a1f8',bg='white',font=('Microsoft Yahei UI Light',23,'bold'))
    heading.place(x=100,y=5)
    #######-----------------------------------------------------------
    def on_enter(e):
        code.delete(0,'end')
    def on_leave(e):
        if code.get()=='':
            code.insert(0,'password') 
        else:
            code.config(show='*')
        
    code = Entry(frame, width=25,fg='black',border=0,bg='white',font=('Microsoft Yahei UI Light',11))
    code.place(x=30,y=150)
    code.insert(0,'password')
    code.bind("<FocusIn>",on_enter)
    code.bind("<FocusOut>",on_leave)
     

    Frame(frame,width=295,height=2,bg='black').place(x=25,y=177)



    #######-----------------------------------------------------------
    def on_enter(e):
        confirm_code.delete(0,'end')
    def on_leave(e):
        if confirm_code.get()=='':
             confirm_code.insert(0,'confirm password') 
    

    def update_password(e):
    # Show the password if it's the default text, otherwise mask it with asterisks
        show = False
        if confirm_code.get() == 'confirm password':
            show = True
        confirm_code.config(show='' if show else '*')        
    confirm_code = Entry(frame, width=25,fg='black',border=0,bg='white',font=('Microsoft Yahei UI Light',11))
    confirm_code.place(x=30,y=220)
    confirm_code.insert(0,'confirm password')
    confirm_code.bind("<FocusIn>",on_enter)
    confirm_code.bind("<FocusOut>",on_leave)
    confirm_code.bind("<KeyRelease>", update_password)  
    Frame(frame,width=295,height=2,bg='black').place(x=25,y=247)


    #######-----------------------------------------------------------
    def on_enter(e):
        user.delete(0,'end')
    def on_leave(e):
        if user.get()=='':
             user.insert(0,'Username') 
    user = Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsoft Yahei UI Light',11))
    user.place(x=30,y=80)
    user.insert(0,'Username')
    user.bind("<FocusIn>",on_enter)
    user.bind("<FocusOut>",on_leave)
    Frame(frame,width=295,height=2,bg='black').place(x=25,y=107)
    #----------------------------------------------------------------------
    Button(frame,width=35,pady=7,text='Sign up',bg='#57a1f8',fg='white',border=0,command=signup).place(x=35,y=280)
    label=Label(frame,text='I have an account',fg='black',bg='white',font=('Microsoft Yahei UI Light',9))
    label.place(x=90,y=340)
    signin=Button(frame,width=6,text='signin',border=0,cursor='hand2',bg='white',fg='#57a1f8',command=signin)
    signin.place(x=200,y=340)




    window.mainloop()

  




#######################@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

img=PhotoImage(file='login.png')
Label(root,image=img,bg='white').place(x=50,y=50)

frame=Frame(root,width=350,height=350,bg='white')
frame.place(x=480,y=70)

heading=Label(frame,text='Login',fg='#57a1f8',bg='white',font=('Microsoft Yahei UI Light',23,'bold'))
heading.place(x=100,y=5)
###################--------------------------------

def on_enter(e):
    user.delete(0,'end')

def on_leave(e):
    name=user.get()
    if name=='':
        user.insert(0,'Username')

user=Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsoft Yahei UI Light',11))
user.place(x=30,y=80)
user.insert(0,'Username')
user.bind('<FocusIn>',on_enter)
user.bind('<FocusOut>',on_leave)

Frame(frame,width=295,height=2,bg='black').place(x=25,y=107)
##########-------------------------------------------------------------

def on_enter(e):
    code.delete(0,'end')

def on_leave(e):
    name=code.get()
    if name=='':
        code.insert(0,'Password')

def hide_pass(e):
    # Show the password if it's the default text, otherwise mask it with asterisks
        show = False
        if code.get() == 'Password':
            show = True
        code.config(show='' if show else '*')    


code=Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsoft Yahei UI Light',11))
code.place(x=30,y=150)
code.insert(0,'Password')

code.bind('<FocusIn>',on_enter)
code.bind('<FocusOut>',on_leave)
code.bind('<KeyRelease>',hide_pass)

Frame(frame,width=295,height=2,bg='black').place(x=25,y=177)
#############-------------------------------------------------------------------------------

Button(frame,width=39,pady=7,text='Login',bg='#57a1f8',fg='white',border=0,command=signin).place(x=35,y=204)
label=Label(frame,text="I don't have an account",fg='black',bg='white',font=('Microsoft Yahei UI Light',9))
label.place(x=75,y=270)

sign_up=Button(frame,width=6,text='sign up',border=0,bg='white',cursor='hand2',fg='#57a1f8',command=signup_command)
sign_up.place(x=215,y=270)



root.mainloop()