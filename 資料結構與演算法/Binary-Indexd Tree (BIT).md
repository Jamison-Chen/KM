# 概述

- BIT 又叫做 Fenwick Tree，由 Peter M. Fenwick 所提出

- BIT 是一種 Binary Tree

# 適用場景

BIT 的強項是用來儲存具有「可累加」屬性的資料，尤其適合用來進行「範圍加總」的任務。

比如現在有一個 array 依序記錄著你從今年第一天到今天為止每一天的「淨收入」（當天收入減當天支出），你可能常常會想要知道從某一天到另一天這段時間的收支加總

依照 [[Tree Traversal#^08a367|Inorder Traversal]] 的順序從 1 開始來編號的話，第 i 個 node 會存著「從 node i 到 node 」

# 參考資料

https://cs.stackexchange.com/questions/10538/bit-what-is-the-intuition-behind-a-binary-indexed-tree-and-how-was-it-thought-a

https://brilliant.org/wiki/fenwick-tree/

https://www.topcoder.com/thrive/articles/Binary%20Indexed%20Trees