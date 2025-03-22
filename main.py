import subprocess
from tkinter import *
from tkinter import filedialog,messagebox
from pypdf import PdfReader
import random
import pyttsx3

"""
Run the following command in your terminal to install the required packages:
    pip install -r requirements.txt
"""


#__________________________________     CONSTANT____________________________________________________
uploaded_file = None
all_text = ""
language = "en"
dir = f"track{random.randint(0,1000)}.mp3"
file_name = f"track{random.randint(0,1000)}.mp3"
player = None

#__________________________________     WINDOW SETUP________________________________________________
window = Tk()
window.geometry("600x600")
window.config(bg="#FF6500")
window.title("PDF To AudioBook Converter")

#____________________________________  FUNCTIONS      ______________________________________________
"""Upload the pdf file"""
def Upload():
    global uploaded_file
    uploaded_file = filedialog.askopenfilename(filetypes=[("pdf","*pdf")])
    if uploaded_file is not None:
        message_Label.config(text="uploaded successfully",fg="#0B192C")

def PDFtoText():
    global all_text,file_name
    """Extracting text from each page of pdf book"""
    reader = PdfReader(uploaded_file)
    number_of_pages = len(reader.pages)
    for pg in range(number_of_pages):
        page = reader.pages[pg]
        all_text += page.extract_text()

    """Using pyttsx3 to turn text into voice"""

    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty("voices")

    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 145)

    engine.save_to_file(all_text, file_name)
    engine.runAndWait()
    generate_Btn.config(text="Generate ")
    message_Label.config(text="Done")

def Generate():
    """Changing Button and Label when generate btn trigered"""
    if uploaded_file is not None:
        message_Label.config(text="")
        window.update_idletasks()
        generate_Btn.config(text="Please Wait... ")
        window.after(1000,PDFtoText)
    else:
        message_Label.config(text="Upload your pdf before generating..!", fg="yellow")


def Save_path():
    global dir,file_name
    dir = filedialog.askdirectory(title="Select folder to to save your file:")
    file_name = f"{dir}/Tts-{random.randint(0,1000)}.mp3"

    # audio_book.save(f"{dir}/ABM-{rand_num}.mp3")
def Play():
    global player
    if player is None:
        play_Btn.config(bg="green")

        player = subprocess.Popen([file_name],shell=True)

#_________________________________UI CONFIGURATION__________________________________________________
"""Labels"""
desc_Label = Label(text="Upload your PDF file to create an audio book",font=("Courier",16),fg="#0B192C",bg="#FF6500")
desc_Label.place(x=5,y=50)

message_Label = Label(text="Upload your File..!set save location then generate",font=("Courier",13),fg="#0B192C",bg="#FF6500")
message_Label.place(x=50,y=484)

"""Buttons"""
upload_Btn = Button(text="UPLOAD",command=Upload,bg="#1E3E62",fg="white",width=10)
upload_Btn.place(x=160,y=450)

generate_Btn = Button(text="generate",command=Generate,bg="#1E3E62",fg="white",width=10)
generate_Btn.place(x=270,y=450)

save_path_BTM = Button(text="Save location",command=Save_path,bg="#1E3E62",fg="white",width=10)
save_path_BTM.place(x=370,y=450)


play_Btn = Button(text="Play",command=Play,bg="#0B192C",fg="white",width=8)
play_Btn.place(x=277,y=520)


"""image"""
canvas_image = Canvas(window,height=300,width=300,highlightthickness=0)
image =PhotoImage(file="OIG3555.png")
canvas_image.create_image(0,0,anchor=NW,image=image)
canvas_image.place(x=155,y=115)


window.mainloop()

