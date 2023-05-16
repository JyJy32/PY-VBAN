from data import Data, Header

def udp_encode(header: Header, data: bytes) -> bytes:
    packet = bytes()
    packet += header.as_bytes()
    
    packet += data
    return packet