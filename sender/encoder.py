from data import Data, Header

def udp_encode(header: Header, data: bytes) -> bytes:
    packet = bytes()
    packet += header.as_bytes()
    # print(len(packet))
    packet += data
    return packet