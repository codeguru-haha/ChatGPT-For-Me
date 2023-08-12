import openai
from tkinter import *
import customtkinter
import pyperclip
from config import *

root = customtkinter.CTk()  # create a root widget   

openai.api_key=API_KEY
messages = []
bid_theme = BID_THEME
input_chatgpt_text = " "

option = IntVar()

# --- theme change fun ---

def theme_Change():
    if (str(button_theme.cget('text')) == "Dark"):
        button_theme.configure(text = 'Light')
        customtkinter.set_appearance_mode('light')
    else:
        button_theme.configure(text = 'Dark')
        customtkinter.set_appearance_mode('dark')

# --- bid generate fun ---

def bid_Generator():
    global input_chatgpt_text
    job_description = text_in.get("1.0","end-1c") 
    if (job_description.strip() == ""):
        return
    ShowChoice()
    messages.append({"role": "user", "content": input_chatgpt_text})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages)

    # response = openai.Completion.create(
    #               engine='davinci',
                    # prompt='Once upon a time...',
                    # max_tokens=100
    #         )
    # print(response)
    reply = response["choices"][0]["message"]["content"]
    text_out.delete("1.0", END)
    pyperclip.copy(reply)
    text_out.insert("1.0", reply) 

    messages.append({"role": "assistant", "content": reply})

# --- clear Description fun ---

def clear_Description():
    text_in.delete("1.0", END)

# --- clear Description fun ---

def all_Clear():
    global messages
    messages = []
    text_in.delete("1.0", END)
    text_out.delete("1.0", END)
    option.set(1)

# --- theme button ---

button_theme = customtkinter.CTkButton(root, text="Dark",font=customtkinter.CTkFont( weight="bold", size=17), fg_color="#23a9dd", height=60, border_width=6, corner_radius=30, width=80, command=theme_Change)
button_theme.place(x=0, y=0)

#  --- chat generator button ---

button_generator = customtkinter.CTkButton(root, text="Generator",font=customtkinter.CTkFont( weight="bold", size=17),fg_color="#aa0011", height=60, border_width=5, corner_radius=30, command=bid_Generator)
button_generator.pack()

# --- all history clear button ---

customtkinter.CTkButton(root, text="New",font=customtkinter.CTkFont( weight="bold", size=17),fg_color="#23a9dd", height=60, border_width=5, width=80, corner_radius=30, command=all_Clear).place(x=400, y= 0)

# --- input text ---

customtkinter.CTkLabel(root, text="Description", font=customtkinter.CTkFont( "",20, "bold")).pack()
text_in = customtkinter.CTkTextbox(root, width=500, height=150, font=customtkinter.CTkFont("Times New Roman", 15, "bold"))
text_in.pack()

# --- output text ---

customtkinter.CTkLabel(root, text="Answer", font=customtkinter.CTkFont( "",20, "bold")).pack()
text_out = customtkinter.CTkTextbox(root, width=500, height=450, font=customtkinter.CTkFont("Times New Roman", 16, "bold"))
text_out.pack()

#  --- option set ---

languages = [("Proposal", 1),
   	        ("Mean", 2),
            ("Answer", 3),
            ("General", 4)]

def ShowChoice():
    global input_chatgpt_text
    job_description = text_in.get("1.0","end-1c")
    match option.get():
        case 1:
            my_name = txt_name.get()
            input_chatgpt_text = SET_BID + my_name + "Job Description : \" " + job_description +"\" \n"  # + bid_theme 
        case 2:
            input_chatgpt_text = "\"" + job_description + SET_MEAN
        case 3:
            input_chatgpt_text = SET_ANSWER + job_description +"\""
        case _:
            input_chatgpt_text = job_description

for language, val in languages:
    Radiobutton(root, 
                  text=language,
                  indicatoron = 0,
                  width = 15,
                  variable=option, 
                  font=customtkinter.CTkFont("Times New Roman", 16, "bold"),
                  command=ShowChoice,
                  value=val).place(anchor=W, x=340, y=70 + val *30)
option.set(1)

# --- description clear button ---

customtkinter.CTkButton(root, text="Clear",font=customtkinter.CTkFont( weight="bold", size=15),fg_color="#23a9dd", height=40, border_width=5, width=80, corner_radius=30, command=clear_Description).place(x=420, y= 210)

# --- Input Name ---

customtkinter.CTkLabel(root, text="Name : ", font=customtkinter.CTkFont( weight="bold", size=15)).place(x=0, y=239)
txt_name = customtkinter.CTkEntry(root, font=customtkinter.CTkFont( weight="bold", size=15))
txt_name.place(x=50, y= 239)

# --- root ---

customtkinter.set_appearance_mode("dark")
root.minsize(500,700)
root.maxsize(500,700)
root.title("My ChatGPT")
root.geometry("500x700+1400+30")  # width x height + x + y
root.mainloop()