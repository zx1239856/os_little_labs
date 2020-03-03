# Address Conversion with Multi-level Page Table

Please refer to `sim.py` for more details on how to perform the address conversion. Here are the outputs:

```
Read 4096 bytes into mem

Please input virtual address (base 16), q to quit: 6c74
  --> pde index:0x1b pde contents:(valid 1, pfn 0x20)
    --> pte index:0x 3 pte contents:(valid 1, pfn 0x61)
      --> Translates to Physical Address 0x c34 --> Value: 0x 6

Please input virtual address (base 16), q to quit: 6b22
  --> pde index:0x1a pde contents:(valid 1, pfn 0x52)
    --> pte index:0x19 pte contents:(valid 1, pfn 0x47)
      --> Translates to Physical Address 0x 8e2 --> Value: 0x1a

Please input virtual address (base 16), q to quit: 03df
  --> pde index:0x 0 pde contents:(valid 1, pfn 0x5a)
    --> pte index:0x1e pte contents:(valid 1, pfn 0x 5)
      --> Translates to Physical Address 0x  bf --> Value: 0x f

Please input virtual address (base 16), q to quit: 69dc
  --> pde index:0x1a pde contents:(valid 1, pfn 0x52)
    --> pte index:0x e pte contents:(valid 0, pfn 0x7f)
      --> Fault (page table entry not valid)

Please input virtual address (base 16), q to quit: 317a
  --> pde index:0x c pde contents:(valid 1, pfn 0x18)
    --> pte index:0x b pte contents:(valid 1, pfn 0x35)
      --> Translates to Physical Address 0x 6ba --> Value: 0x1e

Please input virtual address (base 16), q to quit: 4546
  --> pde index:0x11 pde contents:(valid 1, pfn 0x21)
    --> pte index:0x a pte contents:(valid 0, pfn 0x7f)
      --> Fault (page table entry not valid)

Please input virtual address (base 16), q to quit: 2c03
  --> pde index:0x b pde contents:(valid 1, pfn 0x44)
    --> pte index:0x 0 pte contents:(valid 1, pfn 0x57)
      --> Translates to Physical Address 0x ae3 --> Value: 0x16

Please input virtual address (base 16), q to quit: 7fd7
  --> pde index:0x1f pde contents:(valid 1, pfn 0x12)
    --> pte index:0x1e pte contents:(valid 0, pfn 0x7f)
      --> Fault (page table entry not valid)

Please input virtual address (base 16), q to quit: 390e
  --> pde index:0x e pde contents:(valid 0, pfn 0x7f)
    --> Fault (page directory entry not valid)

Please input virtual address (base 16), q to quit: 748b
  --> pde index:0x1d pde contents:(valid 1, pfn 0x 0)
    --> pte index:0x 4 pte contents:(valid 0, pfn 0x7f)
      --> Fault (page table entry not valid)
```

