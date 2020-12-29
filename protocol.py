import textwrap
from bitstring import BitArray

NUM_OF_LEDS = 8
FRAMES_PER_SECOND = 5
LEN_OF_MSG_LENGTH = 6


def _compress(bytes_to_compress):
    return bytes_to_compress


def _decompress(bytes_to_decompress):
    return bytes_to_decompress


def _apply_error_detection(byte_apply_error_detection):
    return byte_apply_error_detection


def _detect_error(byte_to_detect_errors):
    return byte_to_detect_errors


def _get_start_protocol(content, num_of_leds):
    start_segments = ['1' * num_of_leds]
    length = [str(format(len(content), "08b"))]
    return start_segments + length


def _identify_start(byte_stream, num_of_leds):
    for i, byte in enumerate(byte_stream):
        if byte == "1" * num_of_leds:
            break
    return byte_stream[i + 1:]


def _get_end_protocol(num_of_leds):
    return []


def _split_bytes(bytes_to_split, segment_length):
    return textwrap.wrap(bytes_to_split, segment_length)


def _read_file(file_path):
    stream = b''
    with open(file_path, 'rb') as binary_file:
        for line in binary_file.readlines():
            stream += line
    return BitArray(stream).bin


def _bits2chr(b):
    return ''.join(chr(int(''.join(x), 2)) for x in zip(*[iter(b)] * 8))


def _get_msg_length(byte_stream):
    raw_length = byte_stream[0]
    length = int(raw_length, 2)
    msg = byte_stream[0:length]
    return length, msg


def data_to_raw(file_path, num_of_leds):
    content = _apply_error_detection(_compress(_split_bytes(_read_file(file_path), NUM_OF_LEDS)))
    start = _get_start_protocol(content, num_of_leds)
    end = _get_end_protocol(num_of_leds)
    return start + content + end


def raw_to_data(byte_stream):
    decoded_msg = [_bits2chr(byte) for byte in _decompress(_detect_error(byte_stream))]
    return "".join(decoded_msg)


import random
file_path = r"C:\Users\t8875881\Desktop\secret.txt"
with open(file_path) as file:
    print("".join(file.readlines()))
raw_data = data_to_raw(file_path, NUM_OF_LEDS)
print("Sending:",raw_data)
# noise_length = 8
# raw_data = ["".join([str(random.randint(0, 1)) for _ in range(NUM_OF_LEDS)]) for _ in range(noise_length)] + raw_data
print("Got:", raw_data[2:])
print(raw_to_data(raw_data[2:]))
