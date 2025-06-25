#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void pwncollege() {}

int main() {
    pid_t pid = fork();

    if (pid == 0) {
        int err = execl("/challenge/run", "");
        exit(err);
    } else if (pid < 0) {
        printf("[-] fork failed");
        exit(-1);
    }
}
