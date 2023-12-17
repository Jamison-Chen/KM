>[!Note]
>閱讀本文前，建議先了解 [[程式語言的分類#編譯式 vs. 直譯式]]。

Interpretation (轉譯) 與 Compilation (編譯) 並非互斥的概念，很多 interpreter 做的事情與 compiler 是部分重疊的。

# Development Cycle

During the software development cycle, programmers make frequent changes to source code. When using a compiler, each time a change is made to the source code, they must wait for the compiler to translate the altered source files and link all of the binary code files together before the program can be executed. The larger the program, the longer the wait.

By contrast, a programmer using an interpreter does a lot less waiting, as the interpreter usually just needs to translate the code being worked on to an intermediate representation.

Compiled code is generally less readily debugged as editing, compiling, and linking are sequential processes that have to be conducted in the proper sequence with a proper set of commands. For this reason, many compilers also have an executive aid, known as a [Make](https://en.wikipedia.org/wiki/Make_(software)) file and program. The Make file lists compiler and linker command lines and program source code files, but might take a simple command line menu input (e.g. "Make 3") which selects the third group (set) of instructions then issues the commands to the compiler, and linker feeding the specified source code files.

# Distribution

A compiler converts source code into binary instruction for a specific processor's architecture, thus making it less portable. This conversion is made just once, on the developer's environment, and after that the same binary can be distributed to the user's machines where it can be executed without further translation. A [cross compiler](https://en.wikipedia.org/wiki/Cross_compiler) can generate binary code for the user machine even if it has a different processor than the machine where the code is compiled.

An interpreted program can be distributed as source code. It needs to be translated in each final machine, which makes the program distribution independent of the machine's architecture. However, the portability of interpreted source code is dependent on whether **the target machine having a suitable interpreter**. If the interpreter needs to be supplied along with the source, the overall installation process is more complex than delivery of a monolithic executable since the interpreter itself is part of what need be installed.

# Efficiency

The main disadvantage of interpreters is that an interpreted program typically runs slower than if it had been compiled. It generally takes longer to run a program under an interpreter than to run the compiled code but it can take less time to interpret it than the total time required to compile and run it.

Interpreting code is slower than running the compiled code because the interpreter must analyze each statement in the program each time it is executed and then perform the desired action, whereas the compiled code just performs the action within a fixed context determined by the compilation. This [runtime](https://en.wikipedia.org/wiki/Run_time_(program_lifecycle_phase)) analysis is known as "interpretive overhead". Access to variables is also slower in an interpreter because the mapping of identifiers to storage locations must be done repeatedly at run-time rather than at [compile time](https://en.wikipedia.org/wiki/Compile_time).

|Basis for Comparison|Compiler|Interpreter|
|:-:|:-:|:-:|
|Input|It takes an entire program at a time.|It takes a single line of code or instruction at a time.|
|Output|It generates intermediate object code.|It does not produce any intermediate object code.|
|Working mechanism|The compilation is done before execution.|Compilation and execution take place simultaneously at runtime.|
|Speed|Comparatively faster|Slower|
|Memory|Memory requirement is more due to the creation of object code.|It requires less memory as it does not create intermediate object code.|
|Errors|Display all errors after compilation, all at the same time.|Displays one error at a time.|
|Error detection|Difficult|Easier comparatively|
|Pertaining programming languages|C, C++, C#, Scala, TypeScript, etc.|Python, PHP, Perl, Ruby, etc.|

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/interpreted-language-vs-compiled-language.png>)
