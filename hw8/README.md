# Process Scheduler
```bash
>> python3 proc.py -l 5:30:30,5:40:40,10:10:0 -s 3

Produce a trace of what would happen when you run these processes:
Process 0
  cpu
  yld
  cpu
  yld
  yld

Process 1
  cpu
  cpu
  io
  yld
  yld

Process 2
  yld
  cpu
  cpu
  cpu
  cpu
  cpu
  cpu
  cpu
  cpu
  cpu

Important behaviors:
  System will switch when the current process is FINISHED or ISSUES AN YIELD or IO
  After IOs, the process issuing the IO will run LATER (when it is its turn)

Time     PID: 0     PID: 1     PID: 2        CPU        IOs 
  1     RUN:cpu      READY      READY          1            
  2     RUN:yld      READY      READY          1            
  3       READY    RUN:cpu      READY          1            
  4       READY    RUN:cpu      READY          1            
  5       READY     RUN:io      READY          1            
  6       READY    WAITING    RUN:yld          1          1 
  7     RUN:cpu    WAITING      READY          1          1 
  8     RUN:yld    WAITING      READY          1          1 
  9*      READY      READY    RUN:cpu          1            
 10       READY      READY    RUN:cpu          1            
 11       READY      READY    RUN:cpu          1            
 12       READY      READY    RUN:cpu          1            
 13       READY      READY    RUN:cpu          1            
 14       READY      READY    RUN:cpu          1            
 15       READY      READY    RUN:cpu          1            
 16       READY      READY    RUN:cpu          1            
 17       READY      READY    RUN:cpu          1            
 18     RUN:yld      READY       DONE          1            
 19       READY    RUN:yld       DONE          1            
 20        DONE    RUN:yld       DONE          1            

Stats: Total Time 20
Stats: CPU Busy 20 (100.00%)
Stats: IO Busy  3 (15.00%)
```
