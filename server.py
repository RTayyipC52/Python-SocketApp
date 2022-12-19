import socket
import threading

HOST = '127.0.0.1'
PORT = 1234 
LISTENER_LIMIT = 5
active_clients = [] 
active_users = []

def listen_for_messages(client, username):
    while 1:
        message = client.recv(2048)
        if((b'*****' not in message)): # image
            while message:
                send_image_to_all(message)
                message = client.recv(2048)
                if len(message)<2048:
                    send_image_to_all(message)
                    break
            print("while loop finished")

        else: # message
            incoming_message = message.decode("utf-8")
            if incoming_message != '':
                chat = incoming_message.split("&")
                print(chat)
                message_to_be_send = chat[1]
                person_to_be_send = chat[2]
                sender = chat[3]
                final_message = "message_from_server," + username + '~' + message_to_be_send + '~' + person_to_be_send
                send_messages_to_one(final_message, person_to_be_send, sender)

            else:
                print(f"The message send from client {username} is empty")
            
def send_message_to_client(client, message):
    client.sendall(message.encode())

def send_image_to_client(client, message):
    client.send(message)

def send_messages_to_one(message, person_to_be_send, sender): # Only sends message to the sender and person to be send 
    
    for user in active_clients:
        if user[0] == person_to_be_send:
            send_message_to_client(user[1], message)

    for user2 in active_clients:
        if user2[0] == sender:
            send_message_to_client(user2[1], message)    

def send_messages_to_all(message): # Sends message to all users

    for user in active_clients:
        send_message_to_client(user[1], message)

def send_image_to_all(message): # Sends image bits to the all users

    for user in active_clients:
        send_image_to_client(user[1], message)

def client_handler(client):
    
    while 1:
        username = client.recv(2048).decode('utf-8')
        if username != '':
            active_clients.append((username, client))
            active_users.append(username)
            c = active_users
            list_message = ' '.join(c)
            send_messages_to_all("message_from_server," + list_message) # Sends logged in users to the client
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