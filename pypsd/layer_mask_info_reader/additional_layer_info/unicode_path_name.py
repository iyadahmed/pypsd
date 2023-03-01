from typing import BinaryIO

from pypsd.utils import read_uint32, read_unicode_string

# TODO: move descriptor reading code to its own module
from pypsd.image_resources_reader.slices import read_descriptor_structure


def read_unicode_path_name(buf: BinaryIO):
    assert read_uint32(buf) == 16

    # TODO: modify read_descriptor_structure to return the descriptor,
    #       it currently returns nothing ^^
    read_descriptor_structure(buf)
