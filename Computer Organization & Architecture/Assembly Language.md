Assembly language（組合語言）are converted into executable [Machine Code](</Computer Organization & Architecture/Machine Code.md>) by an [Assembler](</Computer Organization & Architecture/Assembler.md>).

Because assembly languages depend on the machine code instructions, each assembly language is specific to a particular computer architecture.

Sometimes an assembler is specific to an [operating system](https://en.wikipedia.org/wiki/Operating_system) or to particular operating systems.

Assembly languages were once widely used for all sorts of programming. However, by the 1980s, their use had largely been supplanted by **higher-level languages**, in the search for improved programming productivity. Today, assembly language is still used for direct hardware manipulation, access to specialized processor instructions, or to address critical performance issues.

In contrast to assembly languages, most [high-level programming languages](https://en.wikipedia.org/wiki/High-level_programming_language) are generally portable across multiple architectures but require **interpreting or compiling** (See [Compilation vs Interpretation](</Computer Science/Compilation vs Interpretation.md>)), a much more complicated task than assembling.

Most early microcomputers relied on hand-coded assembly language. This was because these systems had severe resource constraints, imposed idiosyncratic memory and display architectures, and provided limited, buggy system services. Perhaps more important was the lack of first-class high-level language compilers suitable for microcomputer use.

# Typical Uses

* [Device drivers](https://en.wikipedia.org/wiki/Device_driver)
* Low-level [embedded systems](https://en.wikipedia.org/wiki/Embedded_system)
*  [Real-time](https://en.wikipedia.org/wiki/Real-time_computing) systems

# Typical applications

### System's [boot](https://en.wikipedia.org/wiki/Booting) code

The low-level code that initializes and tests the system hardware prior to booting the operating system and is often stored in ROM

e.g. [BIOS](https://en.wikipedia.org/wiki/BIOS)

### Low-level code

Low-level code cannot rely on the availability of pre-existing system calls and must indeed implement them for the particular processor architecture on which the system will be running.

e.g. [operating system kernels](https://en.wikipedia.org/wiki/Kernel_(operating_system))

### [Inline assembly](https://en.wikipedia.org/wiki/Inline_assembly)

Some compilers for relatively low-level languages, such as Pascal or C, allow the programmer to embed assembly language directly in the source code. Programs using such facilities can then construct abstractions using different assembly language on each hardware platform. The system's portable code can then use these processor-specific components through a uniform interface.
