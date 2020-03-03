with open('mem.txt', 'r') as fp:
    mem = []
    for line in fp.readlines():
        mem.extend(line.strip().split(' ')[2:])
    print("Read {} bytes into mem".format(len(mem)))
    pdbr = 0x220
    while True:
        vaddr = input('\nPlease input virtual address (base 16), q to quit: ')
        if vaddr == 'q':
            exit()
        try:
            vaddr = int(vaddr, base=16)
            pde_idx = (vaddr >> 10) & 0x1f
            pde = int(mem[pdbr + pde_idx], base=16)
            valid = pde >> 7
            pfn = pde & 0x7f
            print("  --> pde index:0x{:2x} pde contents:(valid {}, pfn 0x{:2x})".format(pde_idx, valid, pfn))
            if valid:
                pte_base = pfn << 5
                pte_idx = (vaddr >> 5) & 0x1f
                pte = int(mem[pte_base + pte_idx], base=16)
                valid = pte >> 7
                pfn = pte & 0x7f
                print("    --> pte index:0x{:2x} pte contents:(valid {}, pfn 0x{:2x})".format(pte_idx, valid, pfn))
                if valid:
                    paddr = (pfn << 5) + (vaddr & 0x1f)
                    print("      --> Translates to Physical Address 0x{:4x} --> Value: 0x{:2x}".format(paddr, int(mem[paddr], base=16)))
                else:
                    print("      --> Fault (page table entry not valid)")
            else:
                print("    --> Fault (page directory entry not valid)")
        except:
            print("Invalid memory access!")