mem = []
disk = []
with open('mem.txt', 'r') as fp:
    for line in fp.readlines():
        mem.extend(line.strip().split(' ')[2:])
    print("Read {} bytes from mem".format(len(mem)))

with open('disk.txt', 'r') as fp:
    for line in fp.readlines():
        disk.extend(line.strip().split(' ')[2:])
    print("Read {} bytes from disk".format(len(disk)))

pdbr = 0xd80
while True:
    vaddr = input('\nPlease input virtual address (base 16), q to quit: ')
    if vaddr == 'q':
        exit()
    try:
        vaddr = int(vaddr, base=16)
        if vaddr >= 0x2000 or vaddr < 0:
            print("Virtual address out of range")
            continue
        pde_idx = (vaddr >> 10) & 0x1f
        pde = int(mem[pdbr + pde_idx], base=16)
        valid = pde >> 7
        pfn = pde & 0x7f
        print("  --> pde index:0x{:x} pde contents:(valid {}, pfn 0x{:x})".format(pde_idx, valid, pfn))
        if valid:
            pte_base = pfn << 5
            pte_idx = (vaddr >> 5) & 0x1f
            pte = int(mem[pte_base + pte_idx], base=16)
            valid = pte >> 7
            pfn = pte & 0x7f
            print("    --> pte index:0x{:x} pte contents:(valid {}, pfn 0x{:x})".format(pte_idx, valid, pfn))
            if valid:
                paddr = (pfn << 5) + (vaddr & 0x1f)
                print("      --> Translates to Physical Address 0x{:3x} --> Value: 0x{:02x}".format(paddr, int(mem[paddr], base=16)))
            elif pfn == 0x7f:
                print("      --> Fault (page table entry not valid)")
            else:
                paddr = (pfn << 5) + (vaddr & 0x1f)
                print("      --> Translates to Disk Sector Address 0x{:3x} --> Value: 0x{:02x}".format(paddr, int(disk[paddr], base=16)))
        else:
            print("    --> Fault (page directory entry not valid)")
    except:
        print("Invalid memory access!")
