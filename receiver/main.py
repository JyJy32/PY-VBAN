import socket
import threading
import time
import pyaudio
from receiver.decoder import udp_decode
from data import Data, Header   
    
class VBAN_receiver():
    def __init__(self, ip: str, port: int) -> None:
        self.incomming: dict[str, Header] = {}
        self.selection: int = 0
        self.selected: Header = None
        
        self.ip: str = ip
        self.port: int = port
        
        print(f"VBAN receiver initialized with IP: {self.ip} and port: {self.port}")
        self.sock: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.ip, self.port))
        
        # PyAudio object.
        self.audio = audio = pyaudio.PyAudio()

        stream_format = pyaudio.get_format_from_width(2)
        self.stream = audio.open(format=stream_format, channels=2, rate=44100, output=True)
        
        threading.Thread(target=self.get_incomming).start()
        
    def get_incomming(self) -> dict[str, Data]:
        self.sock.settimeout(2)
        start_time = time.time()
        end_time = start_time + 2
        while time.time() < end_time:
            recv, addr = self.sock.recvfrom(1500)
            data = udp_decode(recv, addr)
            if data:
                self.incomming[f"{data.header.stream_name}@{data.header.sender}"] = data.header
                
        
    def select_stream(self) -> None:
        print("Select stream")
        for i, stream in enumerate(self.incomming):
            print(f"{i}: {stream}")
        choice = input("Select stream: ")
        try: 
            self.selection = int(choice)
        except ValueError:
            print("Invalid input")
            self.select_stream()
        try:
            self.selected = list(self.incomming.values())[self.selection]
        except Exception as e:
            print(e)
            self.select_stream()
            
        print(self.selected)
        
    def start_stream(self):
        print("Starting stream")
        self.stream.start_stream()
        
        while True:
            recv, addr = self.sock.recvfrom(1500)
            data = udp_decode(recv, addr)
            #print(f"data: {data.header}")
            if (data.header.stream_name != self.selected.stream_name) and (data.header.sender != self.selected.sender):
                continue
            if not data:
                break
            self.stream.write(data.data)
            
        self.sock.close()
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()