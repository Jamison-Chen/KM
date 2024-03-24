Instruction Set Architecture（ISA，指令集架構）

# ISA 的種類：CISC vs. RISC

#TODO 

# 兩大主流 ISAs：x86 vs. ARM

#TODO 

---

- CISC/RISC 指的是兩個不同類別 ISAs，x86/ARM 則分別是 CISC 與 RISC 這兩類 ISAs 的其中一種實作
- 同樣 ISA 的 CPU 中，新版本的通常會向後相容，所以通常舊版 CPU 可以運行的程式也可以在新版 CPU 上運情；但反之就不必然了，因為新版 CPU 通常都會有一些舊版 CPU 沒有（看不懂）的新 instructions，所以往往市面上的軟體都不會被 compile 成最新的版本的 ISA，為的就是讓更多 CPU 可以執行該軟體
