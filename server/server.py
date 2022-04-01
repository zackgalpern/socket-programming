import socket, os

HOST = "localhost"

TCP_PORT = 6596
UDP_PORT = 6597

TCP_ADDR = (HOST, TCP_PORT)
UDP_ADDR = (HOST, UDP_PORT)

tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# udp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

tcp_server.bind(TCP_ADDR)
# udp_server.bind(UDP_ADDR)

print("Server Running")


tcp_server.listen()
# server.settimeout(5.0)
# print("TCP LISTENING")

def listAllFiles():
    files = os.listdir()
    str_files = ""
    for file in files:
        str_files += file + " "
    conn.send(str_files.encode())
    return str_files

while True:
    
    conn, addr = tcp_server.accept()
    # print(f"{addr} connected")
    command = conn.recv(1024).decode("utf-8")
    
    # print(f"COMMAND IS {command}")

    if command == "listallfiles":
        # print(f"[RECEIVED COMMAND] listallfiles")
        listAllFiles()

    elif command == "download file":
        udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        udp_server.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF, 659665)

        conn.send("COMMAND RECEIVED".encode("utf-8"))
        filename = conn.recv(1024).decode("utf-8")

        if os.path.exists(filename):
            fileSize = str(os.path.getsize(filename))
            byteString = bytes(fileSize, encoding='utf8')

            conn.send(byteString)

            ack = conn.recv(1024).decode("utf-8")
            udp_server.sendto(filename.encode(), ('localhost', 6597))

            #file handler
            file = open(filename, "rb")
            while True:
                fileData = file.read(1024)
                # print(f"FILE DATA IN SERVER IS: {fileData}")
                if not fileData:   
                    # print("NO DATA IN FILE")
                    file.close()
                    break
                udp_server.sendto(fileData, (HOST, UDP_PORT))
                # print(f"FILE DATA SENT IS {fileData}")
        udp_server.close()
        
    elif command == "download all":
        # print(f"[RECEIVED COMMAND] download all")
        
        filesToDownload = os.listdir()
        # print(f"FILES TO DOWNLOAD: {filesToDownload}")

        for fileName in filesToDownload:
            # print(f"FILENAME IS {fileName}")
            file = open(fileName, "rb")
            conn.send(fileName.encode())
            fileNameAck = conn.recv(1024).decode()
            # print(f"FILE NAME ACK: {fileNameAck}")

            fileSize = str(os.path.getsize(fileName))
            # print(f"FILE SIZE IS: {fileSize}")

            conn.send(fileSize.encode())
            fileSizeAck = conn.recv(1024).decode()
            # print(f"FILE SIZE ACK: {fileSizeAck}")

            fileData = file.read(1024)
            while fileData:
                conn.send(fileData)
                fileData = file.read(1024)
            file.close()
        conn.send("DOWNLOADS COMPLETE".encode())
            
    elif command == "exit":
        print(f"Exiting")
        conn.close()
        break