# 概述

- BIT 又叫做 Fenwick Tree，由 Peter M. Fenwick 所提出

- BIT 就結構上來講是一種 binary tree

# 適用場景

BIT 的強項是用來儲存具有==可累加==屬性的資料，尤其適合用來進行==範圍加總==的任務。

比如現在有一個 array 依序記錄著你從某天開始到今天為止每一天的「淨收入」（當天收入減當天支出），而你可能常常會想要知道從某一段時間內的淨收入，比如這一個月或從年初到現在，這個時候就很適合使用 BIT 來作為資料結構。

依照 [inorder traversal](</Data Structures & Algorithms/Tree Traversal.md#DFS - Inorder Traversal>) 的順序從 1 開始為 BIT 以及 array 編號的話，第 i 個 tree node 會存著「array 中第 $i-2^r+1$ 個元素到第 $i$ 個元素的加總」，其中 $r$ 為 $i$ 以二進制表達時從右邊數來第一個 1 的 index（從 0 開始數）(i.e. $r$ is the position of the least significant non-zero bit of $i$)

看起來大概像這樣：

#TODO 

# 參考資料

- <https://cs.stackexchange.com/questions/10538/bit-what-is-the-intuition-behind-a-binary-indexed-tree-and-how-was-it-thought-a>
- <https://brilliant.org/wiki/fenwick-tree/>
- <https://www.topcoder.com/thrive/articles/Binary%20Indexed%20Trees>
