## RSA Noob

If e = 1, we can get the plaintext by

$plaintext = ciphertext \mod modulus$

Converting the plaintext number to ascii

$$
(a mod b) mod b = a
$$

```python
message = ciphertext % modulus
plaintext_ascii = ""
while message > 0:
    ascii_value = message % 256  # Assuming ASCII range (0-255)
    plaintext_ascii = chr(ascii_value) + plaintext_ascii
    message //= 256  # Move to the next character block

return plaintext_ascii
```
