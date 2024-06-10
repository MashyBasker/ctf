def find_leftmost_set_bit(num):
    # Function to find the position of the leftmost set bit
    position = 0
    while num > 1:
        num >>= 1
        position += 1
    return position

def encrypt(plaintext: str):
    enc_plaintext = ""

    for letter in plaintext:
        cp = int("10011", 2)
        cp_length = cp.bit_length()
        bin_letter, rem = ord(letter), ord(letter) * 2**(cp_length - 1)
        while (rem.bit_length() >= cp_length):
            first_pos = find_leftmost_set_bit(rem)
            rem = rem ^ (cp << (first_pos - cp_length))
        enc_plaintext += format(bin_letter, "08b") + format(rem, "0" + f"{cp_length - 1}" + "b")

    return enc_plaintext

def check_errors(encrypted_text):
    plaintext = ""
    cp = int("10011", 2)  # Fixed polynomial
    cp_length = cp.bit_length()

    for i in range(0, len(encrypted_text), 16):
        # Extract ASCII value and remainder from each 16-bit segment
        bin_letter = encrypted_text[i:i+8]
        rem = int(encrypted_text[i+8:i+16], 2)

        # Compute CRC-like checksum
        bin_letter_value = int(bin_letter, 2)
        while rem.bit_length() >= cp_length:
            first_pos = find_leftmost_set_bit(rem)
            rem = rem ^ (cp << (first_pos - cp_length))

        # Compare computed checksum with provided checksum
        if rem == 0:
            plaintext += chr(bin_letter_value)

    return plaintext

# Example usage
encrypted_text = encrypt("Hello, world!")
print("Encrypted text:", encrypted_text)

# Check for errors
plaintext = check_errors(encrypted_text)
print("Decrypted plaintext:", plaintext)
