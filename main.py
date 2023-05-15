import socket
import pyaudio
from decoder import udp_decode
from data import Data, Header

UDP_IP = input("this device's IP: ")
UDP_PORT = 8080

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

def callback(in_data, frame_count, time_info, status):
    print("callback")
    data = udp_decode(sock.recvfrom(1500)[0])
    return (data.data, pyaudio.paContinue)

# PyAudio object.
audio = pyaudio.PyAudio()

stream_format = pyaudio.get_format_from_width(2)
stream = audio.open(format=stream_format, channels=2, rate=44100, output=True)
stream.start_stream() 

while True:
    data = udp_decode(sock.recvfrom(1500)[0])
    #print(data.header)
    if not data:
        break
    stream.write(data.data)
    
sock.close()
stream.stop_stream()
stream.close()
audio.terminate()
