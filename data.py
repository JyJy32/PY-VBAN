from tools import * 

SAMPLE_RATES = [
    6000,
    12000,
    24000,
    48000,
    96000,
    192000,
    384000,
    8000,
    16000,
    32000,
    64000,
    128000,
    256000,
    512000,
    11025,
    22050,
    44100,
    88200,
    176400,
    352800,
    705600,
]


class Header:
    sender: str
    vban: str
    sample_rate: int
    sub_protocol: int
    samples_per_frame: int
    channels: int
    bit_resolution: int
    codec: int
    stream_name: str
    frame_counter: int

    def __init__(
        self,
        sender: str,
        vban: str,
        sample_rate: int,
        sub_protocol: int,
        samples_per_frame: int,
        channels: int,
        bit_resolution: int,
        codec: int,
        stream_name: str,
        frame_counter: int,
    ) -> None:
        self.sender = sender
        self.vban = vban
        self.sample_rate = SAMPLE_RATES[sample_rate]
        self.sub_protocol = sub_protocol
        self.samples_per_frame = samples_per_frame
        self.channels = channels
        self.bit_resolution = bit_resolution
        self.codec = codec
        self.stream_name = stream_name
        self.frame_counter = frame_counter

    def __str__(self) -> str:
        return f"{self.vban} with {self.sample_rate}Hz and {self.channels} channels"
    
    def display_full(self) -> str:
        return f"{self.vban} with {self.sample_rate}Hz and {self.channels} channels\nsub_protocol: {self.sub_protocol}\nsamples_per_frame: {self.samples_per_frame}\nbit_resolution: {self.bit_resolution}\ncodec: {self.codec}\nstream_name: {self.stream_name}\nframe_counter: {self.frame_counter}"
    
    def as_bytes(self) -> bytes:
        # Encode the header values into a byte array
        header_bytes = bytearray()
        
        # vban
        vban_bytes = self.vban.encode("utf-8")
        header_bytes.extend(vban_bytes)
        
        # sample rate and sub protocol
        bits =  int_to_bits(self.sub_protocol, 3) + int_to_bits(SAMPLE_RATES.index(self.sample_rate), 5)
        bits_byte = bits_to_byte(bits)
        header_bytes.append(int.from_bytes(bits_byte, byteorder="big"))
        
        # sample per frame
        header_bytes.append(self.samples_per_frame)
        
        # channels
        header_bytes.append((self.channels - 1))
        
        # bit resolution and codec
        bits = int_to_bits(self.codec, 4) + "0" + int_to_bits(self.bit_resolution, 3)
        bits_byte = bits_to_byte(bits)
        header_bytes.append(int.from_bytes(bits_byte, byteorder="big"))
        
        # stream name
        stream_name_bytes = self.stream_name.encode("utf-8")
        header_bytes.extend(stream_name_bytes.ljust(16, b'\x00'))
        
        # frame counter
        frame_counter_bytes = u32_encode(self.frame_counter)
        header_bytes.extend(frame_counter_bytes)
        
        return header_bytes


class Data:
    header: Header
    data: bytes

    def __init__(self, header: Header, data: bytes) -> None:
        self.header = header
        self.data = data

    def __str__(self) -> str:
        return f"{self.header} with {len(self.data)} bytes of data"
