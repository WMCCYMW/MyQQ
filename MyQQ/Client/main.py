import socket
import threading
import controller
import sys
import serverModule
IP="127.0.0.1"
Port="8888"
if __name__ == '__main__':
    serverModule.ss.connect((IP,int(Port)))
    ReciveThread=threading.Thread(target=serverModule.Reciver,args=(serverModule.ss,))
    ReciveThread.start()
    cont = controller.Controller()
    sys.exit(cont.app.exec_())
