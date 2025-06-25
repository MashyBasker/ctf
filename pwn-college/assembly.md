Assembly the programs into ELF with `gcc`

```shell
gcc -nostdlib prog.s -o prog
/challenge/run prog
```

### level 1

```asm
.intel_syntax noprefix
mov rdi, 0x1337
```

### level 2

```asm
.intel_syntax noprefix
mov rax, 0x1337
mov r12, 0xCAFED00D1337BEEF
mov rsp, 0x31337
```

### level 3

```asm
.intel_syntax noprefix
add rdi, 0x331337
```

### level 4

`imul rdi, rsi` => `rdi = rdi * rsi`
`add rdi, rdx` => `rdi = rdi + rdx`

```asm
.intel_syntax noprefix

imul rdi, rsi
add  rdi, rdx
mov  rax, rdi
```

### level 5

> Notes

The `div` instruction performs integer division

For the instruction div reg, the following happens:

    rax = rdx:rax / reg
    rdx = remainder

rdx:rax means that rdx will be the upper 64-bits of the 128-bit dividend and rax will be the lower 64-bits of the 128-bit dividend.

You must be careful about what is in rdx and rax before you call div.

Code:

```asm
.intel_syntax noprefix

# distance = rdi
# time = rsi
# speed = rax
# compute: speed = distance / time

mov rax, rdi # move rdi to tax
div rsi      # divide rax / rsi and store quotient in rax. rdx stores the remainder
```

### level 6

Code:

```asm
.intel_syntax noprefix
mov rax, rdi
xor rdx, rdx
div rsi
mov rax, rdx
```


### level 7

```
MSB                                    LSB
+----------------------------------------+
|                   rax                  |
+--------------------+-------------------+
                     |        eax        |
                     +---------+---------+
                               |   ax    |
                               +----+----+
                               | ah | al |
                               +----+----+
```


Code:

```asm
.intel_syntax noprefix
mov ax, 0x42
```


### level 8

We can use a math trick to optimize the modulo operator (%). Compilers use this trick a lot.
If we have x % y, and y is a power of 2, such as 2^n, the result will be the lower n bits of x.
Therefore, we can use the lower register byte access to efficiently implement modulo!

```asm
.intel_syntax noprefix
mov al, dl # rdi % 256 => lower 8-byte of rdi
mov bx, si # rsi % 65536 => lower 16-byte of rsi
```


### level 9

We shift right by 32 bits because each byte is 8 bits, and the 5th least significant byte (counting from the right) starts at bit 32. Shifting rdi right by 32 moves that byte (bits 39–32) down to the lowest 8 bits (bits 7–0), making it easy to isolate

```asm
.intel_syntax noprefix
shl rdi, 32
mov al, dil
```
