# LRU-K
## About CRP (Correlated Reference Period)
Coalesce references within a small period, and impose no penalty or credit for them. (See reference slide for more details).

### Usage

Type the following command to view help:

``` bash
python3 lru_k.py -h
```

## Test cases
(Buffer size = 5)

+ k=1, seq: 1,2,3,4,5,1,2,3,4,5 --> Hit rate: 50%
+ k=1, seq: 1,2,3,4,5,6,1,2,3,4,5 --> Hit rate: 0%
+ k=2, seq: 1,2,3,4,5,6,1,2,3,4,5 --> Hit rate: 36.7%
+ Or you can try random cases

## References
[LRU-K and 2Q](http://www.cs.cmu.edu/~christos/courses/721.S03/LECTURES-PDF/0241-LRUK.PDF)