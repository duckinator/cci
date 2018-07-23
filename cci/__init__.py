#!/usr/bin/env python3

import inspect
import shlex
from subprocess import Popen, PIPE
import sys

def get_headers(f):
    shebang = f.readline()
    args_str = f.readline()
    if args_str.startswith("# cci:"):
        args = args_str.split("# cci:")[1]
        f.seek(len(shebang) + len(args_str))
    else:
        args = ""
        f.seek(len(shebang))
    return (shebang, args)

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
    cci is designed for being put in the shebang line of C files.
    Due to limitations in how shebang lines work, arguments to
    Clang are on the line immediately after the shebang line, and
    that line must start with "# cci:".

    For example, save the following to "hello-world.c":

        #!/usr/bin/env cci
        # cci: -std=c11 -Wall -pedantic-errors
        #include <stdio.h>
        int main() {
            printf("Hello, world!\n")
            return 0;
        }

    Now, mark it as executable (on *nix, `chmod +x hello-world.c`),
    then run `./hello-world.c`.

    DEBUGGING
        If you include the argument "-###" in the arguments, it will be
        passed through to Clang for debugging purposes.
    """
    if argv is None:
        argv = sys.argv[1:]

    if any(map(lambda x: x == "-h" or x == "--help", argv)) or len(argv) != 1:
        # Print help text.
        print(inspect.getdoc(main))
        exit(1)
    else:
        # We got a file name only.
        f = open(argv[0])
        _, header_argv = get_headers(f)

    args = shlex.split(header_argv)

    clang = ["clang", "-xc", *args, "-", "-S", "-emit-llvm", "-o", "-"]
    lli   = ["lli", "-"]

    commands = [clang]
    if not "-###" in args:
        commands.append(lli)

    with f:
        pipe(commands, stdin=f, stdout=sys.stdout)

if __name__ == "__main__":
    main()
