import os
import dropbox
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
import tkinter.ttk as ttk
from cryptography.fernet import Fernet
from datetime import datetime
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from pathlib import Path
from tkinter import *
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
# Explicit imports to satisfy Flake8


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH/ "assets" / "frame2"
  # This will point to the 'assets' folder in the same directory as the script

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)
# Define the initial access token 
with open("token.txt","r") as f: 
    ACCESS_TOKEN = f.read()

# Function to generate an encryption key from a password and salt
def generate_key_from_password(password, salt):
    # Create a PBKDF2HMAC key derivation function
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        iterations=100000,  # You can adjust the number of iterations
        salt=salt,
        length=32  # 32 bytes key (256 bits)
    )
    
    # Derive the encryption key from the password
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    
    return key

# Function to download and decrypt the file
def download_and_decrypt_file(shared_url, password, download_folder):
    try:
        dbx = dropbox.Dropbox(ACCESS_TOKEN)

        # Extract the file ID from the shared URL
        file_id = shared_url.split("/")[-1]

        # Download the file using the Dropbox SDK
        metadata, response = dbx.sharing_get_shared_link_file(shared_url)

        # Read the encrypted file content
        encrypted_data = response.content

        # Extract the salt from the beginning of the file
        salt_length = 16  # Length of the salt in bytes
        salt = encrypted_data[:salt_length]
        encrypted_data = encrypted_data[salt_length:]

        # Derive the encryption key using the password and salt
        encryption_key = generate_key_from_password(password, salt)

        # Decrypt the data
        cipher = Fernet(encryption_key)
        decrypted_data = cipher.decrypt(encrypted_data)

        # Extract the file name from the Dropbox metadata
        original_file_name = metadata.name

        # Remove the ".encrypted" extension if present
        if original_file_name.endswith(".encrypted"):
            original_file_name = original_file_name[:-10]  # Remove the last 10 characters (".encrypted")

        # Split the original file name and extension
        name, ext = os.path.splitext(original_file_name)

        # Construct the full file path with the original file name and extension (excluding the timestamp)
        base_file_path = os.path.join(download_folder, name + ext)

        # Check if the file already exists in the download folder
        file_path = base_file_path
        counter = 2
        while os.path.exists(file_path):
            # If the file exists, add the counter in parentheses
            file_path = os.path.join(download_folder, f"{name}({counter}){ext}")
            counter += 1

        # Save the decrypted file with the modified file name
        with open(file_path, 'wb') as decrypted_file:
            decrypted_file.write(decrypted_data)

        return file_path

    except dropbox.exceptions.ApiError as e:
        print(f'Dropbox API error: {e}')
    except Exception as e:
        print(f'Error: {e}')

# Function to check the entries and enable/disable the "Download" button
def check_entries():
    # Get the content of the URL entry and password entry
    url_content = entry_1.get()
    password_content = entry_2.get()

    # Disable the "Download" button if both fields are empty, enable it otherwise
    if not url_content or not password_content:
        button_1.config(state=tk.DISABLED)
    else:
        button_1.config(state=tk.NORMAL)

# Function to browse for a download folder and start the download and decryption process
def browse_folder():
    download_folder = filedialog.askdirectory()
    if download_folder:
        shared_url = entry_1.get()
        password = entry_2.get()  # Get the password from the password entry textbox
        if not shared_url:
            print("Please enter a shared URL.")
            return
        if not password:
            print("Please enter a decryption password.")
            return

        progress_label.config(text='Downloading and decrypting...')
        window.update()

        decrypted_file_path = download_and_decrypt_file(shared_url, password, download_folder)

        if decrypted_file_path:
            print(f"File downloaded and decrypted: {decrypted_file_path}")
            progress_label.config(text='Download and decryption completed.')

window = Tk()

window.geometry("705x400")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 400,
    width = 705,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_1 = canvas.create_image(
    352.0,
    200.0,
    image=image_image_1
)

canvas.create_text(
    187.0,
    150.0,
    anchor="nw",
    text="PASSWORD",
    fill="#000000",
    font=("Righteous Regular", 20 * -1)
)

canvas.create_text(
    187.0,
    63.0,
    anchor="nw",
    text="ENTER URL",
    fill="#000000",
    font=("Righteous Regular", 20 * -1)
)
#url_entry
entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_1 = canvas.create_image(
    338.5,
    113.0,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=203.0,
    y=93.0,
    width=271.0,
    height=38.0
)
#password_entry
entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_3.png"))
entry_bg_2 = canvas.create_image(
    338.5,
    200.0,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0,
    show="*"  # password hiding
)

entry_2.place(
    x=203.0,
    y=180.0,
    width=271.0,
    height=38.0
)
#download_button
button_image_1 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=browse_folder,
    relief="flat"
)
button_1.place(
    x=290.0,
    y=269.0,
    width=95.0,
    height=89.0
)
# Create a progress label
progress_label = ttk.Label(window, text='')
progress_label.pack(side="bottom", pady=10)
progress_label.configure(style='Custom.TLabel', background='#E6E6E6')

window.resizable(False, False)
window.mainloop()
