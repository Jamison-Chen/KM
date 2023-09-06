![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/deadlocks.png>)

以上方的 RAG 為例，`P1`、`P2` 兩個執行中的 processes 現在都需要額外資源才能繼續執行，也都必須執行完後才會釋出它們身上的資源。

`P1` 擁有資源 `R1`，額外需要資源 `R2`；`P2` 擁有資源 `R2`，還額外需要資源 `R1`，兩邊都在互相等待而沒有任何一個可繼續。

# 出現 Deadlock 的條件

Deadlock 只有在下列四個條件「同時滿足」時才會發生：

- **No Preemption**：系統資源不能被強制從一個 process 中搶走。
- **Hold and Wait**：一個 process 可以在等待時持有系統資源。
- **Mutual Exclusion**：系統資源無法同時分配給多個 processes。
- **Circular Waiting**：一系列 processes 互相持有其他 process 所需要的系統資源。

當發生 deadlock 時，必須破壞其中至少一項條件才能解除 deadlock 的狀態。
