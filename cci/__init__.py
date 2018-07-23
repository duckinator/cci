#!/usr/bin/env python3

import inspect
import shlex
from subprocess import Popen, PIPE
import sys

def skip_shebang(f):
    line = f.readline()
    if line.startswith("#!"):
        f.seek(len(line))
    else:
        f.seek(0)

def pipe(cmds, stdin, stdout):
    procs = []
    limit = len(cmds) - 1

    for (idx, cmd) in enumerate(cmds):
        cur_stdin  = stdin  if idx == 0     else procs[idx - 1].stdout
        cur_stdout = stdout if idx == limit else PIPE
        procs.append(Popen(cmd, stdin=cur_stdin, stdout=cur_stdout))

    return procs[-1].communicate()

def main(argv=None):
    """
    cci isn't built for being called from the commandline.
    It's designed for being put in the shebang line of C files.

    For example, save the following to "hello-world.c":

        #!cci -std=c11 -Wall -pedantic-errors
        #include <stdio.h>
        int main() {
            printf("Hello, world!")
            return 0;
        }

    Now, mark it as executable (on *nix, `chmod +x hello-world.c`),
    then run `./hello-world.c`.

    It should run without issue, _without creating any new files_.

    DEBUGGING
        If you include the argument "-###" in the arguments, it will be
        passed through to Clang for debugging purposes.
    """
    if argv is None:
        argv = sys.argv[1:]

    if any(map(lambda x: "-h" in x, argv)) or len(argv) != 2:
            print(inspect.getdoc(main))
            exit(1)

    args = shlex.split(argv[0])
    filename = argv[1]

    f = open(filename)
    skip_shebang(f)

    clang = ["clang", "-xc", *args, "-", "-S", "-emit-llvm", "-o", "-"]
    lli   = ["lli", "-"]

    commands = [clang]
    if not "-###" in args:
        commands.append(lli)

    with f:
        pipe(commands, stdin=f, stdout=sys.stdout)

if __name__ == "__main__":
    main()
