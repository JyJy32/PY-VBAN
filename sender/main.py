import pyaudio
import socket
from sender.encoder import udp_encode

from data import Header

class VBAN_transmitter():
    def __init__(self, ip: str, port: int) -> None:
        self.ip: str = ip
        self.port: int = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        self.header = Header("VBAN", 16, 0, 255, 2, 1, 0, "Stream1", 0)
        # print(self.header.as_bytes())
        print(f"VBAN transmitter initialized with IP: {self.ip} and port: {self.port}")
        audio = pyaudio.PyAudio()
        self.stream = audio.open(format=pyaudio.paInt16, channels=2, rate=44100, input=True, frames_per_buffer=256)
        
    
    def start_stream(self):
        while True:
            data = self.stream.read(256)
            packet = udp_encode(self.header, data)
            self.sock.sendto(packet, (self.ip, self.port))
            self.header.frame_counter += 1
            