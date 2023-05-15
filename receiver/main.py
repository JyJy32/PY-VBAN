import socket
import pyaudio
from receiver.decoder import udp_decode
from data import Data, Header

def start(ip: str, port: int) -> None:
    UDP_IP = ip
    UDP_PORT = port

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

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