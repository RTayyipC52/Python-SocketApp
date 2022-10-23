import tkinter as tk
from tkinter import scrolledtext
import socket
from tkinter import messagebox

HOST = '127.0.0.1'
PORT = 1234

master = tk.Tk()
master.geometry('350x350+500+100')
master.resizable(False, False)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect():
    def add_message(message):
        message_box2.config(state=tk.NORMAL)
        message_box2.insert(tk.END, message + '\n')
        message_box2.config(state=tk.DISABLED)

    try:
        client.connect((HOST, PORT))
        print("Successfully connected to server")
        add_message("[SERVER] Successfully connected to the server")
    except:
        messagebox.showerror("Unable to connect to server", f"Unable to connect to server {HOST} {PORT}")

    username = username_textbox.get()
    if username != '':
        client.sendall(username.encode())
    else:
        messagebox.showerror("Invalid username", "Username cannot be empty")

    username_textbox.config(state=tk.DISABLED)
    username_button.config(state=tk.DISABLED)

    #master.destroy()

    kullanicilar = tk.Tk()
    kullanicilar.geometry("600x600+500+100")
    kullanicilar.title("Kullanıcı Listesi")
    kullanicilar.resizable(False, False)

    title = tk.Label(kullanicilar, text='Kullanıcı Listesi', fg='red', bg='black', font='Times 14 bold')
    title.pack()

    main = tk.Canvas(kullanicilar, height=550, width=550, bg="#add8e6")
    main.pack()

    listbox = tk.Listbox(kullanicilar,selectmode=tk.SINGLE)

    btn = tk.Button(kullanicilar,text="Seç" ,command=kullanicilar.destroy)
    btn.place(x=400,y=550)

    kullanicilar.mainloop()
    
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

username_button = tk.Button(frame, text="Giriş Yap", command=connect)
username_button.place(x=175,y=100)

message_box2 = scrolledtext.ScrolledText(frame, bg='#ECF7FA', fg='black', width=67, height=26.5)
message_box2.config(state=tk.DISABLED)
message_box2.place(relx=0.1, rely=0.5, relwidth=0.8, relheight=0.4)

def main():

    master.mainloop()
    
if __name__ == '__main__':
    main()