"""
written based on this repo: https://github.com/scardine/image_size
"""
import collections
import json
import os
import struct
import typing

FILE_UNKNOWN = "Sorry, don't know how to get size for this file."


class UnknownImageFormat(Exception):
    pass


types = collections.OrderedDict()
BMP = types['BMP'] = 'BMP'
GIF = types['GIF'] = 'GIF'
ICO = types['ICO'] = 'ICO'
JPEG = types['JPEG'] = 'JPEG'
PNG = types['PNG'] = 'PNG'
TIFF = types['TIFF'] = 'TIFF'


class ImageMetadata(typing.NamedTuple):
    type: str
    file_size: int
    width: int
    height: int

    def to_str_row(self):
        return ("%d\t%d\t%d\t%s" % (
            self.width,
            self.height,
            self.file_size,
            self.type,
        ))

    def to_str_row_verbose(self):
        return ("%d\t%d\t%d\t%s\t##%s" % (
            self.width,
            self.height,
            self.file_size,
            self.type,
            self))

    def to_str_json(self, indent=None):
        return json.dumps(self._asdict(), indent=indent)


def get_image_metadata(file_path: str) -> ImageMetadata:
    """
    Return an `ImageMetadata` object for a given img file content - no external
    dependencies except the os and struct builtin modules

    :param file_path: path to an image file
    :return: ImageMetadata: (type, file_size, width, height)
    """

    size = os.path.getsize(file_path)

    # be explicit with open arguments - we need binary mode
    with open(file_path, "rb") as f:
        return get_image_metadata_from_bytesio(f, size)


def get_image_metadata_from_bytesio(f: typing.BinaryIO, size: int) -> ImageMetadata:
    """
    Return an `ImageMetadata` object for a given img file content - no external
    dependencies except the os and struct builtin modules

    :param f: io object support read & seek
    :param size: size of buffer in byte
    :return: ImageMetadata: (type, file_size, width, height)
    """

    height = -1
    width = -1
    data = f.read(26)
    msg = " raised while trying to decode as JPEG."

    if (size >= 10) and data[:6] in (b'GIF87a', b'GIF89a'):
        # GIFs
        img_type = GIF
        w, h = struct.unpack("<HH", data[6:10])
        width = int(w)
        height = int(h)
    elif ((size >= 24) and data.startswith(b'\211PNG\r\n\032\n')
          and (data[12:16] == b'IHDR')):
        # PNGs
        img_type = PNG
        w, h = struct.unpack(">LL", data[16:24])
        width = int(w)
        height = int(h)
    elif (size >= 16) and data.startswith(b'\211PNG\r\n\032\n'):
        # older PNGs
        img_type = PNG
        w, h = struct.unpack(">LL", data[8:16])
        width = int(w)
        height = int(h)
    elif (size >= 2) and data.startswith(b'\377\330'):
        # JPEG
        img_type = JPEG
        f.seek(0)
        f.read(2)
        b = f.read(1)
        try:
            w = h = -1
            while b and ord(b) != 0xDA:
                while ord(b) != 0xFF:
                    b = f.read(1)
                while ord(b) == 0xFF:
                    b = f.read(1)
                if 0xC0 <= ord(b) <= 0xC3:
                    f.read(3)
                    h, w = struct.unpack(">HH", f.read(4))
                    break
                else:
                    f.read(
                        int(struct.unpack(">H", f.read(2))[0]) - 2)
                b = f.read(1)
            width = int(w)
            height = int(h)
        except struct.error:
            raise UnknownImageFormat("StructError" + msg)
        except ValueError:
            raise UnknownImageFormat("ValueError" + msg)
        except Exception as e:
            raise UnknownImageFormat(e.__class__.__name__ + msg)
    elif (size >= 26) and data.startswith(b'BM'):
        # BMP
        img_type = 'BMP'
        header_size = struct.unpack("<I", data[14:18])[0]
        if header_size == 12:
            w, h = struct.unpack("<HH", data[18:22])
            width = int(w)
            height = int(h)
        elif header_size >= 40:
            w, h = struct.unpack("<ii", data[18:26])
            width = int(w)
            # as h is negative when stored upside down
            height = abs(int(h))
        else:
            raise UnknownImageFormat(f"Unknown DIB header size:{header_size}")
    elif (size >= 8) and data[:4] in (b"II\052\000", b"MM\000\052"):
        # Standard TIFF, big- or little-endian
        # BigTIFF and other different but TIFF-like formats are not
        # supported currently
        img_type = TIFF
        byte_order = data[:2]
        bo_char = ">" if byte_order == "MM" else "<"
        # maps TIFF type id to size (in bytes)
        # and python format char for struct
        tiff_types = {
            1: (1, bo_char + "B"),  # BYTE
            2: (1, bo_char + "c"),  # ASCII
            3: (2, bo_char + "H"),  # SHORT
            4: (4, bo_char + "L"),  # LONG
            5: (8, bo_char + "LL"),  # RATIONAL
            6: (1, bo_char + "b"),  # SBYTE
            7: (1, bo_char + "c"),  # UNDEFINED
            8: (2, bo_char + "h"),  # SSHORT
            9: (4, bo_char + "l"),  # SLONG
            10: (8, bo_char + "ll"),  # SRATIONAL
            11: (4, bo_char + "f"),  # FLOAT
            12: (8, bo_char + "d")  # DOUBLE
        }
        ifd_offset = struct.unpack(bo_char + "L", data[4:8])[0]
        try:
            count_size = 2
            f.seek(ifd_offset)
            ec = f.read(count_size)
            ifd_entry_count = struct.unpack(bo_char + "H", ec)[0]
            # 2 bytes: TagId + 2 bytes: type + 4 bytes: count of values + 4
            # bytes: value offset
            ifd_entry_size = 12
            for i in range(ifd_entry_count):
                entry_offset = ifd_offset + count_size + i * ifd_entry_size
                f.seek(entry_offset)
                tag = f.read(2)
                tag = struct.unpack(bo_char + "H", tag)[0]
                if tag == 256 or tag == 257:
                    # if type indicates that value fits into 4 bytes, value
                    # offset is not an offset but value itself
                    _type = f.read(2)
                    _type = struct.unpack(bo_char + "H", _type)[0]
                    if _type not in tiff_types:
                        raise UnknownImageFormat(
                            "Unknown TIFF field type:" +
                            str(_type))
                    type_size = tiff_types[_type][0]
                    type_char = tiff_types[_type][1]
                    f.seek(entry_offset + 8)
                    value = f.read(type_size)
                    value = int(struct.unpack(type_char, value)[0])
                    if tag == 256:
                        width = value
                    else:
                        height = value
                if width > -1 and height > -1:
                    break
        except Exception as e:
            raise UnknownImageFormat(str(e))
    elif size >= 2:
        # see http://en.wikipedia.org/wiki/ICO_(file_format)
        img_type = 'ICO'
        f.seek(0)
        reserved = f.read(2)
        if 0 != struct.unpack("<H", reserved)[0]:
            raise UnknownImageFormat(FILE_UNKNOWN)
        _format = f.read(2)
        assert 1 == struct.unpack("<H", _format)[0]
        num = f.read(2)
        num = struct.unpack("<H", num)[0]
        if num > 1:
            import warnings
            warnings.warn("ICO File contains more than one image")
        # http://msdn.microsoft.com/en-us/library/ms997538.aspx
        w = f.read(1)
        h = f.read(1)
        width = ord(w)
        height = ord(h)
    else:
        raise UnknownImageFormat(FILE_UNKNOWN)

    return ImageMetadata(type=img_type,
                         file_size=size,
                         width=width,
                         height=height)
