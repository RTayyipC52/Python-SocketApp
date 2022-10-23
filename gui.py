import tkinter as tk
from tkinter import scrolledtext

master = tk.Tk()
master.geometry('350x350+500+100')
master.resizable(False, False)
    
title = tk.Label(master, text='SocketApp', fg='red', bg='black', font='Times 14 bold')
title.pack()

alan = tk.Canvas(master, height=200, width=400)
alan.pack()

master.title('SocketApp')

frame = tk.Frame(master, bg="#add8e6")
frame.place(relx=0.1, rely=0.1, relheight=0.8, relwidth=0.8)

username_label = tk.Label(frame,text="Kullanıcı Adı:",font="Times 10 bold")
username_label.place(x=20,y=70)

kullanici_adi = tk.StringVar()
username_textbox = tk.Entry(frame, textvariable=kullanici_adi)
username_textbox.place(x=110,y=70)

username_button = tk.Button(frame, text="Giriş Yap", command=master.destroy)
username_button.place(x=175,y=100)

message_box2 = scrolledtext.ScrolledText(frame, bg='#ECF7FA', fg='black', width=67, height=26.5)
message_box2.config(state=tk.DISABLED)
message_box2.place(relx=0.1, rely=0.5, relwidth=0.8, relheight=0.4)

def main():

    master.mainloop()
    
if __name__ == '__main__':
    main()