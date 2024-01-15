from pathlib import Path
import os
import dropbox
from dropbox.exceptions import AuthError
import tkinter as tk
from tkinter import filedialog
import tkinter.ttk as ttk
import pyperclip
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from datetime import datetime
import base64
from tkinter import messagebox
from tkinter import *
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
#Explicit imports to satisfy Flake8

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / "assets" / "frame1"



def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Define the initial access token 
with open("token.txt","r") as f: 
    ACCESS_TOKEN = f.read()

# Initialize the shared link URL as a global variable
encrypted_shared_link = ""

# Function to generate a password-based encryption key
def generate_key_from_password(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        iterations=100000,
        salt=salt,
        length=32,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key

# Function to encrypt a file using a user-provided password
def encrypt_file_with_password(file_path, password):
    salt = os.urandom(16)
    encryption_key = generate_key_from_password(password, salt)

    with open(file_path, 'rb') as file:
        data = file.read()
        cipher = Fernet(encryption_key)
        encrypted_data = cipher.encrypt(data)

    encrypted_file_path = f"{file_path}.encrypted"
    with open(encrypted_file_path, 'wb') as encrypted_file:
        encrypted_file.write(salt + encrypted_data)

    return encrypted_file_path

# Function to upload a file to Dropbox
def upload_file(file_path):
    try:
        if not os.path.isfile(file_path):
            print("File not found.")
            return

        dbx = dropbox.Dropbox(ACCESS_TOKEN)

        # Get the base filename and extension
        filename, extension = os.path.splitext(os.path.basename(file_path))

        # Initialize a counter to handle conflicts
        counter = 2
        unique_filename = filename + extension

        while True:
            dest_path = '/' + unique_filename

            try:
                dbx.files_get_metadata(dest_path)
                # A file with the same name already exists, so modify the filename
                unique_filename = f"{filename}({counter}){extension}"
                counter += 1
            except dropbox.exceptions.ApiError as e:
                break

        with open(file_path, 'rb') as file:
            dbx.files_upload(file.read(), dest_path)

        shared_link_metadata = dbx.sharing_create_shared_link(dest_path)
        shared_link_url = shared_link_metadata.url

        return shared_link_url

    except FileNotFoundError as e:
        print(f'File not found: {e}')
    except dropbox.exceptions.ApiError as e:
        print(f'Error uploading file: {e}')
def return_to_home_page():
    # Destroy the current window
    window.destroy()
    import home
    # Restart the application or navigate back to the home page
    # For simplicity, let's just print a message here
    print("Returning to the home page...")
# Function to copy the shared URL to the clipboard
def copy_url():
    global encrypted_shared_link
    pyperclip.copy(encrypted_shared_link)
    window.after(4000, return_to_home_page)

# Function to browse for a file and perform encryption, upload
def browse_file():
    global encrypted_shared_link
    password = entry_1.get()
    if not password:
        # Show a pop-up message box
        messagebox.showinfo("Password Required", "Please enter a password.")
        return

    # Continue with the file encryption and upload process

    file_path = filedialog.askopenfilename()
    if file_path:
        # Initialize the progress bar
        progress_bar['value'] = 0
        progress_label.config(text='Encrypting and uploading...')
        window.update()

        # Encrypt and upload the file
        encrypted_file_path = encrypt_file_with_password(file_path, password)
        encrypted_shared_link = upload_file(encrypted_file_path)

        if encrypted_shared_link:
            print(f"Encrypted Shared Link: {encrypted_shared_link}")
            pyperclip.copy(encrypted_shared_link)
            progress_label.config(text='Encryption and upload completed.')
        else:
            progress_label.config(text='Error occurred during encryption and upload.')

        # Set the progress bar to 100% when the process is complete
        progress_bar['value'] = 100

        # Ensure the button is enabled
        button_1.config(state=tk.NORMAL)


# Create a Tkinter window
window = Tk()

window.geometry("700x400")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 400,
    width = 700,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_1 = canvas.create_image(
    355.0,
    200.0,
    image=image_image_1
)

canvas.create_text(
    186.0,
    73.0,
    anchor="nw",
    text="PASSWORD",
    fill="#000000",
    font=("Righteous Regular", 20 * -1)
)
#password entry
entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    337.5,
    119.0,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0,
    show="*"  # Set the show attribute to "*" to mask the characters entered
)

entry_1.place(
    x=202.0,
    y=99.0,
    width=271.0,
    height=38.0
)
#button for copy url
button_image_1 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=copy_url,  # Add a comma here
    relief="flat",
)
button_1.place(
    x=283.0,
    y=238.0,
    width=95.0,
    height=89.0
)

#button for browse file
button_image_2 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=browse_file,
    relief="flat"
)
button_2.place(
    x=223.0,
    y=169.0,
    width=216.0,
    height=45.0
)
# progression bar
progress_frame = ttk.Frame(window, style="Custom.TFrame")
progress_frame.pack(side="bottom", pady=10)

# Create a custom style for the frame
window.style = ttk.Style()
window.style.configure("Custom.TFrame", background="#E6E6E6")

progress_label = ttk.Label(progress_frame,text="")
progress_label.pack(pady=5)
progress_label.configure(style='Custom.TLabel', background='#E6E6E6')

progress_bar = ttk.Progressbar(progress_frame, length=300, mode="determinate")
progress_bar.pack(pady=5)


window.resizable(False, False)
window.mainloop()
