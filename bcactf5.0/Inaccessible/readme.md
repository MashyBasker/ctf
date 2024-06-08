# Inaccessible

For note-taking during the CTF

*Given*:

- an executable called `chall`
- this message => `I wrote a function to generate the flag, but don't worry, I bet you can't access it!`

### Setup

It is unsafe to run executables in your local machine, so we setup a VM using [Vagrant](https://www.vagrantup.com)

```bash
$ vagrant init cybersecurity/UbuntuVM # generate Vagrantfile
$ vagrant up # get the VM up and running
```
Now we need to copy the `chall` file into the VM. Find the Port number and path to private key using this:

```bash
$ vagrant ssh-config
```

To copy the file:

```
$ scp -P [port no.] -i [/path/to/private/key] [/path/to/file/in/host] vagrant@127.0.0.1:~
```

This will copy the executable to the home dir of the VM

Executing the file gave the discouraging output:
```
No flag for you >:(
```

### Reverse Engineering

> Since we are told that a function exists to generate the flag. It means that it is not called in the main() function

Examining the executable
```bash
$ file chall
chall: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/l, for GNU/Linux 2.6.32, not stripped
```

Notice the `not stripped` at the end. It means, that the debug info is present. We can use GDB!!

Let's start with setting a break-point at `main`

```gdb
(gdb) b main
Breakpoint 1 at 0x4006bc
```
main function is at the address `0x4006bc`

Disassembling the main function

```
   0x00000000004006b8 <+0>:	    push   %rbp
   0x00000000004006b9 <+1>:	    mov    %rsp,%rbp
=> 0x00000000004006bc <+4>:	    mov    $0x400754,%edi
   0x00000000004006c1 <+9>:	    callq  0x400400 <puts@plt>
   0x00000000004006c6 <+14>:	mov    $0x0,%eax
   0x00000000004006cb <+19>:	pop    %rbp
   0x00000000004006cc <+20>:	retq   
```

The arrow(`=>`) marks to the address where the EIP is pointing

We need to find the name of this mysterious function.

```bash
(gdb) info functions
```
Gives the name of all the functions but also includes all the names of stdlib and extra GNU functions. Too much noise. We need to find the functions declared in the C file.

To put it simply, we are interested in the `.text` section of the assembly. Where is the `.text`?
```bash
(gdb) info files
```
The `.text` is here:

```
0x00007ffff7a03360 - 0x00007ffff7b7bafc is .text in /lib/x86_64-linux-gnu/libc.so.6
```

This did not help.

The function we need must be around the main function. So I search for the word main. First I store the `info functions` output in `gdb.txt`

```
(gdb) set logging on
(gdb) info functions
(gdb) set logging off
```

Now,
```
$ grep -w 'main' gdb.txt
```
It is present in this chunk:
```vim
Non-debugging symbols:
0x00000000004003c8  _init
0x0000000000400400  puts@plt
0x0000000000400410  memset@plt
0x0000000000400420  __libc_start_main@plt
0x0000000000400430  __gmon_start__@plt
0x0000000000400440  _start
0x0000000000400470  deregister_tm_clones
0x00000000004004b0  register_tm_clones
0x00000000004004f0  __do_global_dtors_aux
0x0000000000400510  frame_dummy
0x0000000000400536  c
0x0000000000400599  f
0x00000000004005ea  win
0x00000000004006b8  main
0x00000000004006d0  __libc_csu_init
0x0000000000400740  __libc_csu_fini
0x0000000000400744  _fini
0x00007ffff7dd3e90  _dl_catch_exception@plt
0x00007ffff7dd3ea0  malloc@plt
0x00007ffff7dd3eb0  _dl_signal_exception@plt
0x00007ffff7dd3ec0  calloc@plt
0x00007ffff7dd3ed0  realloc@plt
0x00007ffff7dd3ee0  _dl_signal_error@plt
0x00007ffff7dd3ef0  _dl_catch_error@plt
0x00007ffff7dd3f00  free@plt
0x00007ffff7ffb7c0  __vdso_clock_gettime
0x00007ffff7ffb7c0  clock_gettime
0x00007ffff7ffb830  __vdso_gettimeofday
0x00007ffff7ffb830  gettimeofday
0x00007ffff7ffb8a0  __vdso_time
0x00007ffff7ffb8a0  time
0x00007ffff7ffb8c0  __vdso_getcpu
```

I see there is another function called `win`. Let's disassemble it

```
(gdb) disas win
```

```
   0x00000000004005ea <+0>:	    push   rbp
   0x00000000004005eb <+1>:	    mov    rbp,rsp
   0x00000000004005ee <+4>:	    push   rbx
   0x00000000004005ef <+5>:	    sub    rsp,0x48
   0x00000000004005f3 <+9>:	    lea    rax,[rbp-0x50]
   0x00000000004005f7 <+13>:	mov    edx,0x28
   0x00000000004005fc <+18>:	mov    esi,0x0
   0x0000000000400601 <+23>:	mov    rdi,rax
   0x0000000000400604 <+26>:	call   0x400410 <memset@plt>
   0x0000000000400609 <+31>:	mov    DWORD PTR [rbp-0x14],0x0
   0x0000000000400610 <+38>:	jmp    0x40069b <win+177>
   0x0000000000400615 <+43>:	mov    eax,DWORD PTR [rbp-0x14]
   0x0000000000400618 <+46>:	cdqe   
   0x000000000040061a <+48>:	mov    rbx,QWORD PTR [rax*8+0x600b80]
   0x0000000000400622 <+56>:	mov    eax,DWORD PTR [rbp-0x14]
   0x0000000000400625 <+59>:	add    eax,0x1
   0x0000000000400628 <+62>:	mov    edi,eax
   0x000000000040062a <+64>:	call   0x400599 <f>
   0x000000000040062f <+69>:	movsxd rcx,eax
   0x0000000000400632 <+72>:	mov    rax,rbx
   0x0000000000400635 <+75>:	cqo    
   0x0000000000400637 <+77>:	idiv   rcx
   0x000000000040063a <+80>:	mov    QWORD PTR [rbp-0x20],rax
   0x000000000040063e <+84>:	mov    eax,DWORD PTR [rbp-0x14]
   0x0000000000400641 <+87>:	cdqe   
   0x0000000000400643 <+89>:	movzx  eax,BYTE PTR [rax+0x600cc0]
   0x000000000040064a <+96>:	movsx  eax,al
   0x000000000040064d <+99>:	mov    edi,eax
   0x000000000040064f <+101>:	call   0x400599 <f>
   0x0000000000400654 <+106>:	mov    edx,eax
   0x0000000000400656 <+108>:	mov    rax,QWORD PTR [rbp-0x20]
   0x000000000040065a <+112>:	lea    ebx,[rdx+rax*1]
   0x000000000040065d <+115>:	mov    eax,DWORD PTR [rbp-0x14]
   0x0000000000400660 <+118>:	cdqe   
   0x0000000000400662 <+120>:	movzx  eax,BYTE PTR [rax+0x600d00]
   0x0000000000400669 <+127>:	movsx  eax,al
   0x000000000040066c <+130>:	mov    edi,eax
   0x000000000040066e <+132>:	call   0x400536 <c>
   0x0000000000400673 <+137>:	add    eax,ebx
   0x0000000000400675 <+139>:	mov    edx,eax
   0x0000000000400677 <+141>:	mov    eax,DWORD PTR [rbp-0x14]
   0x000000000040067a <+144>:	cdqe   
   0x000000000040067c <+146>:	mov    BYTE PTR [rbp+rax*1-0x50],dl
   0x0000000000400680 <+150>:	mov    eax,DWORD PTR [rbp-0x14]
   0x0000000000400683 <+153>:	cdqe   
   0x0000000000400685 <+155>:	movzx  eax,BYTE PTR [rbp+rax*1-0x50]
   0x000000000040068a <+160>:	not    eax
   0x000000000040068c <+162>:	mov    edx,eax
   0x000000000040068e <+164>:	mov    eax,DWORD PTR [rbp-0x14]
   0x0000000000400691 <+167>:	cdqe   
   0x0000000000400693 <+169>:	mov    BYTE PTR [rbp+rax*1-0x50],dl
   0x0000000000400697 <+173>:	add    DWORD PTR [rbp-0x14],0x1
   0x000000000040069b <+177>:	cmp    DWORD PTR [rbp-0x14],0x24
   0x000000000040069f <+181>:	jle    0x400615 <win+43>
   0x00000000004006a5 <+187>:	lea    rax,[rbp-0x50]
   0x00000000004006a9 <+191>:	mov    rdi,rax
   0x00000000004006ac <+194>:	call   0x400400 <puts@plt>
   0x00000000004006b1 <+199>:	add    rsp,0x48
   0x00000000004006b5 <+203>:	pop    rbx
   0x00000000004006b6 <+204>:	pop    rbp
   0x00000000004006b7 <+205>:	ret    
End of assembler dump.
```

Nice, this looks promising. We need to take the Instruction Pointer Register to point to this function and continue. GDB will execute this `win` function
Address = `0x00000000004005ea`

```
(gdb) set $rip = 0x00000000004005ea
(gdb) c
```

This will give us the flag!

### Helpful references
- [Instruction Pointer Register](https://0xinfection.github.io/reversing/pages/part-12-instruction-pointer-register.html)
- [List functions in GDB](https://stackoverflow.com/questions/10680670/ask-gdb-to-list-all-functions-in-a-program)
- [Non-debugging symbols](https://getdocs.org/Gdb/docs/latest/gdb/Non_002ddebug-DLL-Symbols)