當你觀察到 server 花比較多時間處理某些 requests 或 tasks 時，須要考慮以下三種可能原因：

- CPU Bound
- I/O Bound
- Memory Bound

### CPU-Bound Task

- 須要大量計算的任務
- 常見的發生時機：圖像／影像處理、deep learning
- CPU 大部分時間處於 burst 狀態

    ![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/cpu-bound-task.png>)

- 解決方法：升級 CPU，特殊情況下可使用 GPU
- 注意事項：一個 CPU 只能處裡一個 process，所以若只升級單一個 CPU，對 multi-process 的程式來說並不會有顯著的速度提升

### I/O-Bound Task

- 須要大量 I/O 的任務
- CPU 大部分時間處於 idle 狀態

    ![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/io-bound-task.png>)

- 有一種特殊的 I/O-bound task 叫做 **Network-Bound Task**，指的是須要透過網路傳送大量資料的任務
- 常見的發生時機：從資料庫存取大量資料、log 大量資料、網路傳輸大量資料

### Memory-Bound Task

- 須要大量 memory 的任務，導致需要 context switching
- 常見的發生時機：application 太肥、載入的檔案太大
- 解決方法：加大 RAM

# 參考資料

- <https://www.baeldung.com/cs/cpu-io-bound>
- <https://www.atatus.com/ask/cpu-io-memory-bound>
