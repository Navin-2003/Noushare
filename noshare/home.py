from pathlib import Path
from tkinter import *

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH/ "assets" / "frame0"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

window = Tk()
window.geometry("705x400")
window.configure(bg="#FFFFFF")

def nextPage():
    window.destroy()
    import s
 

def prevPage():
    window.destroy()
    import r

canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=400,
    width=705,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)
image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    352.0,
    200.0,
    image=image_image_1
)

canvas.create_text(
    486.0,
    310.0,
    anchor="nw",
    text="Receive",  # Fixed typo: "Recive" to "Receive"
    fill="#1E1B1B",
    font=("Righteous Regular", -40)  # Fixed font size: 40 * -1 to -40
)

canvas.create_text(
    137.0,
    310.0,
    anchor="nw",
    text="Send",
    fill="#1E1B1B",
    font=("Righteous Regular", -40)  # Fixed font size: 40 * -1 to -40
)

canvas.create_text(
    245.0,
    44.0,
    anchor="nw",
    text="NOUSHARE",
    fill="#000000",
    font=("Righteous Regular", -40)  # Fixed font size: 40 * -1 to -40
)

button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=nextPage,
    relief="flat"
)
button_1.place(
    x=141.0,
    y=221.0,
    width=95.0,
    height=89.0
)

button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=prevPage,
    relief="flat"
)
button_2.place(
    x=502.0,
    y=221.0,
    width=95.0,
    height=89.0
)

window.resizable(False, False)
window.mainloop()
