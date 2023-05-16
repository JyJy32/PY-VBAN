from receiver.main import *
from sender.main import *
from tools import *
import threading

listener = VBAN_receiver(ip= "192.168.1.11", port= 6980)
threading.Thread(target=listener.start_stream).start()

sender = VBAN_transmitter(ip="192.168.1.5", port= 6980)
threading.Thread(target=sender.start_stream).start()

# print(int.from_bytes(bits_to_byte(int_to_bits(0, 4) + "0" + int_to_bits(1, 3)), byteorder="big"))