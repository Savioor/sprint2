import textwrap
from bitstring import BitArray

NUM_OF_LEDS = 8
FRAMES_PER_SECOND = 5
LEN_OF_MSG_LENGTH = 6


def _get_start_protocol(content, num_of_leds):
    start_segments = ['1' * num_of_leds]
    length = [str(format(len(content), "08b"))]
    return start_segments + length


def _identify_start(byte_stream, num_of_leds):
    for i, byte in enumerate(byte_stream):
        if byte == "1" * num_of_leds:
            break
    return byte_stream[i + 1:]


def _split_bytes(bytes_to_split, segment_length):
    return textwrap.wrap(bytes_to_split, segment_length)


def _read_file(file_path):
    stream = b''
    with open(file_path, 'rb') as binary_file:
        for line in binary_file.readlines():
            stream += line
    return BitArray(stream).bin


def _get_msg_length(byte_stream):
    raw_length = byte_stream[0]
    length = int(raw_length, 2)
    msg = byte_stream[0:length]
    return length, msg


def data_to_raw(file_path, num_of_leds):
    content = _split_bytes(_read_file(file_path), NUM_OF_LEDS)
    start = _get_start_protocol(content, num_of_leds)
    return start + content


def raw_to_data(byte_stream):
    decoded_msg = [chr(byte) for byte in byte_stream]
    return "".join(decoded_msg)

