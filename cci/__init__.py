#!/usr/bin/env python3

import inspect
import shlex
from subprocess import Popen, PIPE
import sys

def get_flags(filename):
    with open(filename, "r") as f:
        f.readline() # Skip shebang line.
        args_str = f.readline()

    if args_str.startswith("// cci:"):
        return args_str[7:]
    return ""

def pipe(cmds, stdin, stdout):
    """Given a series of commands, create and run a shell-style pipeline."""
    procs = []
    limit = len(cmds) - 1

    for (idx, cmd) in enumerate(cmds):
        cur_stdin  = stdin  if idx == 0     else procs[idx - 1].stdout
        cur_stdout = stdout if idx == limit else PIPE
        procs.append(Popen(cmd, stdin=cur_stdin, stdout=cur_stdout))

    return procs[-1].wait()

def main(argv=None):
    """
    cci is designed for being put in the shebang line of C files.
    Due to limitations in how shebang lines work, arguments to
    Clang are on the line immediately after the shebang line, and
    that line must start with "// cci:".

    For example, save the following to "hello-world.c":

        #!/usr/bin/env cci
        // cci: -std=c11 -Wall -pedantic-errors
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

    if len(argv) == 0 or argv[0] == "-h" or argv[0] == "--help":
        # Print help text.
        print(inspect.getdoc(main))
        sys.exit(1)

    filename, *program_args = argv
    clang_args = shlex.split(get_flags(filename))

    clang = ["clang", "-xc", *clang_args, "-", "-S", "-emit-llvm", "-o", "-"]
    lli = ["lli", "-", *program_args]

    commands = [clang]
    if "-###" not in clang_args:
        # If -### is passed to clang, it doesn't generate LLVM output.
        commands.append(lli)

    with open(filename, "rb", buffering=0) as f:
        f.readline() # Skip shebang line.
        pipe(commands, stdin=f, stdout=sys.stdout)

if __name__ == "__main__":
    main()
