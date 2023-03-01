from typing import BinaryIO

from pypsd.utils import read_uint32


def read_text_engine_data(buf: BinaryIO):
    data_len = read_uint32(buf)
    buf.read(data_len)
