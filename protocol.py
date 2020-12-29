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
    length = textwrap.wrap(BitArray(bytes(str(len(content)).zfill(LEN_OF_MSG_LENGTH), "ascii")).bin, num_of_leds)
    return start_segments + length


def _identify_start(byte_stream, num_of_leds):
    count_init = 0
    for i, byte in enumerate(byte_stream):
        if byte == "1" * num_of_leds:
            count_init += 1
            if count_init == FRAMES_PER_SECOND:
                break
        else:
            count_init = 0
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
    raw_length = byte_stream[:LEN_OF_MSG_LENGTH]
    length = int("".join([_bits2chr(byte) for byte in raw_length]))
    msg = byte_stream[LEN_OF_MSG_LENGTH:LEN_OF_MSG_LENGTH + length]
    return length, msg


def data_to_raw(file_path, num_of_leds):
    content = _apply_error_detection(_compress(_split_bytes(_read_file(file_path), NUM_OF_LEDS)))
    start = _get_start_protocol(content, num_of_leds)
    end = _get_end_protocol(num_of_leds)
    return start + content + end


def raw_to_data(byte_stream):
    decoded_msg = [_bits2chr(byte) for byte in _decompress(_detect_error(byte_stream))]
    return "".join(decoded_msg)


# import random
# file_path = r"C:\Users\t8875881\Desktop\secret.txt"
# with open(file_path) as file:
#     print("".join(file.readlines()))
# raw_data = data_to_raw(file_path, NUM_OF_LEDS)
# print("Sending:",raw_data)
# noise_length = 8
# raw_data = ["".join([str(random.randint(0, 1)) for _ in range(NUM_OF_LEDS)]) for _ in range(noise_length)] + raw_data
# beginning = _identify_start(raw_data, NUM_OF_LEDS)
# msg_length, message = _get_msg_length(beginning)
# print("Got:", message)
# print(raw_to_data(message))
