當你觀察到 server 花比較多時間處理某些 requests/tasks 時，須要考慮以下兩種可能原因：

- CPU Bound
- I/O Bound

# CPU-Bound Task

- 須要大量計算的任務
- Time complexity 高的演算法容易形成 CPU-bound task
- 常見的發生時機：圖像／影像處理、machine learning
- CPU 大部分時間處於 [[CPU Scheduling|burst]] 狀態

    ![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/cpu-bound-task.png>)

- 解決方法：升級 CPU（很貴），特殊情況下可使用 GPU

# I/O-Bound Task

- 須要大量 I/O 的任務
- CPU 大部分時間處於 idle 狀態

    ![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/io-bound-task.png>)

- 有一種特殊的 I/O-bound task 叫做 **Network-Bound Task**，指的是須要透過網路傳送大量資料的任務
- 常見的發生時機：從資料庫存取大量資料、log 大量資料、網路傳輸大量資料

# 同場加映：Memory-Bound Task

- 泛指會佔用大量 memory 的 tasks
- 當 memory 被塞爆時，造成的影響通常不是速度變慢，而是根本無法運算
- Space complexity 高的演算法容易形成 memory-bound task
- 解決方法：加大 RAM

# 參考資料

- <https://www.baeldung.com/cs/cpu-io-bound>
