#include <execinfo.h>
#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <ucontext.h>

void sig_handler(int sig, siginfo_t *si, void *arg) {
	constexpr int MAX_SIZE = 50;
	ucontext_t *ctx = (ucontext_t *)arg;
	void *trace[MAX_SIZE];
	if(sig == SIGSEGV) {
		printf("Sigfault occured at %p, from %p\n", (void*)ctx->uc_mcontext.gregs[REG_CR2], (void*)ctx->uc_mcontext.gregs[REG_RIP]);
	} else {
		printf("Caught signal %d\n", sig);
	}
	int size = backtrace(trace, MAX_SIZE);
	char **names = backtrace_symbols(trace, size);
	printf("Call stack: \n");
	for(int i = 1 ; i < size; ++i)
		printf("%d %s\n", size - i, names[i]);
	free(names);
	exit(0);
}

void faulty_func() {
	*((char *)0xdeadbeef) = 'a'; // crash
}

void recursion(int a) {
	if(a <= 0) {
		faulty_func();
	} else {
		return recursion(a - 1);
	}
}

int main() {
	struct sigaction sa;
	sa.sa_sigaction = sig_handler;
	sigemptyset(&sa.sa_mask);
	sa.sa_flags = SA_RESTART;
	sigaction(SIGSEGV, &sa, nullptr);
	sigaction(SIGABRT, &sa, nullptr);

	recursion(5);
}
