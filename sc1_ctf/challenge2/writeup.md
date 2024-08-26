# Status Code CTF Challenge 2 Writeup

Problem statement:

![image.png](challenge.png)

We are given:

- an executable called `chall`
- The message ⇒ “I’ve written a function that generates the flag, but don’t worry-I’m confident you won’t be able to access it”

## Setup

Performing `chmod +x` on the `chall` file and running it gives the discouraging output:

```
No flag for you >:(
```

## Reverse Engineer

> Since we are told that a function exists to generate the flag. It means that it is not called in the main() function
> 

Examining the executable,

```console
$ file chall
chall: ELF 32-bit LSB pie executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, BuildID[sha1]=ef2a1cda76f897ece1a878d657ad232434442078, for GNU/Linux 4.4.0, with debug_info, not stripped
```

Notice the `not stripped` at the end. It means, that the debug info is present. We can use [GDB](https://sourceware.org/gdb/)!

Let’s start with setting a breakpoint at main and diassembling

```console
(gdb) b main
Note: breakpoint 1 also set at pc 0x565564a1.
Breakpoint 2 at 0x565564a1: file temp.c, line 79.
(gdb) r
Starting program: /home/okabe/midland/status_code_ctf/chall 
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/usr/lib/libthread_db.so.1".

Breakpoint 1, main () at temp.c:79
79	    printf("No flag for you >:(\n");
(gdb) disas
Dump of assembler code for function main:
   0x56556488 <+0>:	lea    ecx,[esp+0x4]
   0x5655648c <+4>:	and    esp,0xfffffff0
   0x5655648f <+7>:	push   DWORD PTR [ecx-0x4]
   0x56556492 <+10>:	push   ebp
   0x56556493 <+11>:	mov    ebp,esp
   0x56556495 <+13>:	push   ebx
   0x56556496 <+14>:	push   ecx
   0x56556497 <+15>:	call   0x565564c4 <__x86.get_pc_thunk.ax>
   0x5655649c <+20>:	add    eax,0x2b58
=> 0x565564a1 <+25>:	sub    esp,0xc
   0x565564a4 <+28>:	lea    edx,[eax-0x1fe8]
   0x565564aa <+34>:	push   edx
   0x565564ab <+35>:	mov    ebx,eax
   0x565564ad <+37>:	call   0x56556060 <puts@plt>
   0x565564b2 <+42>:	add    esp,0x10
   0x565564b5 <+45>:	mov    eax,0x0
   0x565564ba <+50>:	lea    esp,[ebp-0x8]
   0x565564bd <+53>:	pop    ecx
   0x565564be <+54>:	pop    ebx
   0x565564bf <+55>:	pop    ebp
   0x565564c0 <+56>:	lea    esp,[ecx-0x4]
   0x565564c3 <+59>:	ret
End of assembler dump.`
```

The arrow(`=>`) marks to the address where the Instruction pointer register is pointing(`0x565564a1`)

We need to find the name of this mysterious function.

```console
(gdb) info functions
All defined functions:

File temp.c:
41:	int c(int);
11:	struct Node *create_node(int);
49:	int f(int);
27:	struct Node *insert(struct Node *, int);
78:	int main();
19:	void post_order(struct Node *);
67:	void win();

Non-debugging symbols:
0x56556000  _init
0x56556030  __libc_start_main@plt
0x56556040  printf@plt
0x56556050  malloc@plt
0x56556060  puts@plt
0x56556070  memset@plt
0x56556080  _start
0x565560b0  __x86.get_pc_thunk.bx
0x565561a9  __x86.get_pc_thunk.dx
0x565564c4  __x86.get_pc_thunk.ax
0x565564d0  __divdi3
0x56556660  __stack_chk_fail_local
0x5655667c  _fini
.
.
.
<Continues>
```

I see there is an interesting function called `win`. Let's disassemble it:

```console
(gdb) disas win
Dump of assembler code for function win:
   0x56556374 <+0>:	push   ebp
   0x56556375 <+1>:	mov    ebp,esp
   0x56556377 <+3>:	push   edi
   0x56556378 <+4>:	push   esi
   0x56556379 <+5>:	push   ebx
   0x5655637a <+6>:	sub    esp,0x4c
   0x5655637d <+9>:	call   0x565560b0 <__x86.get_pc_thunk.bx>
   0x56556382 <+14>:	add    ebx,0x2c72
   0x56556388 <+20>:	mov    eax,gs:0x14
   0x5655638e <+26>:	mov    DWORD PTR [ebp-0x1c],eax
   0x56556391 <+29>:	xor    eax,eax
   0x56556393 <+31>:	sub    esp,0x4
   .
   .
   .
   <Continues>
```

Looks promising. We need to take the Instruction Pointer Register(`eip`) to point to this function and continue. Address of the win function → `0x56556374`

To check what the `eip` points to use the command: 

```console
(gdb) r
Starting program: /home/okabe/midland/status_code_ctf/chall 
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/usr/lib/libthread_db.so.1".

Breakpoint 1, main () at temp.c:79
79	    printf("No flag for you >:(\n");
(gdb) x/1xw $eip
0x565564a1 <main+25>:	0x8d0cec83
```

Now let’s move this `eip` to the `win` function:

```console
(gdb) x/1xw $eip
0x565564a1 <main+25>:	0x8d0cec83
(gdb) set $eip = 0x56556374
(gdb) x/1xw $eip
0x56556374 <win>:	0x57e58955
(gdb) c
Continuing.
SC1{Y0u_Ar3_B3t33r_Th4n_07h3rs}

Program received signal SIGSEGV, Segmentation fault.
```

We got the flag!
