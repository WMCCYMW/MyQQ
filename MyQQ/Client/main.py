import socket
import threading
import controller
import sys
import serverModule
IP="192.168.0.103"
Port="3456"
if __name__ == '__main__':
    serverModule.ss.connect((IP,int(Port)))
    cont = controller.Controller()
    ReciveThread=threading.Thread(target=serverModule.Reciver,args=(serverModule.ss,cont))
    ReciveThread.start()
    cont = controller.Controller()
    sys.exit(cont.app.exec_())
