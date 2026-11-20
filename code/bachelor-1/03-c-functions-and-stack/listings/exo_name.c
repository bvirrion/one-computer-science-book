// exo_name.c: a function that builds a greeting in a local array.
#include <stdio.h>

char *greeting(const char *name)
{
    char text[32];
    snprintf(text, sizeof text, "Hello, %s!", name);
    return text;
}

int main(void)
{
    char *g = greeting("Ada");
    printf("greeting: %s\n", g);
    return 0;
}
