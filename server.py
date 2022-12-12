import socket
import threading

HOST = '127.0.0.1'
PORT = 1234 
LISTENER_LIMIT = 5
active_clients = [] 
aktif_kullanicilar = []

def listen_for_messages(client, username):
    while 1:
        message = client.recv(2048)
        if((b'*****' not in message)):
            while message:
                send_image_to_all(message)
                message = client.recv(2048)
                if len(message)<2048:
                    send_image_to_all(message)
                    print("while bitti")
                    break
            print("while sonlandı")

                
        else:
            mesaj = message.decode("utf-8")
            if mesaj != '':
                sohbet = mesaj.split("&")
                print(sohbet)
                gonderilecek_mesaj = sohbet[1]
                gonderilecek_kisi = sohbet[2]
                gonderen_kisi = sohbet[3]
                final_msg = "text_from_server," + username + '~' + gonderilecek_mesaj + '~' + gonderilecek_kisi
                send_messages_to_one(final_msg, gonderilecek_kisi, gonderen_kisi)

            else:
                print(f"The message send from client {username} is empty")
            
def send_message_to_client(client, message):
    client.sendall(message.encode())

def send_image_to_client(client, message):
    client.send(message)

def send_messages_to_one(message, gonderilecek_kisi, gonderen_kisi):
    
    for user in active_clients:
        if user[0] == gonderilecek_kisi:
            send_message_to_client(user[1], message)

    for user2 in active_clients:
        if user2[0] == gonderen_kisi:
            send_message_to_client(user2[1], message)    

def send_messages_to_all(message):

    for user in active_clients:
        send_message_to_client(user[1], message)

def send_image_to_all(message):

    for user in active_clients:
        send_image_to_client(user[1], message)

def client_handler(client):
    
    while 1:
        username = client.recv(2048).decode('utf-8')
        if username != '':
            active_clients.append((username, client))
            aktif_kullanicilar.append(username)
            c = aktif_kullanicilar
            list_message = ' '.join(c)
            send_messages_to_all("text_from_server," + list_message)
            # prompt_message = "SERVER~" + f"{username} added to the chat"
            # send_messages_to_all(prompt_message)
            break
        else:
            print("Client username is empty")

    threading.Thread(target=listen_for_messages, args=(client, username, )).start()

def main():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        
        server.bind((HOST, PORT))
        print(f"Running the server on {HOST} {PORT}")
    except:
        print(f"Unable to bind to host {HOST} and port {PORT}")

    server.listen(LISTENER_LIMIT)

    while 1:

        client, address = server.accept()
        print(f"Successfully connected to client {address[0]} {address[1]}")

        threading.Thread(target=client_handler, args=(client, )).start()
        

if __name__ == '__main__':
    main()