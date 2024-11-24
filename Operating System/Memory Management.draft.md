# Mono-Programming

# Multi-Programming

### Partitioning

### Paging

### Demand Paging

### Demand Segmentation

# Virtual Memory

#TODO 

# Memory Protection

### Protection Ring & CPU Modes

又叫做 hierarchical protection domains，是 OS 用來保護 [kernel](</Operating System/Kernel.draft.md>) 的方式。

Protection ring 可以有若干層，至少會有兩層，下圖是一個四層的示意圖：

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/protection-ring-4.jpeg>)

Protection ring 的實作方式通常是透過 CPU 切換不同的 CPU modes 來達成，一個 mode 對應到一個 protection ring，CPU 至少會有 **Kernel mode** 與 **User mode** 兩種 modes：

|Mode|Description|
|---|---|
|Kernel mode|CPU 可以執行任何其所使用的 instruction set architecture 之下的指令；<br/>CPU 可以存取任何 memory address area|
|User mode|CPU 指能執行的指令有限；無法存取部分 memory address area|

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/protection-ring-2.jpeg>)

# 參考資料

- <https://en.wikipedia.org/wiki/Virtual_memory>
- <https://en.wikipedia.org/wiki/Protection_ring>
- <https://en.wikipedia.org/wiki/Memory_protection>
