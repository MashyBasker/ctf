# Challenge writeups

### Level 22

The `run` executable will be present in the `/challenge` dir

Create a python script in `/tmp` with

```py
import subprocess
subprocess.run(["/challenge/run"])
```

Run this with `python3 /tmp/script.py`. Boom! flag found.


### Level 23

Similar to 22. Trivial changes


### Level 24


Similar to 23. Just add the required password as parameter in the subprocess call


### Level 25

Look into how to set environment variables for subprocess. Do that and then run the executable through subprocess.


### Level 26

Look into how to pass files into subprocess.

> Hint: `stdin` parameter

### Level 27

Similar to 26. Just redirect to a file using `stdout` param


### Level 28

Pass an empty dictionary into the `env` parameter.


### Level 29

Write a C program that executes this binary using functions from the `exec` family. This needs to be done in the home directory

```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

void pwncollege() {}

int main() {
    pid_t pid = fork();

    if (pid == 0) {
        // child: stdin is already set to terminal input
        execl("/challenge/run", "/challenge/run", NULL);
        perror("exec failed");
        exit(1);
    } else if (pid > 0) {
        // parent: wait for child to finish
        int status;
        waitpid(pid, &status, 0);
    } else {
        perror("fork failed");
        exit(1);
    }

    return 0;
}
```

### Level 30

Pass the password to stdin like this `echo '<pass> | ./prog`

### Level 31

Provide the password as the first argument in execl call

### Level 32

Store the environment variable in a `char *env[] = {/* env var */}` variable

```c
execve("/challenge/run", NULL, env)
```


### Level 33

Simply redirect the file like this `./prog < /tmp/file`



### Level 36

The parent process must be bash and the process should be `cat`

```console
bash
/challenge/run | cat
```

### 37

```
bash
/challenge/run | grep "pwn"
```


### Level 58

`(echo 'passwd'; sleep 5) | /usr/bin/cat | python3.8 script.py`


### Level 66

`find /challenge -type f -executable -exec {} \;`



# Some general notes

If we run a program with:

```
import os
os.system("./chall")
```

This spawns a new shell process to run the program. If you see `/usr/bin/dash`, this is the likely issue. Instead do

```py
import subprocess
subprocess.run(["./chall"])
```

This keeps the parent process as python. Avoid the `shell=True` parameter in `subprocess.run()` to not spawn a new shell process


- Use `execve` or `execle` to get better control over the execution. 



```
```
