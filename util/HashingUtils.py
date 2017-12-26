# Long hash code generator from: http://www.javamex.com/tutorials/collections/strong_hash_code_implementation_2.shtml
# Ported to Python
from array import array


class HashingUtils:
    def __init__(self):
        self.HSTART = int('BB40E64DA205B064', 16)
        self.HMULT = 7664345821815920749
        self.byteTable = self.createLookupTable()

    # def rotl(self, num, bits):
    #     bit = num & (1 << (bits - 1))
    #     num <<= 1
    #     if bit:
    #         num |= 1
    #     num &= (2 ** bits - 1)
    #
    #     return num
    #
    # def rotr(self, num, bits):
    #     num_origin = num
    #     num &= (2 ** bits - 1)
    #     bit = num & 1
    #     num >>= 1
    #     if bit:
    #         num |= (1 << (bits - 1))
    #
    #     print('Received num %d (%s), right shift rotate %d bits: %d (%s)' % (num_origin, bin(num_origin), bits, num, bin(num)))
    #     return num

    def shift_rotate_right(self, num, bits):
        print('About to shift rotate %d (%s)' % (num, bin(num)))
        bits_to_rotate = num & (2 ** (bits - 1) - 1) # These are the rightmost bits bit in the argument, we need to move them to the left
        print('Bits to rotate %d (%s)' % (bits_to_rotate, bin(bits_to_rotate)))
        num >>= bits # Simple right shift (no rotate)
        print('Num shifted to %d bit to right (no rotate): %d (%s)' % (bits, num, bin(num)))
        bits_moved_to_left = bits_to_rotate << (64 - bits)
        print('New leftmost bits: %d (%s)' % (bits_moved_to_left, bin(bits_moved_to_left)))
        final_num = num | bits_moved_to_left
        print('Final number: %d (%s)' % (final_num, bin(final_num)))
        # print('Received num %d (%s), right shift rotate %d bits: %d (%s)' % (num_origin, bin(num_origin), bits, final_num, bin(final_num)))
        return final_num


    def createLookupTable(self):
        h = int('544B2FBACAAF1684', 16)
        table_of_long = []
        for i in range(256):
            for j in range(31):
                h = self.shift_rotate_right(h, 7) ^ h
                h = (h << 11) ^ h
                h = self.shift_rotate_right(h, 10) ^ h

            h &= (2 ** 65 - 1)
            print('Adding %d (%s) to table' % (h, bin(h)))
            table_of_long.append(h)

        return table_of_long

    def hashBytesToLong(self, data_bytes):
        h = self.HSTART
        hmult = self.HMULT
        ht = self.byteTable

        data_len = len(data_bytes)
        i = 0
        while i < data_len:
            h = (h * hmult) ^ ht[data_bytes[i] & int('0xff', 16)]

        return h

    def hashStringToLong(self, string):
        h = self.HSTART
        hmult = self.HMULT
        ht = self.byteTable
        str_len = len(string)

        for i in range(str_len):
            ch = string[i]
            h = (h * hmult) ^ ht[ord(ch) & int('0xff', 16)]
            h = (h * hmult) ^ ht[(self.shift_rotate_right(ord(ch), 8)) & int('0xff', 16)]

        return h

hashingUtils = HashingUtils()
nums = [0, 1, 10, 16, 20]
for num in nums:
    print(hashingUtils.shift_rotate_right(num, 3))

text = 'bilash'
print(hashingUtils.hashStringToLong("bilash"))

