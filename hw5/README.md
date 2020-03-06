# Address Conversion with Multi-level Page Table

## Calculate by hand

Note here valid virtual address range should be `0x0000-0x1fff` (inclusive). Thus we only need to calculate `0x1c13, 0x0af6, 0x1e6f`, while `0x6653, 0x6890` should be marked as invalid.

Take `0x1e6f` as an example:

```
0x1e6f --> 00111_10011_01111
pde_index 0x7 + pdbr 0xd80 -->
page 6c: e1 b5 a1 c1 b3 e4 a6 bd 7f 7f 7f 7f 7f 7f 7f 7f 7f 7f 7f 7f 7f 7f 7f 7f 7f 7f 7f 7f 7f 7f 7f 7f  --> selects 0xbd (1_0111101) --> valid, pfn 0x3d

page 3d: f6 7f 5d 4d 7f 04 29 7f 1e 7f ef 51 0c 1c 7f 7f 7f 76 d1 16 7f 17 ab 55 9a 65 ba 7f 7f 0b 7f 7f 
pte_index 0x13 --> selects 0x16 (0_0010110) --> valid bit not set, not 0x7f --> page on disk --> paddr: 0x2cf(0010110_01111) 

--> page 0x16 on disk, offset 0xf
disk 16: 00 0a 15 1a 03 00 09 13 1c 0a 18 03 13 07 17 1c 0d 15 0a 1a 0c 12 1e 11 0e 02 1d 10 15 14 07 13 --> data content is 0x1c
```

## Calculate through program

Please refer to `sim.py` for more details on how to perform the address conversion. Here are the outputs:

```
Please input virtual address (base 16), q to quit: 6653
Virtual address out of range

Please input virtual address (base 16), q to quit: 1c13
  --> pde index:0x7 pde contents:(valid 1, pfn 0x3d)
    --> pte index:0x0 pte contents:(valid 1, pfn 0x76)
      --> Translates to Physical Address 0xed3 --> Value: 0x12

Please input virtual address (base 16), q to quit: 6890
Virtual address out of range

Please input virtual address (base 16), q to quit: 0af6
  --> pde index:0x2 pde contents:(valid 1, pfn 0x21)
    --> pte index:0x17 pte contents:(valid 0, pfn 0x7f)
      --> Fault (page table entry not valid)

Please input virtual address (base 16), q to quit: 1e6f
  --> pde index:0x7 pde contents:(valid 1, pfn 0x3d)
    --> pte index:0x13 pte contents:(valid 0, pfn 0x16)
      --> Translates to Disk Sector Address 0x2cf --> Value: 0x1c
```

