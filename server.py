import socket
from sys import path
from threading import Thread
import os
import json
import tqdm


#create a class that extends/inherits from Thread class
class MyThread(Thread):
    #create a constructor for our class,
    #counter is just a variable to show how can we take
    # aurguments for our thread
    UTF8 = "utf-8"
    def __init__(self, client):
        #class the parent constructor that will make sure
        # a separate thread is created, when called
        Thread.__init__(self)
        #save the counter parameter, so that we can use
        #it later
        self.client=client
        #override the run function of the Thread class
    def run(self):
        #done by this thread. It is just waiting for 1
        # second at each iteration untill we reach the
        data = self.client.recv(1024)
        print(data)
        data = data.decode(self.UTF8)
        data = json.loads(data)
        print(data[0])
        check = data[0]
        #This condition will check if client want to get list of files
        if check == "0x0000":
            file_names = os.listdir("C:\\Users\\Marhaba\Desktop\\Computer Netwroks\\Lab_08\\File-Transfer-Protocol-Using-TCP\\Files")
            if len(file_names) > 0:
                ResponseToClientFilesList= []
                ResponseToClientFilesList.append("0x0010")
                #Calculating totall size of files in bytes
                dir = "C:\\Users\\Marhaba\Desktop\\Computer Netwroks\\Lab_08\\File-Transfer-Protocol-Using-TCP\\Files"
                totalSize = 0
                for dirpath, dirnames, filenames in os.walk(dir):
                    for file in filenames:
                        file_path = os.path.join(dirpath, file)
                        if not os.path.islink(file_path):
                            totalSize += os.path.getsize(file_path)
                ResponseToClientFilesList.append(totalSize)
                ResponseToClientFilesList.append("Individual File Names --->")
                for file in file_names:
                    ResponseToClientFilesList.append(file)
                ResponseToClientFilesList= json.dumps(ResponseToClientFilesList)
                self.client.send(ResponseToClientFilesList.encode(self.UTF8))
            else:
                ResponseToClientFilesList= []
                ResponseToClientFilesList.append("0x0010")
                ResponseToClientFilesList.append("0")
                ResponseToClientFilesList.append("No files are found")
                ResponseToClientFilesList= json.dumps(ResponseToClientFilesList)
                self.client.send(ResponseToClientFilesList.encode(self.UTF8))
        elif check == "0x0001":
            file_name_for_download = data[1]
            file_names = os.listdir("C:\\Users\\Marhaba\Desktop\\Computer Netwroks\\Lab_08\\File-Transfer-Protocol-Using-TCP\\Files")
            count = file_names.count(file_name_for_download)
            if count > 0:
                BufferSize = 100 # 100 Bytes for uploading data to client
                #file size 
                fileSize = os.path.getsize("C:\\Users\\Marhaba\Desktop\\Computer Netwroks\\Lab_08\\File-Transfer-Protocol-Using-TCP\\Files\\"+file_name_for_download)
                ResponseToClientDownloadFile= []
                ResponseToClientDownloadFile.append("0x0011")
                ResponseToClientDownloadFile.append(file_name_for_download)
                sizeFile = str(fileSize)
                ResponseToClientDownloadFile.append(sizeFile)
                ResponseToClientDownloadFile= json.dumps(ResponseToClientDownloadFile)
                #Sending file name and size to client
                self.client.send(ResponseToClientDownloadFile.encode(self.UTF8))

                # Sending file from here and will use tqdm for progress bar
                progress_bar = tqdm.tqdm(range(fileSize), f"Sending {file_name_for_download}", unit="B", unit_scale=True, unit_divisor=1024)
                with open("C:\\Users\\Marhaba\Desktop\\Computer Netwroks\\Lab_08\\File-Transfer-Protocol-Using-TCP\\Files\\"+file_name_for_download, "rb") as file:
                    while True:
                        # bytes are reading from file 100
                        bytes_read = file.read(BufferSize)
                        if not bytes_read:
                            break
                        #using sendall to assure transimission in busy network
                        self.client.sendall(bytes_read)
                        #Updating progress bar
                        progress_bar.update(len(bytes_read))
                #Closing the socket
                self.client.close()
                
            else:
                ResponseToClientFilesList= []
                ResponseToClientFilesList.append("0x0011")
                ResponseToClientFilesList.append("No such file is avaiable for download")
                ResponseToClientFilesList.append("0")
                ResponseToClientFilesList= json.dumps(ResponseToClientFilesList)
                self.client.send(ResponseToClientFilesList.encode(self.UTF8))
                
                        


def main():
    Address = "localhost"

    port = 5050

    s = socket.socket()

    s.bind((Address,port))

    s.listen(5)
    print("Listening for client")
    while True:
        c,addr = s.accept()
        #Create object for our thread class
        thread=MyThread(c)
        thread.start()
if __name__=='__main__':
    main()

