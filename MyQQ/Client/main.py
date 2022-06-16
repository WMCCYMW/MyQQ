import socket
import threading
import controller
import sys
import serverModule
IP="192.168.0.103"
Port="3457"
if __name__ == '__main__':
    try:
        s = socket.socket(socket.AF_INET)
        s.connect(("127.0.0.1",3456))
        cont = controller.Controller(s)
        ReciveThread=threading.Thread(target=serverModule.Reciver,args=(s,cont))
        ReciveThread.start()

        sys.exit(cont.app.exec_())
        ReciveThread.join()
    except Exception as e:
        print(e)


