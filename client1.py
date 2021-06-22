import socket
import time 
import json
import tqdm
BufferSize = 100 # 100 Bytes for downloading data from server

address = "localhost"

port = 5050

UTF8 = "utf-8"

c = socket.socket()

c.connect((address,port))
print("Enter 1 for request list of files")
print("Enter 2 for download a file")
check = input()
if check == "1":
    Get_List_of_File = []
    Get_List_of_File.append("0x0000")
    Get_List_of_File = json.dumps(Get_List_of_File)
    c.send(Get_List_of_File.encode(UTF8))    
    data = c.recv(1024)
    data = json.loads(data)    
    print(data)
elif check == "2":
    Download_File = []
    Download_File.append("0x0001")
    file_name = input("Enter file name for download --->")
    Download_File.append(file_name)
    Download_File = json.dumps(Download_File)
    Download_File = Download_File.encode(UTF8)
    #Sending file name to server for download
    c.send(Download_File)
    data = c.recv(1024)
    data = data.decode(UTF8)
    data = json.loads(data)
    fileType = data[0]
    fileName = data[1]
    fileSize = data[2]
    if fileType == "0x0011" and fileSize == "0":
        print(data)
    else:
        print(data)     
        #From server started downloading
        fileSize = int(fileSize)
        progress = tqdm.tqdm(range(fileSize), f"Receiving {fileName}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(fileName, "wb") as file:
            while True:
                #downloading data from server 
                bytesRead = c.recv(BufferSize)
                if not bytesRead:   
                    break
                #Writing data into file 
                file.write(bytesRead)
                progress.update(len(bytesRead))

        c.close()
    

