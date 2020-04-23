# Disk Scheduling: C-SCAN and C-LOOK

### FIFO

```
python3 disksim.py -a 0
Block:   0  Seek:  0  Rotate:165  Transfer: 30  Total: 195

python3 disksim.py -a 6
Block:   6  Seek:  0  Rotate:345  Transfer: 30  Total: 375

python3 disksim.py -a 30
Block:  30  Seek: 80  Rotate:265  Transfer: 30  Total: 375

python3 disksim.py -a 7,30,8
Block:   7  Seek:  0  Rotate: 15  Transfer: 30  Total:  45
Block:  30  Seek: 80  Rotate:220  Transfer: 30  Total: 330
Block:   8  Seek: 80  Rotate:310  Transfer: 30  Total: 420

TOTALS      Seek:160  Rotate:545  Transfer: 90  Total: 795

python3 disksim.py -a 10,11,12,13,24,1
Block:  10  Seek:  0  Rotate:105  Transfer: 30  Total: 135
Block:  11  Seek:  0  Rotate:  0  Transfer: 30  Total:  30
Block:  12  Seek: 40  Rotate:320  Transfer: 30  Total: 390
Block:  13  Seek:  0  Rotate:  0  Transfer: 30  Total:  30
Block:  24  Seek: 40  Rotate:260  Transfer: 30  Total: 330
Block:   1  Seek: 80  Rotate:280  Transfer: 30  Total: 390

TOTALS      Seek:160  Rotate:965  Transfer:180  Total:1305
```

### SSTF

```
python3 disksim.py -a 10,11,12,13,24,1
```

```
Block:  10  Seek:  0  Rotate:105  Transfer: 30  Total: 135
Block:  11  Seek:  0  Rotate:  0  Transfer: 30  Total:  30
Block:   1  Seek:  0  Rotate: 30  Transfer: 30  Total:  60
Block:  12  Seek: 40  Rotate:260  Transfer: 30  Total: 330
Block:  13  Seek:  0  Rotate:  0  Transfer: 30  Total:  30
Block:  24  Seek: 40  Rotate:260  Transfer: 30  Total: 330

TOTALS      Seek: 80  Rotate:655  Transfer:180  Total: 915
```

`C-SCAN` and `C-LOOK` yield the same output in the case of this sequence.

### C-SCAN

```
python3 disksimv3.py -a 10,11,12,13,24,25,27,28,30,12 -c -p CSCAN -w 5
```

```
Block:  10  Seek:  0  Rotate:105  Transfer: 30  Total: 135
Block:  11  Seek:  0  Rotate:  0  Transfer: 30  Total:  30
Block:  12  Seek: 40  Rotate:320  Transfer: 30  Total: 390
Block:  13  Seek:  0  Rotate:  0  Transfer: 30  Total:  30
Block:  24  Seek: 40  Rotate:260  Transfer: 30  Total: 330
Block:  25  Seek:  0  Rotate:  0  Transfer: 30  Total:  30
Block:  27  Seek:  0  Rotate: 30  Transfer: 30  Total:  60
Block:  28  Seek:  0  Rotate:  0  Transfer: 30  Total:  30
Block:  30  Seek:  0  Rotate: 30  Transfer: 30  Total:  60
Block:  12  Seek: 80  Rotate:110  Transfer: 30  Total: 220

TOTALS      Seek:160  Rotate:855  Transfer:300  Total:1315
```

### C-LOOK

```
python3 disksimv3.py -a 10,11,12,13,24,25,27,28,30,12 -c -p CSCAN -w 5
```

```
Block:  10  Seek:  0  Rotate:105  Transfer: 30  Total: 135
Block:  11  Seek:  0  Rotate:  0  Transfer: 30  Total:  30
Block:  12  Seek: 40  Rotate:320  Transfer: 30  Total: 390
Block:  13  Seek:  0  Rotate:  0  Transfer: 30  Total:  30
Block:  24  Seek: 40  Rotate:260  Transfer: 30  Total: 330
Block:  25  Seek:  0  Rotate:  0  Transfer: 30  Total:  30
Block:  27  Seek:  0  Rotate: 30  Transfer: 30  Total:  60
Block:  28  Seek:  0  Rotate:  0  Transfer: 30  Total:  30
Block:  30  Seek:  0  Rotate: 30  Transfer: 30  Total:  60
Block:  12  Seek: 40  Rotate:110  Transfer: 30  Total: 180

TOTALS      Seek:120  Rotate:855  Transfer:300  Total:1275
```

Compared with `C-SCAN`, this algorithm spends 40 fewer units of time on seeking.