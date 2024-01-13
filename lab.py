from construct import (BitsInteger, ByteSwapped, BitStruct, Array)

channelsStructure = ByteSwapped(
    BitStruct("channels" / Array(16, BitsInteger(11)))
)

# struct = channelsStructure.build({"channels": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 99]})
# print(struct)

var1 = b'\x0fp@\x03\x18\xb0\x00\x05$\x00\x01\x070@\x01\x080\x00\x01\x04\x00\x00'
var2 = b'cp@\x03\x18\xb0\x00\x05$\x00\x01\x070@\x01\x080\x00\x01\x04\x00\x00'
data1 = channelsStructure.parse(var1)
print(data1)
data2 = channelsStructure.parse(var2)
print(data2)
