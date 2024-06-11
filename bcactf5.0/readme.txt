Cool stuff I learnt
===================


- When the exponential of RSA is very small(e=3) we can use Coppersmith's attack(https://en.wikipedia.org/wiki/Coppersmith%27s_attack)
- When the same message is encrypted with different keys in RSA, we can use Hastad's broadcast attack(https://xanhacks.gitlab.io/ctf-docs/crypto/rsa/08-hastad-broadcast-attack/)

- Use pwntools python package when sending payload to a process. Easier to manipulate the payload.
- We can use BuiltinImporters class in a Pyjail with restricted environment(__builtins__ are disabled) (https://netsec.expert/posts/breaking-python3-eval-protections/)
- If a stream cipher uses the same key to encrypt two different plaintexts and one of the plaintexts is known as well as both of the ciphertexts, then we can use a key-reuse XOR attack to recover the other plaintext(https://en.wikipedia.org/wiki/Stream_cipher_attacks)
