import tkinter as tk
from tkinter import ANCHOR, scrolledtext
import socket
import threading
from tkinter import messagebox
from tkinter import filedialog as fd

HOST = '127.0.0.1'
PORT = 1234

master = tk.Tk()
master.geometry('350x350+500+100')
master.resizable(False, False)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect():

    try:
        client.connect((HOST, PORT))
        print("Successfully connected to server")
        #add_message("[SERVER] Successfully connected to the server")
    except:
        messagebox.showerror("Unable to connect to server", f"Unable to connect to server {HOST} {PORT}")

    username = username_textbox.get()
    if username != '':
        client.sendall(username.encode())
    else:
        messagebox.showerror("Invalid username", "Username cannot be empty")

    username_textbox.config(state=tk.DISABLED)
    username_button.config(state=tk.DISABLED)

    master.destroy()

    kullanicilar = tk.Tk()
    kullanicilar.geometry("750x750+500+50")
    kullanicilar.title("Kullanıcı Listesi")
    kullanicilar.resizable(False, False)

    title = tk.Label(kullanicilar, text='Kullanıcı Listesi', fg='red', bg='black', font='Times 14 bold')
    title.pack()

    main = tk.Canvas(kullanicilar, height=700, width=700, bg="#add8e6")
    main.pack()

    frame = tk.Frame(main, bg="#66B2FF")
    frame.place(relx=0.25, rely=0.01, relheight=0.9, relwidth=0.7)

    message_box = scrolledtext.ScrolledText(frame, bg='#ECF7FA', fg='black', width=67, height=26.5)
    message_box.config(state=tk.DISABLED)
    message_box.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.8)

    def add_message(message):
        message_box.config(state=tk.NORMAL)
        message_box.insert(tk.END, message + '\n')
        message_box.config(state=tk.DISABLED)

    def send_message():
        message1 = "*****" + "&" + message_textbox.get("1.0","end")
        message2 = listbox.get(ANCHOR)
        message3 = username
        message = str(message1) + "&" + message2 + "&" + message3
        if message1 == '\n':
            messagebox.showerror("Boş Mesaj", "Boş mesaj gönderemezsiniz")
        elif message2 == '':
            messagebox.showerror("Kullanıcı Seçilmedi", "Lütfen mesajlaşmak için listeden bir kullanıcı seçiniz")
        elif message3 == message2:
            messagebox.showerror("Kendinizi Seçtiniz", "Lütfen mesajlaşmak için başka bir kullanıcı seçiniz")
        else:
            client.sendall(message.encode())
            message_textbox.delete("1.0","end")

    message_textbox = tk.Text(frame, height=5, width=60)
    message_textbox.tag_configure('style',foreground="#bfbfbf", font='Times 10 italic')
    message_textbox.place(relx=0.01, rely=0.83)

    message_button = tk.Button(frame, text="Gönder", command=send_message)
    message_button.place(relx=0.88, rely=0.83)

    listbox = tk.Listbox(kullanicilar,selectmode=tk.SINGLE)
    
    def add_list(message):
        if message not in listbox.get(0, "end"):
            listbox.insert("end", message)
        listbox.place(relx=0.05, rely=0.05, relwidth=0.2, relheight=0.9)
        
    def listen_for_lists_from_server(client):
        while 1 :
            ilk_mesaj= client.recv(2048)
            print(ilk_mesaj)
            if ("text_from_server" not in str(ilk_mesaj)):
                file = open('indir.jpg', "wb")
                while ilk_mesaj:
                    print("resim geldi")
                    file.write(ilk_mesaj)
                    ilk_mesaj = client.recv(2048)
                    if len(ilk_mesaj)<2048:
                        file.write(ilk_mesaj)
                        file.close()
                        break
                    print("resim alındı")
            else:
                print("mesaj geldi")
                message = str(ilk_mesaj).replace("\'","").split(",")[1]
                if (('~' not in message)):
                    soh = message.split(' ')
                    for kullanici in soh:
                        add_list(f"{kullanici}")
                else:
                    username = message.split("~")[0]
                    content = str(message.split("~")[1])
                    mesaj = content.replace("\\n","")
                    gonderilen = message.split("~")[2]
                    add_message(f"[{username}] → [{gonderilen}] {mesaj} ")

    threading.Thread(target=listen_for_lists_from_server, args=(client, )).start()

    def send_image(image_data):
        message = image_data
        client.send(message)

    def openfile():
        filetypes = (
            ('JPG', '*.jpg'),
            ('All files', '*.*')
        )

        file = fd.askopenfile(
            initialdir='/',
            filetypes=filetypes)

        foto = str(file.name)
        image = open(foto,"rb")
        image_data = image.read(2048)
        while image_data:
            send_image(image_data)
            image_data = image.read(2048)
        image.close()

    btn = tk.Button(kullanicilar,text="Dosya Seç" ,command=openfile)
    btn.place(x=400,y=700)
    
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

def main():
    master.mainloop()
    
if __name__ == '__main__':
    main()