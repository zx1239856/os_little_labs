# Buddy System Memory Allocator
## Note:
Please refer to Tsinghua Git: https://git.tsinghua.edu.cn/xiang-zh17/os-little-labs/tree/35a188a9/hw3

## Usage:
```bash
python3 ostep3-malloc.py -S 100 -b 1000 -a 4 -p BUDDY -c -A +12,+60,+8,+3,+1,-4,-3,+7,-0,-1,+9,+20,+50,-2,-5,-6,-7,-8
```
Use `-p BUDDY` to select buddy system policy for test.

Example output:

```
Total size for buddy: 128  // the size will be round up to power of 2
ptr[0] = Alloc(12) returned 1000 (searched 0 elements)
Alloc List [ Size 1 ]: [ addr:1000 sz:16 ]   
// alloc 12(16), split 64,32,16 out of 128

ptr[1] = Alloc(60) returned 1064 (searched 0 elements)
Alloc List [ Size 2 ]: [ addr:1000 sz:16 ][ addr:1064 sz:64 ] 
// alloc 60(64), use existing child node (split during malloc ptr[0])

ptr[2] = Alloc(8) returned 1016 (searched 0 elements)
Alloc List [ Size 3 ]: [ addr:1000 sz:16 ][ addr:1064 sz:64 ][ addr:1016 sz:8 ] 
// alloc 8, split 8 out of 16 (the neighbor of ptr[0])

ptr[3] = Alloc(3) returned 1024 (searched 0 elements)
Alloc List [ Size 4 ]: [ addr:1000 sz:16 ][ addr:1064 sz:64 ][ addr:1016 sz:8 ][ addr:1024 sz:4 ]
// alloc 3(4), split 4 out of 8 (the neighbor of ptr[2])

ptr[4] = Alloc(1) returned 1028 (searched 0 elements)
Alloc List [ Size 5 ]: [ addr:1000 sz:16 ][ addr:1064 sz:64 ][ addr:1016 sz:8 ][ addr:1024 sz:4 ][ addr:1028 sz:4 ]
// alloc 1(4), use existing child node (split during malloc ptr[3]) 

Free(ptr[4]) returned 0
Alloc List [ Size 4 ]: [ addr:1000 sz:16 ][ addr:1064 sz:64 ][ addr:1016 sz:8 ][ addr:1024 sz:4 ]
// free, no merging

Free(ptr[3]) returned 0
Alloc List [ Size 3 ]: [ addr:1000 sz:16 ][ addr:1064 sz:64 ][ addr:1016 sz:8 ]
// free, merge nodes for ptr[3] and ptr[4] to become a 8-byte node

ptr[5] = Alloc(7) returned 1024 (searched 0 elements)
Alloc List [ Size 4 ]: [ addr:1000 sz:16 ][ addr:1064 sz:64 ][ addr:1016 sz:8 ][ addr:1024 sz:8 ]
// alloc 7(8), use existing node created during Free(ptr[3])

Free(ptr[0]) returned 0
Alloc List [ Size 3 ]: [ addr:1064 sz:64 ][ addr:1016 sz:8 ][ addr:1024 sz:8 ]
// free, no merging because the neighbor 16-byte node is occupied by [ addr:1016 sz:8 ]

Free(ptr[1]) returned 0
Alloc List [ Size 2 ]: [ addr:1016 sz:8 ][ addr:1024 sz:8 ]
// free, no merging because the neighbor 64-byte node is occupied

ptr[6] = Alloc(9) returned 1000 (searched 0 elements)
Alloc List [ Size 3 ]: [ addr:1016 sz:8 ][ addr:1024 sz:8 ][ addr:1000 sz:16 ]
// alloc 9(16), using existing node from Free(ptr[0])

ptr[7] = Alloc(20) returned 1032 (searched 0 elements)
Alloc List [ Size 4 ]: [ addr:1016 sz:8 ][ addr:1024 sz:8 ][ addr:1000 sz:16 ][ addr:1032 sz:32 ]
// alloc 20(32), using existing node

ptr[8] = Alloc(50) returned 1064 (searched 0 elements)
Alloc List [ Size 5 ]: [ addr:1016 sz:8 ][ addr:1024 sz:8 ][ addr:1000 sz:16 ][ addr:1032 sz:32 ][ addr:1064 sz:64 ]
// alloc 50(64), using existing node

...

Free(ptr[8]) returned 0
Alloc List [ Size 0 ]:
```



## Dependencies
```bash
pip install bitmap
```
