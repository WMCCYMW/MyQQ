import socket
import threading
import controller
import sys
import serverModule
IP=""
Port=""
if __name__ == '__main__':
    s=socket.socket(socket.AF_INET)
    serverModule.ss=s.connet((IP,int(Port)))
    ReciveThread=threading.Thread(target=serverModule.Reciver,args=(s,))
    cont = controller.Controller()
    sys.exit(cont.app.exec_())
