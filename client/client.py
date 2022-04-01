import socket

# tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def listFiles():
    #print("listing all files")
    tcp_client.send("listallfiles".encode("utf-8"))
    files = tcp_client.recv(4096).decode()
    print(files)
    tcp_client.close()

def exit():
    tcp_client.send("exit".encode("utf-8"))
    tcp_client.close()
    
def downloadAll():
    tcp_client.send("download all".encode("utf-8"))
    # print("downloading all")

    # receive first filename 
    fileName = tcp_client.recv(1024).decode()
    # print(f"FILE NAME IS {fileName}")
    #send filename ack
    tcp_client.send("file name ACK".encode())
    # print(f"FILE DATA {fileData}")
    fileSize = int(tcp_client.recv(1024))
    # fileSizeInt = int(fileSize)
    # print(f"FILE SIZE IS {fileSize}")

    tcp_client.send("ACK".encode())

    result = "Downloaded"

    chunk = 0

    while fileName != "DOWNLOADS COMPLETE":

        newFile = open(fileName, 'wb')

        result += " " + fileName

        while fileSize > 0:
            #time for chunking again
            if fileSize > 1024:
                chunk = 1024
            else:
                chunk = fileSize
            fileData = tcp_client.recv(chunk)
            fileSize -= chunk
            newFile.write(fileData)
        
        newFile.close()
        fileName = tcp_client.recv(1024).decode().strip()
        # print(f"NEW FILE NAME IS: {fileName}")
        if fileName == "DOWNLOADS COMPLETE":
            break
        tcp_client.send("file name ack 2".encode())
        fileSize = int(tcp_client.recv(1024).decode().strip())
        tcp_client.send("file size ack 2".encode())

    tcp_client.close()
    print(result)

def downloadSingle(filename):
    udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    udp_client.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF, 659665)

    udp_client.bind((IP,UDP_PORT))

    tcp_client.send("download file".encode("utf-8"))
    #recv COMMAND RECEIVED
    cmdrecv = tcp_client.recv(1024).decode("utf-8")
    # print(cmdrecv)
    
    tcp_client.send(filename.encode("utf-8"))
    # #recv size
    fileSize = int(tcp_client.recv(1024))

    tcp_client.send("FILE SIZE ACK".encode("utf-8"))

    fileName, addr = udp_client.recvfrom(1024)

    chunk = 0
    
    newFile = open(filename, 'wb')

    while True:
        if fileSize > 1024:
            chunk = 1024
        else:
            chunk = fileSize
        fileSize -= chunk

        fileData, addr = udp_client.recvfrom(chunk)

        newFile.write(fileData)
        
        if fileSize <= 0:
            newFile.close()
            break

    print(f"Downloaded {fileName.decode()}")

while True:

    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    cmd = str(input("> "))
    cmdList = cmd.split()

    IP = "localhost"

    tcp_port = 6596
    UDP_PORT = 6597

    tcp_client.connect((IP, tcp_port))

    if len(cmdList) > 2 or len(cmdList) <= 0:
        print("Invalid Command")
    else:
        if cmdList[0] == "listallfiles":
            listFiles()
            tcp_client.close()
            
        elif cmdList[0] == "exit":
            exit()
            # tcp_client.close()
            break
        elif cmdList[0] == "download":
            if len(cmdList) != 2:
                print("Invalid Command")
            elif cmdList[1] == "all":
                downloadAll()
                tcp_client.close()
            else:
                # print(f"FILENAME IS {cmdList[1]}")
                downloadSingle(cmdList[1])
                tcp_client.close()
                # udp_client.close()
        else:
            print("Invalid Command")