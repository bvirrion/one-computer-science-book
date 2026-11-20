// exo_last_word.c: another way to count the words of a text. Which word is lost?
#include <stdio.h>
#include <string.h>

static size_t count_words(const char *text, size_t len) {
    size_t n = 0;
    int in_word = 0;
    for (size_t i = 0; i < len; i++) {
        unsigned char c = (unsigned char)text[i];
        if ((c | 0x20) >= 'a' && (c | 0x20) <= 'z') {
            in_word = 1;
        } else if (in_word) {  // a separator ends the word in progress
            n++;
            in_word = 0;
        }
    }
    return n;
}

int main(void) {
    const char *texts[] = {"Red fish, blue fish.\n", "Red fish, blue fish\n",
                           "Red fish, blue fish"};
    for (int i = 0; i < 3; i++)
        printf("%-24.*s %zu words\n", (int)strcspn(texts[i], "\n"), texts[i],
               count_words(texts[i], strlen(texts[i])));
    return 0;
}
