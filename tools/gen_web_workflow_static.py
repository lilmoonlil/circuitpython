# SPDX-FileCopyrightText: 2014 MicroPython & CircuitPython contributors (https://github.com/adafruit/circuitpython/graphs/contributors)
#
# SPDX-License-Identifier: MIT

import argparse
import gzip
import mimetypes
import pathlib

parser = argparse.ArgumentParser(description="Generate displayio resources.")
parser.add_argument("--output_c_file", type=argparse.FileType("w"), required=True)
parser.add_argument("files", metavar="FILE", type=argparse.FileType("rb"), nargs="+")

args = parser.parse_args()


c_file = args.output_c_file

c_file.write(f"// Autogenerated by tools/gen_web_workflow_static.py\n")
c_file.write(f"#include <stdint.h>\n\n")

for f in args.files:
    path = pathlib.Path(f.name)
    variable = path.name.replace(".", "_")
    uncompressed = f.read()
    ulen = len(uncompressed)
    compressed = gzip.compress(uncompressed)
    clen = len(compressed)
    compressed = ", ".join([hex(x) for x in compressed])
    mime = mimetypes.guess_type(f.name)[0]

    c_file.write(f"// {f.name}\n")
    c_file.write(f"// Original length: {ulen} Compressed length: {clen}\n")
    c_file.write(f"const uint32_t {variable}_length = {clen};\n")
    c_file.write(f'const char* {variable}_content_type = "{mime}";\n')
    c_file.write(f"const uint8_t {variable}[{clen}] = {{{compressed}}};\n\n")
