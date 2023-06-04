當多個 clients 同時對 server 發出「會導致狀態變更」的 requests 時，處理 requests 的順序會影響結果，因此需要使用 queue 來確保 requests 的順序，這個 queue 只能有一個，且負責處理這個 queue 的 worker (consumer) 也只能有一個 (single thread)，下方為示意圖：

![[SingularUpdateQueue.png]]

從 queue 中讀取 task 時，可以／通常會設置 timeout，用以避免 queue 遭到阻塞

# 參考資料

- <https://martinfowler.com/articles/patterns-of-distributed-systems/singular-update-queue.html>