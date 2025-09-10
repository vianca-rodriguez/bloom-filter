import sys
import csv
import math
import hashlib
import array

def makeBitArray(bitSize, fill = 0):
        intSize = bitSize >> 5                   # number of 32 bit integers
        if (bitSize & 31):                      # if bitSize != (32 * n) add
            intSize += 1                        #    a record for stragglers
        if fill == 1:
            fill = 4294967295                                 # all bits set
        else:
            fill = 0                                      # all bits cleared

        bitArray = array.array('I')          # 'I' = unsigned 32-bit integer
        bitArray.extend((fill,) * intSize)
        return(bitArray)

# testBit() returns a nonzero result, 2**offset, if the bit at 'bit_num' is set to 1.
def testBit(array_name, bit_num):
    record = bit_num >> 5
    offset = bit_num & 31
    mask = 1 << offset
    return(array_name[record] & mask)

# setBit() returns an integer with the bit at 'bit_num' set to 1.
def setBit(array_name, bit_num):
    record = bit_num >> 5              # which 32-bit block (same as dividing by 32)
    offset = bit_num & 31              # which bit inside that block (mod 32)
    mask = 1 << offset                 # bitmask with 1 at the correct position
    array_name[record] |= mask         # use OR to set the bit

# generate k for each email
def get_hashes(email, k, m):
    positions = []
    for i in range(k):
        to_hash = email + str(i)
        hash_digest = hashlib.sha256(to_hash.encode('utf-8')).hexdigest()
        hash_int = int(hash_digest, 16)
        positions.append(hash_int % m)
    return positions


if len(sys.argv) > 1:
    # get input file emails
    insert = sys.argv[1]
    check = sys.argv[2]
    emails_insert = []
    emails_check = []

    # Read the files
    with open(insert, "r") as emails:
        csvreader = csv.reader(emails)
        next(csvreader)
        for i in csvreader:
            emails_insert.append(i[0])

    with open(check, "r") as checks:
        csvreader = csv.reader(checks)
        next(csvreader)
        for i in csvreader:
            emails_check.append(i[0])

    n = len(emails_insert)
    p = 0.0000001                           # false positive probability
    # Calculate m and k
    m = int(-(n * math.log(p)) / (math.log(2) ** 2))
    k = int((m / n) * math.log(2))

    # Initialize Bloom filter
    bit_array = makeBitArray(m)

    # Insert emails into Bloom filter
    for email in emails_insert:
        positions = get_hashes(email, k, m)
        for i in positions:
            setBit(bit_array, i)

    # Check emails
    for email in emails_check:
        positions = get_hashes(email, k, m)
        if all(testBit(bit_array, i) for i in positions):
            print(f"{email},Probably in the DB")
        else:
            print(f"{email},Not in the DB")



