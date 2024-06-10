#!/usr/bin/env python

import math

# Actual data extracted from memory
unk_400800 = [
    9607, 9804, 9412, 9804,
    13459, 10407, 15132, 9804,
    9028, 9804, 2307, 10003,
    4764, 9028, 10407, 5332,
    7747, 10204, 4627, 9028,
    3028, 5187, 2707, 6087,
    5628, 2812, 9028, 3028,
    2919, 2503, 2707, 3028,
    3139, 2503, 3028, 2919,
    15628, 103, 990059265
] # array stored at 0x400800

def main():
    # equivalent to the memcpy
    v6 = unk_400800[:38]
    output = ""
    
    print("Here's your flag!\n", end="")
    
    i = 0
    while i < len(v6):
        v3 = i
        # weird math done to generate flag
        try:
            v4 = math.sqrt(v6[v3] - 3)
            output += chr(int(v4))
        # if some problematic value is received, use a ? instead of failing
        except ValueError:
            output += '?'
        
        i += 1
        if i >= len(v6):
            break
    
    print(output)

if __name__ == "__main__":
    main()

