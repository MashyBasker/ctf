def xor_strings(s1, s2):
    # Determine the length of the shorter string
    min_len = min(len(s1), len(s2))
    
    # Convert strings to byte arrays
    b1 = bytearray(s1, 'utf-8')
    b2 = bytearray(s2, 'utf-8')
    
    # Perform XOR operation on corresponding bytes up to the length of the shorter string
    result = bytearray()
    for i in range(min_len):
        result.append(b1[i] ^ b2[i])
    
    # Convert result back to string
    return str(result, 'utf-8')

# Example usage
string1 = "903c242d21dd7ec623cf9336e2d2211a"
string2 = "2ff87897e9f3f0aac4e8b52e22f270e305aa52358b08bce1b7ce90ab91e24a27"
xor_result = xor_strings(string2, string1)
print("XOR result:", xor_result)

# s1 = "QYYZXX[]QY\Q[SZ"
# s2 = "903c242d21dd7ec623cf9336e2d2211a"
# print(xor_strings(s1,s2))

# keystream = _UUT[
    
# 903c242d21dd7ec623cf9336e2d2211a
# p1 xor p2 xor k ==> QYYZXX[]QY\Q[SZ