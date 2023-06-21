# LZ77.py, created by Marcan and updated by NinjaCheetah
import sys


class WiiLZ77:
    TYPE_LZ77 = 1

    def __init__(self, file, offset):
        self.file = file
        self.offset = offset

        self.file.seek(self.offset)

        hdr = int.from_bytes(file.read(4), "little")
        self.decompressed_length = hdr >> 8
        self.compression_type = hdr >> 4 & 0xF

        if self.compression_type != self.TYPE_LZ77:
            raise ValueError("Unsupported compression method %d" % self.compression_type)

    def decompress(self):
        dout = ""

        self.file.seek(self.offset + 0x4)

        while len(dout) < self.decompressed_length:
            flags = int.from_bytes(self.file.read(1), "little")

            for i in range(8):
                if flags & 0x80:
                    info = int.from_bytes(self.file.read(2), "big")
                    num = 3 + ((info >> 12) & 0xF)
                    # disp = info & 0xFFF
                    ptr = len(dout) - (info & 0xFFF) - 1
                    for ii in range(num):
                        dout += dout[ptr]
                        ptr += 1
                        if len(dout) >= self.decompressed_length:
                            break
                else:
                    dout += self.file.read(1).decode("unicode_escape")
                flags <<= 1
                if len(dout) >= self.decompressed_length:
                    break

        self.data = dout
        return self.data


if len(sys.argv) != 3:
    print("LZ77 Decompressor by Marcan")
    print("Updated for Python 3 by NinjaCheetah")
    print("Usage: lz77.py <input> <output>")
    exit(1)

with open(sys.argv[1], "rb") as file:
    data = file.read(4)
    magic_num = data.decode()
    if magic_num != 'LZ77':
        print("Hey, these don't match!")
        file.seek(0)

    file_data = WiiLZ77(file, file.tell())

    decompressed_data = file_data.decompress()

    with open(sys.argv[2], "w") as out_file:
        out_file.write(decompressed_data)
        out_file.close()

    file.close()
