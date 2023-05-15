import socket
import pyaudio
import decoder

# PyAudio object.
audio = pyaudio.PyAudio()

stream_format = pyaudio.get_format_from_width(2)
stream = audio.open(format=stream_format, channels=2, rate=44100, output=True)

UDP_IP = "192.168.1.11"
UDP_PORT = 8080

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1500)
    decoder.udp_decode(data)
    
