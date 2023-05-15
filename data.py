SAMPLE_RATES = [6000, 12000, 24000, 48000, 96000, 192000, 384000, 
                8000, 16000, 32000, 64000, 128000, 256000, 512000, 
                11025, 22050, 44100, 88200, 176400, 352800, 705600]

class Header():
    vban: str
    sample_rate: int
    sub_protocol: int
    samples_per_frame: int
    channels: int
    bit_resolution: int
    codec: int
    stream_name: str
    frame_counter: int
    
    def __init__(self, vban: str, sample_rate: int, sub_protocol: int, samples_per_frame: int, channels: int, bit_resolution: int, codec: int, stream_name: str, frame_counter: int) -> None:
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
        
class Data():
    header: Header
    data: bytes
    
    def __init__(self, header: Header, data: bytes) -> None:
        self.header = header
        self.data = data
        
    def __str__(self) -> str:
        return f"{self.header} with {len(self.data)} bytes of data"