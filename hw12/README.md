# VSFS Analysis

### Example Output

```
python3 vsfs.py -n 10 -s 16                                          ✔  2362  14:43:28 
ARG seed 16
ARG numInodes 8
ARG numData 8
ARG numRequests 10
ARG reverse False
ARG printFinal False

Initial state

inode bitmap  10000000
inodes        [d a:0 r:2] [] [] [] [] [] [] [] 
data bitmap   10000000
data          [(.,0) (..,0)] [] [] [] [] [] [] [] 

Which operation took place?  // createFile("/y")

inode bitmap  11000000
inodes        [d a:0 r:2] [f a:-1 r:1] [] [] [] [] [] [] 
data bitmap   10000000
data          [(.,0) (..,0) (y,1)] [] [] [] [] [] [] [] 

Which operation took place?  // write("/y")

inode bitmap  11000000
inodes        [d a:0 r:2] [f a:1 r:1] [] [] [] [] [] [] 
data bitmap   11000000
data          [(.,0) (..,0) (y,1)] [u] [] [] [] [] [] [] 

Which operation took place?  // link("/y", "/m")

inode bitmap  11000000
inodes        [d a:0 r:2] [f a:1 r:2] [] [] [] [] [] [] 
data bitmap   11000000
data          [(.,0) (..,0) (y,1) (m,1)] [u] [] [] [] [] [] [] 

Which operation took place?  // unlink("/m")

inode bitmap  11000000
inodes        [d a:0 r:2] [f a:1 r:1] [] [] [] [] [] [] 
data bitmap   11000000
data          [(.,0) (..,0) (y,1)] [u] [] [] [] [] [] [] 

Which operation took place?  // createFile("/z")

inode bitmap  11100000
inodes        [d a:0 r:2] [f a:1 r:1] [f a:-1 r:1] [] [] [] [] [] 
data bitmap   11000000
data          [(.,0) (..,0) (y,1) (z,2)] [u] [] [] [] [] [] [] 

Which operation took place? // mkdir("/f")

inode bitmap  11110000
inodes        [d a:0 r:3] [f a:1 r:1] [f a:-1 r:1] [d a:2 r:2] [] [] [] [] 
data bitmap   11100000
data          [(.,0) (..,0) (y,1) (z,2) (f,3)] [u] [(.,3) (..,0)] [] [] [] [] [] 
```

This is a very basic file system demo which only supports some fundamental operations. One can only create a file and write to it once, and cannot append to it the second time. When each writing occurs, an entire block gets written, leaving no internal fragments. In terms of allocating inodes or data blocks, referring to the following lines:

```python
def alloc(self):
    for num in range(len(self.bmap)):
        if self.bmap[num] == 0:
            self.bmap[num] = 1
            self.numAllocated += 1
            return num
    return -1

def inodeAlloc(self):
    return self.ibitmap.alloc()

def dataAlloc(self):
    return self.dbitmap.alloc()
```

It is obvious that the allocation algorithm is First-Fit, that is, find the first block that is available and use it.