from receiver.main import start
import threading


threading.Thread(target=start, args=("192.168.1.11", 8080)).start()