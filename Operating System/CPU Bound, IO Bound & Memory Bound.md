當你觀察到 server 花比較多時間處理某些 requests 或 tasks 時，須要考慮以下三種可能原因：

- CPU Bound
- I/O Bound
- Memory Bound

### CPU Bound

- 須要大量的計算
- 常見的發生時機：圖像／影像處理、deep learning
- 解決方法：升級 CPU，特殊情況下可使用 GPU
- 注意事項：一個 CPU 只能處裡一個 process，所以若只升級單一個 CPU，對 multi-process 的程式來說並不會有顯著的速度提升。
### I/O Bound

- 須要大量的 I/O
- 有一種特殊的 I/O bound 叫做 **Network Bound**，主要受限於網路速度
- 常見的發生時機：從資料庫讀取大量資料、log 大量資料、網路傳輸大量資料
- 解決方法：
