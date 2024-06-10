# Broken C Code

We are given a binary which when executed gives us a corrupted string that looks like the flag.

> Use GDB but does not help(yet!)

Put the binary to a decompiler => https://dogbolt.org/

See a (mostly) common main function in all the decompiler outputs


**Ghidra output**
```c
undefined8 main(void)

{
  uint uVar1;
  long lVar2;
  undefined8 *puVar3;
  undefined8 *puVar4;
  byte bVar5;
  double dVar6;
  undefined8 local_a8 [19];
  uint local_c;
  
  bVar5 = 0;
  puts("Here\'s your flag!\n");
  puVar3 = &DAT_00400800;
  puVar4 = local_a8;
  for (lVar2 = 0x13; lVar2 != 0; lVar2 = lVar2 + -1) {
    *puVar4 = *puVar3;
    puVar3 = puVar3 + (ulong)bVar5 * -2 + 1;
    puVar4 = puVar4 + (ulong)bVar5 * -2 + 1;
  }
  for (local_c = 0; uVar1 = local_c, local_c < 0x98; local_c = local_c + 1) {
    local_c = local_c + 1;
    dVar6 = sqrt((double)(*(int *)((long)local_a8 + (long)(int)uVar1 * 4) + -3));
    putchar((int)(char)(int)dVar6);
  }
  return 0;
}
```

**Hex-Rays output**
```c
int __fastcall main(int argc, const char **argv, const char **envp)
{
  int v3; // eax
  double v4; // xmm0_8
  int v6[39]; // [rsp+0h] [rbp-A0h] BYREF
  unsigned int i; // [rsp+9Ch] [rbp-4h]

  puts("Here's your flag!\n");
  qmemcpy(v6, &unk_400800, 0x98uLL);
  for ( i = 0; i <= 0x97; ++i )
  {
    v3 = i++;
    v4 = sqrt((double)(v6[v3] - 3));
    putchar((char)(int)v4);
  }
  return 0;
}
``````

152 bytes are copied to `v6` from the address `0x400800` and computations are performed. We need to see what is stored at `0x400800` and takes the first 39 values. `(152 / 4 => 38)`

```
(gdb) x/39dw 0x400800
0x400800:	9607	9804	9412	9804
0x400810:	13459	10407	15132	9804
0x400820:	9028	9804	2307	10003
0x400830:	4764	9028	10407	5332
0x400840:	7747	10204	4627	9028
0x400850:	3028	5187	2707	6087
0x400860:	5628	2812	9028	3028
0x400870:	2919	2503	2707	3028
0x400880:	3139	2503	3028	2919
0x400890:	15628	103	990059265
```

x -> examine\
/39 -> 39 units\
d -> in decimal format\
w -> as words(4 bytes)


These are the integers we need. We use this data to simulate the main function. The `script.py` is provided with the writeup

We get the output from it



