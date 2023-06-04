CAP Theorem 又叫做 Brewer's Theorem。

CAP Theorem 指出，一個服務最多只能同時確保 Consistency, Availability 與 Partition Tolerance 三者的其中兩個：

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/cap_theorem.png>)

### Consistency

Clients 總是可以從資料庫讀取到最新的資料。

### Availability

所有 Request 都會得到 non-error 的 response。

### Partition Tolerance

除了通訊問題以外，服務必須持續運作不間斷。

---

[[ACID vs. BASE#ACID|ACID Model]] 的宗旨即「在具備 Partition Tolerance 的條件下，提供具備 Consistency 的服務」(CP)，銀行業通常會需要這種 Model。

相對地，[[ACID vs. BASE#BASE|BASE Model]] 的宗旨為「在具備 Partition Tolerance 的條件下，提供具備 Availability 的服務」(AP)。

# 參考資料

- <https://en.wikipedia.org/wiki/CAP_theorem>
