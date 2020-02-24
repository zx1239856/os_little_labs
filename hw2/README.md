# Division by Zero Handler in Linux

In a Linux OS running on x86 CPU, division by zero will cause a trap which is then handled by the exception handler in Linux kernel.

The location of the exception handler resides in the IDT (Interrupt Descriptor Table), and here is an extraction from Linux kernel code:
```C++
// linux/arch/x86/include/asm/traps.h

/* Interrupts/Exceptions */
enum {
	X86_TRAP_DE = 0,	/*  0, Divide-by-zero */
	X86_TRAP_DB,		/*  1, Debug */
	X86_TRAP_NMI,		/*  2, Non-maskable Interrupt */
	X86_TRAP_BP,		/*  3, Breakpoint */
	X86_TRAP_OF,		/*  4, Overflow */
    ...
}

// linux/arch/x86/kernel/idt.c
static const __initconst struct idt_data def_idts[] = {
	INTG(X86_TRAP_DE,		divide_error),
	INTG(X86_TRAP_NMI,		nmi),
	INTG(X86_TRAP_BR,		bounds),
	INTG(X86_TRAP_UD,		invalid_op),
	INTG(X86_TRAP_NM,		device_not_available),
    ...
}
```

```asm
// linux/arch/x86/entry/entry_32.S
SYM_CODE_START(divide_error)
	ASM_CLAC
	pushl	$0				# no error code
	pushl	$do_divide_error
	jmp	common_exception
SYM_CODE_END(divide_error)

SYM_CODE_START_LOCAL_NOALIGN(common_exception)
	/* the function address is in %gs's slot on the stack */
	SAVE_ALL switch_stacks=1 skip_gs=1 unwind_espfix=1
	ENCODE_FRAME_POINTER

	/* fixup %gs */
	GS_TO_REG %ecx
	movl	PT_GS(%esp), %edi		# get the function address
	REG_TO_PTGS %ecx
	SET_KERNEL_GS %ecx

	/* fixup orig %eax */
	movl	PT_ORIG_EAX(%esp), %edx		# get the error code
	movl	$-1, PT_ORIG_EAX(%esp)		# no syscall to restart

	TRACE_IRQS_OFF
	movl	%esp, %eax			# pt_regs pointer
	CALL_NOSPEC %edi
	jmp	ret_from_exception
SYM_CODE_END(common_exception)
```

```C++
// linux/arch/sh/kernel/traps_32.c
asmlinkage void do_divide_error(unsigned long r4)
{
	int code;

	switch (r4) {
	case TRAP_DIVZERO_ERROR:
		code = FPE_INTDIV;
		break;
	case TRAP_DIVOVF_ERROR:
		code = FPE_INTOVF;
		break;
	default:
		/* Let gcc know unhandled cases don't make it past here */
		return;
	}
	force_sig_fault(SIGFPE, code, NULL);
}
```

We can see that the exception handler will emit `SIGFPE`, and thus we can handle division by zero through a signal handler running in user mode, without having to modify the kernel code.