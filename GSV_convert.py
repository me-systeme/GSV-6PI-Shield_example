import struct

def bytesTofloat(data):
    return struct.unpack('>f', data)[0]

def bytesTouint32(data):
    return struct.unpack('>I', data)[0]

def floatTobytes(value):
    return struct.pack('>f', value)

def uint32Tobytes(value):
    return struct.pack('>I', value)