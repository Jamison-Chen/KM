當你觀察到 server 花比較多時間處理某些任務時，須要考慮以下兩種可能原因：

- CPU Bound
- I/O Bound

# CPU-Bound Task

- 須要大量計算的任務
- Time complexity 高的演算法容易形成 CPU-bound task
- 常見的發生場景：圖像／影像處理、machine learning
- CPU 大部分時間處於 [burst](</Operating System/CPU Scheduling.draft.md>) 狀態

    ![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/cpu-bound-task.png>)

- 解決方法：
    - 降低演算法的 time complexity
    - 升級 CPU，特殊情況下可使用 GPU

# IO-Bound Task

- 須要大量 I/O (input/output) 的任務
- CPU 大部分時間處於 idle 狀態

    ![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/io-bound-task.png>)

- 有一種 IO-bound task 叫 **network-bound task**，指的是須要透過網路傳送大量資料的任務
- 常見的發生時機：從資料庫存取大量資料、stdout 大量資料、網路頻寬過窄

# 同場加映：OOM

任何 program 要執行的話都必須被先載入至 memory，所以當 memory 資源被用盡時，造成的影響通常不是速度變慢，而是 program 根本無法運行，這種狀況稱為 OOM (out-of-memory)。

OOM 可能是由常態性的 memory leak 造成（慢性死亡），或者是一次從 network 或 disk 拉取過多資料進入 memory 所導致（瞬間死亡）。

在早期，每台電腦的 memory 都很少，且還沒有 [virtual memory](</Operating System/Memory Management.draft.md#Virtual Memory>) 這項技術，所以 OOM 相對較常發生；但後來 virtual memory 的出現使得 OOM 很難真的發生，通常是 OS 會有一些限制 process 使用過多 physical memory 的機制，比如 **per-process memory limits**。

### OOM Killer

OS kernel 在 OOM 發生後，會啟動嘗試將一些 process 強制終止，藉此釋放 memory 讓自己活過來，這個機制叫做 OOM killer。

# 參考資料

- <https://www.baeldung.com/cs/cpu-io-bound>
- <https://en.wikipedia.org/wiki/Out_of_memory>
