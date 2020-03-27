# POC(Proof of Concept) O(1) Scheduler

+ Adapted from OSTEP RR scheduler
+ Implemented `bitarray`, support O(1) operations. Each priority level is associated with a queue.
+ When `ACTIVE bitarray` is empty, swap it with the `EXPIRED bitarray`.
+ NO care about priority when handling time slices, because we would need the simulator to support `wait` or `yield` operations to calculate nicer value of each process, which is a heuristic for priority calculation. Now the priority is randomly selected between 0 ~ 29.
