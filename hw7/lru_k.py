import random
import argparse

class Page:
    def __init__(self, k):
        self.hist = [0] * k
        self.last = 0
        self.crp = 0

class LRU_K:
    def __init__(self, num_pages, k, CRP):
        self.buffer = [0] * num_pages
        self.k = k
        self.time = 0
        self.hits = 0
        self.ops = 0
        self.page_info = {}

        self.CRP = CRP

    def request(self, p):
        self.time += 1
        self.ops += 1

        if p not in self.page_info:
            self.page_info[p] = Page(self.k)

        page = self.page_info[p]
        
        if p in self.buffer:
            self.hits += 1
            if self.time - page.last > self.CRP:
                ## close correlated period and start new
                corr_period = page.last - page.hist[0]
                for j in range(1, self.k):
                    page.hist[j] = page.hist[j-1] + corr_period
                page.hist[0] = self.time
            
            page.last = self.time
        else:
            if 0 in self.buffer:
                self.buffer[self.buffer.index(0)] = p
            else:
                ## find a victim to replace
                victim = -1
                min_t = self.time
                for q in range(len(self.buffer)):
                    page_q = self.buffer[q]
                    if self.time - self.page_info[page_q].last > self.CRP and self.page_info[page_q].hist[self.k-1] < min_t:
                        victim = q
                        min_t = self.page_info[page_q].hist[self.k-1]

                self.buffer[victim] = p
            if page.hist[0] != 0:
                for i in range(1, self.k):
                    page.hist[i] = page.hist[i-1]
            page.hist[0] = self.time
            page.last = self.time

    def hitRatio(self):
        return 1. * self.hits / self.ops

if __name__ == "__main__":
    parser = argparse.ArgumentParser("LRU-K Simulator")
    parser.add_argument("-k", help="Specifies k param of LRU-K", type=int, default=2)
    parser.add_argument("-c", "--crp", help="Correlated reference period", type=int, default=0)
    parser.add_argument("-s", "--seq", help="Page reference seq, split with comma", type=str)
    parser.add_argument("-n", "--num", help="Number of random requests", type=int, default=100)
    parser.add_argument("-b", "--buffer", help="Buffer size", type=int, default=30)

    args = parser.parse_args()

    print("Buffer size: {}".format(args.buffer))

    if args.k < 1 or args.crp < 0 or args.buffer <= 0 or args.num <= 0:
        print("Invalid arguments")
    else:
        seq = []
        random.seed(10)
        if args.seq:
            seq = [int(i) for i in args.seq.strip().split(',')]
        else:
            for i in range(args.num):
                k = random.randint(1, 100)
                if k < 90:
                    seq.append(random.randint(1, 100))
                else:
                    seq.append(random.randint(101, 1000))
            
        buf = LRU_K(args.buffer, args.k, args.crp)
        for p in seq:
            buf.request(p)

        print("LRU-{}".format(args.k))
        print("#Hits: {}, #Ops: {}, HitRate: {:.4f}".format(buf.hits, buf.ops, buf.hitRatio()))