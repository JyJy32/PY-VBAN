import socket
import threading
import pyaudio
from receiver.decoder import udp_decode
from data import Data, Header   
    
class VBAN_receiver():
    def __init__(self, ip: str, port: int) -> None:
        self.ip: str = ip
        self.port: int = port
        
        print(f"VBAN receiver initialized with IP: {self.ip} and port: {self.port}")
        self.sock: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.ip, self.port))
        
        # PyAudio object.
        self.audio = audio = pyaudio.PyAudio()

        stream_format = pyaudio.get_format_from_width(2)
        self.stream = audio.open(format=stream_format, channels=2, rate=44100, output=True)
        
        
    def start_stream(self):
        print("Starting stream")
        self.stream.start_stream()
        
        while True:
            data = udp_decode(self.sock.recvfrom(1500)[0])
            #print(f"data: {data.header}")
            if not data:
                break
            self.stream.write(data.data)
            
        self.sock.close()
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()