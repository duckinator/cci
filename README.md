# cci

cci wraps tools in the LLVM toolchain to allow you to compile and run C
programs on-the-fly using a JIT compiler, instead of requiring a
dedicated compilation phase.

## Usage

To use cci, you point the shebang line of a C file at it.

That is sufficient to use it, but you can also specify more arguments
to e.g. enforce stricter error checking by Clang.

Due to limitations in how shebang lines work, when you use cci, you have
to put arguments to Clang on the line immediately after the shebang line.

To avoid ambiguity, that line must start with "// cci:".

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

## Debugging

If you include the argument "-###" in the arguments, it will be
passed through to Clang for debugging purposes.
