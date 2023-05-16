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

def int_to_bits(value, num_bits):
    return bin(value)[2:].zfill(num_bits)

def bits_to_byte(bits):
    return int(bits, 2).to_bytes(1, byteorder='big')

def u32_encode(value):
    return value.to_bytes(4, byteorder='big')