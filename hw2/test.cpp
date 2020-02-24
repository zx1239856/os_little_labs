#include <signal.h>
#include <ucontext.h>
#include <stdio.h>
#include <stdlib.h>

void sig_handler(int sig, siginfo_t *si, void *arg) {
	if(sig != SIGFPE || si->si_code != FPE_INTDIV) {
		printf("This handler can only be used with SIGFPE caused by division by zero\n");
		exit(0);
	}
	ucontext_t *ctx = (ucontext_t *)arg;
	printf("\033[0;31m[Exception]\033[0m Division by zero detected, original dividend: %lld, will ignore this operation.\n", ctx->uc_mcontext.gregs[REG_RAX]);
	ctx->uc_mcontext.gregs[REG_RIP] += 2;
	// unsafe, move %rip to skip the offending instruction `div/idiv %reg`
}

int main() {
	struct sigaction sa;
	sa.sa_sigaction = sig_handler;
	sigemptyset(&sa.sa_mask);
	sa.sa_flags = SA_SIGINFO;
	sigaction(SIGFPE, &sa, nullptr);
	// about to generate SIGFPE if a == 0
	int a, b;
	printf("Input a and b, calc a/b in integer:\n");
	scanf("%d %d", &a, &b);
	printf("The result is %d\n", a / b);
	return 0;
}
