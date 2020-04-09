## Deadlock in VectorAdd
### main-common.c
```
Init vectors --> create parameters --> create threads to run --> thread join
```

### vector-deadlock.c

```c
void vector_add(vector_t *v_dst, vector_t *v_src) {
    Pthread_mutex_lock(&v_dst->lock); // lock dst
    Pthread_mutex_lock(&v_src->lock); // lock stc
    // do add operation
    int i;
    for (i = 0; i < VECTOR_SIZE; i++) {
	v_dst->values[i] = v_dst->values[i] + v_src->values[i];
    }
    Pthread_mutex_unlock(&v_dst->lock); // unlock dst
    Pthread_mutex_unlock(&v_src->lock); // unlock src
}
```

### How deadlock might occur

If one thread calls `vector_add(0, 1)` and the other one calls `vector_add(1, 0)`, and the following occurs:

```
|------------------------------------|--------------------------------|
|              Thread 1              |            Thread 2            |
|		mutex_lock(0);         context switch                         |
|							        ==>       mutex_lock(1);          |
|                                    |     mutex_lock(0); // blocked  |
|                                   <==
|   mutex_lock(1); // blocked        |                                |
(program hangs)
```

On my computer, executing `./vector-deadlock -n 2 -l 1 -v` only yields two results:

```
->add(0, 1)   // enter add
<-add(0, 1)   // leave add
              ->add(0, 1)
              <-add(0, 1)
```

or

```
              ->add(0, 1)
              <-add(0, 1)
->add(0, 1)
<-add(0, 1)
```

The first pattern is preferred (about 9 out of 10 cases). We can infer that in most cases, thread 0 (created earlier than thread 1) wins the race with thread 1, and there is no context switch between two threads at line `Pthread_mutex_lock(&v_dst->lock);` and `Pthread_mutex_lock(&v_src->lock);` After I tried to add `-d` option (which might induce dead lock) and ran it for 1000 times, still no deadlock occurred.

### Modifications to get deadlock working

First, let current thread yields CPU after acquire the first lock, otherwise the two mutex lock operations are too close and likely to fall within a same time slice, thus inducing no scheduling.

```c
Pthread_mutex_lock(&v_dst->lock);
pthread_yield();
Pthread_mutex_lock(&v_src->lock);
```

Second, pin the program to a single CPU core when executing via `taskset`

```bash
taskset 0x1 ./vector-deadlock -n 2 -l 1 -v -d
```

Finally, the output is

```
              ->add(1, 0)
->add(0, 1)
(program hangs)
```

Just work as expected.

