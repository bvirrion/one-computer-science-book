/* ucontext_switch.c -- the same ping-pong with the C library's contexts: swapcontext saves
   the current registers into one ucontext_t and loads another's. */
#include <stdio.h>
#include <ucontext.h>

static ucontext_t main_ctx, a_ctx, b_ctx;
static char a_stack[16384], b_stack[16384];

static void task_a(void)
{
    for (int i = 1; i <= 3; i++) {
        printf("A%d\n", i);
        swapcontext(&a_ctx, &b_ctx);  /* save A, resume B */
    }
}  /* returning resumes uc_link: main */

static void task_b(void)
{
    for (int i = 10;; i += 10) {
        printf("B%d\n", i);
        swapcontext(&b_ctx, &a_ctx);
    }
}

static void prepare(ucontext_t *c, char *stack, size_t size, void (*f)(void))
{
    getcontext(c);
    c->uc_stack.ss_sp = stack;
    c->uc_stack.ss_size = size;
    c->uc_link = &main_ctx;  /* where to go when f returns */
    makecontext(c, f, 0);
}

int main(void)
{
    prepare(&a_ctx, a_stack, sizeof a_stack, task_a);
    prepare(&b_ctx, b_stack, sizeof b_stack, task_b);
    swapcontext(&main_ctx, &a_ctx);
    printf("back in main\n");
    return 0;
}
