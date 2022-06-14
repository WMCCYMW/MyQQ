import socket
import threading
import controller
import sys
import serverModule
IP="127.0.0.1"
Port="3456"
if __name__ == '__main__':
    serverModule.ss.connect((IP,int(Port)))
    cont = controller.Controller()
    ReciveThread=threading.Thread(target=serverModule.Reciver,args=(serverModule.ss,cont))
    ReciveThread.start()
    sys.exit(cont.app.exec_())


