#! /usr/bin/env python

import sys
from optparse import OptionParser
import random

# process switch behavior
SCHED_SWITCH_ON_IO = 'SWITCH_ON_IO'

# io finished behavior
IO_RUN_LATER = 'IO_RUN_LATER'

# process states
STATE_RUNNING = 'RUNNING'
STATE_READY = 'READY'
STATE_DONE = 'DONE'
STATE_WAIT = 'WAITING'

# members of process structure
PROC_CODE = 'code_'
PROC_PC = 'pc_'
PROC_ID = 'pid_'
PROC_STATE = 'proc_state_'

# things a process can do
DO_COMPUTE = 'cpu'
DO_YIELD = 'yld'
DO_IO = 'io'


class scheduler:
    def __init__(self, process_switch_behavior, io_done_behavior, io_length):
        # keep set of instructions for each of the processes
        self.proc_info = {}
        self.process_switch_behavior = process_switch_behavior
        self.io_done_behavior = io_done_behavior
        self.io_length = io_length
        return

    def new_process(self):
        proc_id = len(self.proc_info)
        self.proc_info[proc_id] = {}
        self.proc_info[proc_id][PROC_PC] = 0
        self.proc_info[proc_id][PROC_ID] = proc_id
        self.proc_info[proc_id][PROC_CODE] = []
        self.proc_info[proc_id][PROC_STATE] = STATE_READY
        return proc_id

    def load(self, program_description):
        proc_id = self.new_process()
        tmp = program_description.split(':')
        if len(tmp) != 3:
            print('Bad description (%s): Must be number <x:y:z>' % program_description)
            print('  where X is the number of instructions')
            print('  and Y is the percent change that an instruction is YIELD')
            print('  and Z is the percent change that an instruction is IO')
            exit(1)

        num_instructions, chance_yield, chance_io = int(
            tmp[0]), float(tmp[1])/100.0, float(tmp[2])/100.0
        assert(chance_yield+chance_io < 1)

        #print "proc %d, num_instr %d, change_cpu %f" % (proc_id,num_instructions, chance_cpu)
        for i in range(num_instructions):
            randnum = random.random()
            if randnum < (1.0-chance_yield-chance_io):
                self.proc_info[proc_id][PROC_CODE].append(DO_COMPUTE)
            elif randnum >= (1.0-chance_yield-chance_io) and randnum < (1.0-chance_io):
                self.proc_info[proc_id][PROC_CODE].append(DO_YIELD)
            else:
                self.proc_info[proc_id][PROC_CODE].append(DO_IO)
            #print "proc %d, instr idx %d, instr cxt %s" % (proc_id, i, self.proc_info[proc_id][PROC_CODE][i])
        return

    #change to READY STATE, the current proc's state should be expected
    #if pid==-1, then pid=self.curr_proc
    def move_to_ready(self, expected, pid=-1):
        if pid == -1:
            pid = self.curr_proc
        assert self.proc_info[pid][PROC_STATE] == expected
        self.proc_info[pid][PROC_STATE] = STATE_READY
        return

    #change to RUNNING STATE, the current proc's state should be expected
    def move_to_running(self, expected):
        assert self.proc_info[self.curr_proc][PROC_STATE] == expected
        self.proc_info[self.curr_proc][PROC_STATE] = STATE_RUNNING
        return

    #change to DONE STATE, the current proc's state should be expected
    def move_to_done(self, expected):
        assert self.proc_info[self.curr_proc][PROC_STATE] == expected
        self.proc_info[self.curr_proc][PROC_STATE] = STATE_DONE
        return

    def move_to_wait(self, expected):
        self.proc_info[self.curr_proc][PROC_STATE] = STATE_WAIT
        assert self.proc_info[self.curr_proc][PROC_STATE] == expected
        return

    #choose next proc using FIFO/FCFS scheduling, If pid==-1, then pid=self.curr_proc
    def next_proc(self, pid=-1):
        if pid == -1:
            pid = self.curr_proc
        tot = self.get_num_processes()
        next_pid = pid
        while True:
            next_pid = (next_pid + 1) % tot
            if self.proc_info[next_pid][PROC_STATE] == STATE_READY:
                self.curr_proc = next_pid
                self.move_to_running(STATE_READY)
                return
            if next_pid == pid:
                break

    def get_num_processes(self):
        return len(self.proc_info)

    def get_num_instructions(self, pid):
        return len(self.proc_info[pid][PROC_CODE])

    def get_instruction(self, pid, index):
        return self.proc_info[pid][PROC_CODE][index]

    def get_num_active(self):
        num_active = 0
        for pid in range(len(self.proc_info)):
            if self.proc_info[pid][PROC_STATE] != STATE_DONE:
                num_active += 1
        return num_active

    def get_num_runnable(self):
        num_active = 0
        for pid in range(len(self.proc_info)):
            if self.proc_info[pid][PROC_STATE] == STATE_READY or \
                    self.proc_info[pid][PROC_STATE] == STATE_RUNNING:
                num_active += 1
        return num_active

    def get_ios_in_flight(self, current_time):
        num_in_flight = 0
        for pid in range(len(self.proc_info)):
            for t in self.io_finish_times[pid]:
                if t > current_time:
                    num_in_flight += 1
        return num_in_flight

    def space(self, num_columns):
        for i in range(num_columns):
            print('%10s' % ' ', end=' ')

    def check_if_done(self):
        if len(self.proc_info[self.curr_proc][PROC_CODE]) == 0:
            if self.proc_info[self.curr_proc][PROC_STATE] == STATE_RUNNING:
                self.move_to_done(STATE_RUNNING)
                self.next_proc()
        return

    def run(self):
        clock_tick = 0

        if len(self.proc_info) == 0:
            return

        # track outstanding IOs, per process
        self.io_finish_times = {}
        for pid in range(len(self.proc_info)):
            self.io_finish_times[pid] = []

        # make first one active
        self.curr_proc = 0
        self.move_to_running(STATE_READY)

        # OUTPUT: heade`[rs for each column
        print('%s' % 'Time', end=' ')
        for pid in range(len(self.proc_info)):
            print('%10s' % ('PID:%2d' % (pid)), end=' ')
        print('%10s' % 'CPU', end=' ')
        print('%10s' % 'IOs', end=' ')
        print('')

        # init statistics
        io_busy = 0
        cpu_busy = 0

        while self.get_num_active() > 0:
            clock_tick += 1

            # check for io finish
            io_done = False
            for pid in range(len(self.proc_info)):
                if clock_tick in self.io_finish_times[pid]:
                    # if IO finished, the should do something for related process
                    self.io_finish_times[pid].remove(clock_tick)
                    io_done = True
                    self.move_to_ready(STATE_WAIT, pid)

            if io_done and self.proc_info[self.curr_proc][PROC_STATE] != STATE_RUNNING:
            	self.next_proc()

            # if current proc is RUNNING and has an instruction, execute it
            instruction_to_execute = ''
            if self.proc_info[self.curr_proc][PROC_STATE] == STATE_RUNNING and \
                    len(self.proc_info[self.curr_proc][PROC_CODE]) > 0:
                #pop a instruction from proc_info[self.curr_proc][PROC_CODE]to instruction_to_execute
                instruction_to_execute = self.proc_info[self.curr_proc][PROC_CODE].pop(
                    0)
                cpu_busy += 1

            # OUTPUT: print what everyone is up to
            if io_done:
                print('%3d*' % clock_tick, end=' ')
            else:
                print('%3d ' % clock_tick, end=' ')
            for pid in range(len(self.proc_info)):
                if pid == self.curr_proc and instruction_to_execute != '':
                    print('%10s' % ('RUN:'+instruction_to_execute), end=' ')
                else:
                    print('%10s' % (self.proc_info[pid][PROC_STATE]), end=' ')
            if instruction_to_execute == '':
                print('%10s' % ' ', end=' ')
            else:
                print('%10s' % 1, end=' ')
            num_outstanding = self.get_ios_in_flight(clock_tick)
            if num_outstanding > 0:
                print('%10s' % str(num_outstanding), end=' ')
                io_busy += 1
            else:
                print('%10s' % ' ', end=' ')
            print('')

            # if this is an YIELD instruction, switch to ready state
            # and add an io completion in the future
            if instruction_to_execute == DO_YIELD:
                self.move_to_ready(STATE_RUNNING)
                self.next_proc()
            # if this is an IO instruction, switch to waiting state
            # and add an io completion in the future
            elif instruction_to_execute == DO_IO:
                self.move_to_wait(STATE_WAIT)
                self.io_finish_times[self.curr_proc].append(
                    clock_tick + self.io_length + 1)
                self.next_proc()

            # ENDCASE: check if currently running thing is out of instructions
            self.check_if_done()
        return (cpu_busy, io_busy, clock_tick)

#
# PARSE ARGUMENTS
#


parser = OptionParser()
parser.add_option('-s', '--seed', default=0, help='the random seed',
                  action='store', type='int', dest='seed')
parser.add_option('-l', '--processlist', default='',
                  help='a comma-separated list of processes to run, in the form X1:Y1:Z1,X2:Y2:Z2,... where X is the number of instructions that process should run, and Y/Z the chances (from 0 to 100) issue an YIELD/IO',
                  action='store', type='string', dest='process_list')
parser.add_option('-L', '--iolength', default=3, help='how long an IO takes',
                  action='store', type='int', dest='io_length')
parser.add_option('-p', '--printstats', help='print statistics at end; only useful with -c flag (otherwise stats are not printed)',
                  action='store_true', default=False, dest='print_stats')
(options, args) = parser.parse_args()

random.seed(options.seed)

process_switch_behavior = SCHED_SWITCH_ON_IO
io_done_behavior = IO_RUN_LATER
io_length = options.io_length


s = scheduler(process_switch_behavior, io_done_behavior, io_length)

# example process description (10:100,10:100)
for p in options.process_list.split(','):
    s.load(p)

print('Produce a trace of what would happen when you run these processes:')
for pid in range(s.get_num_processes()):
    print('Process %d' % pid)
    for inst in range(s.get_num_instructions(pid)):
        print('  %s' % s.get_instruction(pid, inst))
    print('')
print('Important behaviors:')
print('  System will switch when', end=' ')
if process_switch_behavior == SCHED_SWITCH_ON_IO:
    print('the current process is FINISHED or ISSUES AN YIELD or IO')
else:
    print('error in sched switch on iobehavior')
    exit(-1)
print('  After IOs, the process issuing the IO will', end=' ')
if io_done_behavior == IO_RUN_LATER:
    print('run LATER (when it is its turn)')
else:
    print('error in IO done behavior')
    exit(-1)
print('')

(cpu_busy, io_busy, clock_tick) = s.run()

print('')
print('Stats: Total Time %d' % clock_tick)
print('Stats: CPU Busy %d (%.2f%%)' %
      (cpu_busy, 100.0 * float(cpu_busy)/clock_tick))
print('Stats: IO Busy  %d (%.2f%%)' %
      (io_busy, 100.0 * float(io_busy)/clock_tick))
print('')
