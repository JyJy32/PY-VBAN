from data import *

def udp_decode(encode: bytes):
    vban = encode[0:4].decode("utf-8")
    # sample rate and sub protocol
    bits = byte_to_bits(encode[4])
    sample_rate = bits_to_int(bits[3:8])
    sub_protocol = bits_to_int(bits[0:3])
    # sample per frame
    sample_per_frame = encode[5];
    # channels
    channels = encode[6] + 1;
    # bit resolution and codec
    bits = byte_to_bits(encode[7])
    bit_resolution = bits_to_int(bits[5:8])
    if bits[4] == 1:
        print("not valid!!")
        return
    codec = bits_to_int(bits[0:4])
    if codec != 0:
        print("expected codec 0")
        return
    # stream name
    stream_name = encode[8:24].decode("utf-8")
    # frame counter
    frame_counter = u32_decode(encode[24:28])
    
    h = Header(vban, sample_rate, sub_protocol, sample_per_frame, channels, bit_resolution, codec, stream_name, frame_counter)
    # rest of the packet
    """ hex_string = "".join(format(b, '02X') for b in encode[28:])
    print(hex_string)"""
    
    d = Data(h, encode[28:])
    print(d) # debug
    
    
def byte_to_bits(byte: int) -> list[int]:
    power_of_2 = [128, 64, 32, 16, 8, 4, 2, 1]
    bits = []
    for power in power_of_2:
        if byte >= power:
            bits.append(1)
            byte -= power
        else:
            bits.append(0)
    return bits

def bits_to_int(bits: list[int]) -> int:
    value = 0
    for index, bit in enumerate(bits):
        value += bit * 2 ** (len(bits) - index - 1)
    return value

def u32_decode(encode: bytes) -> int:
    return int.from_bytes(encode, byteorder="little", signed=False)