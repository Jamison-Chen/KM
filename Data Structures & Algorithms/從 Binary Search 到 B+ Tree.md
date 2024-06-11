# Binary Search

若要在一個亂序的數列中搜尋「最接近但不大於」指定數字 k 的數字，必須遍歷整個數列，所以時間複雜度為 $O(n)$，其中 n 為數列的長度。

但若==數列是排序好的==，搜尋時就可以用時間複雜度僅有 $O(\log n)$ 的 binary search 來達成。Binary search 的概念如下：

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/binary-search.png>)

但由於「[[Sorting Algorithms.canvas|排序]]」本身的時間複雜度至少為 $O(n)$，所以若未來搜尋的機會不多，其實先將亂序數列做排序再做 binary search 並沒有比較節省資源。

### Linked List 中不適合執行 Binary Search

從前面的圖中我們可以發現：binary search 會須要在數列中跳來跳去，並不是一個接著一個讀取，但在 linked list 中我們無法隨心所欲地從一個 node 跳到任意一個 node，只能前往下一個或前一個 node，因此 binary search 無法在 linked list 中實現。

### Array 中適合執行 Binary Search 嗎？

答案是「看情況」。當==資料數量固定時==，array 中適合執行 binary search，但反之則不然。

反之不然的主要原因是：array 在記憶體中使用的是一整塊連續的空間，當這塊連續的空間被佔滿後，若要繼續在 array 中加入新資料，就必須另外找一塊新的、更大的連續空間（通常是原本的兩倍大），然後把原本的資料複製過去，複製完後把原先佔用的空間釋出，最後才加入新資料，整個過程的時間複雜度是 $O(n)$。

```mermaid
flowchart LR
    id1(找一塊兩倍大\n的新連續空間)
    id2(把原本的資\n料複製過去)
    id3(把原先佔用\n的空間釋出)
    id4(加入新資料)
    id1-->id2
    id2-->id3
    id3-->id4
```

##### 反例：資料庫

資料庫中的資料通常是與日俱增的，因此在有需要進行 binary search 的場景中（比如利用 index 做搜尋時）並不會選用 array 來當作存儲資料的結構。

### 實作

用 Python 實作一個 function，回傳「`nums` 中最接近但不小於 `k` 的元素的 index」：

```Python
def binary_search(nums: list[int], k: int) -> int:
    l, r = 0, len(nums) - 1
    while l < r:
        m = (l + r) // 2
        if nums[m] > k:
            r = m
        elif nums[m] < k:
            l = m + 1
        else:
            l = r = m
    if len(result) > l and result[l] < num:
        return l + 1
    else:
        return l
```

# Binary Search Tree

Binary search tree 簡稱 BST。BST 可以說是結合了 linked list 與 array 的優點，既可以執行 binary search，新增資料時的效率也較 array 高。

BST 有以下規則：

- 每個 node 最多只能有兩個 children
- Left child 要小於或等於自己，right child 則要大於自己

Example:

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/binary-search-tree.png>)

在 BST 中單次搜尋、新增、刪除的時間複雜度「平均而言」都是 $O(\log n)$，其中新增跟刪除會另外需要 restructure：

### Operations

##### 搜尋

如果一個 BST 夠平衡，其 depth「平均而言」會是 $\log n$（n 為元素數量），因此搜尋時的複雜度為 $O(\log n)$。

##### 新增

- Step1: 從 root 開始，若欲新增的數值小於 root，則往左邊走；否則往右邊走
- Step2: 重複 Step1 直到想走的那邊沒有 child 為止，並在那邊新增一個 node

Time complexity: $O(\log n)$

##### 刪除

- Step1: 先搜尋到要刪除的目標 (D)
- Step2: 找到整棵樹中數字小於等於 D 且大小最接近 D 的 node（或大於等於 D 且大小最接近 D 的 node）R
- Step3: 將 R 拔下來放到 D 的位置，若 R 有 child（頂多只會有一個 child）則將 R 的 child 接到 R 的 parent 上
- Step4: 如果這麽做會打破 BST 規則的話（也就是說 R 不應該在 D 的位置），就從 R 所在的位置往下進行 restructure。

Time complexity: $O(\log n)$

### Implementation

（以 Python 為例）

```Python
class Node:
    def __init__(self, val: int, parent: "Node | None" = None) -> None:
        self.val = val
        self.parent: Node | None = parent
        self.left: Node | None = None
        self.right: Node | None = None


class BinarySearchTree:
    def __init__(self, nums: list[int]) -> None:
        self.root = None
        self.__build_tree(nums)

    def __build_tree(self, nums: list[int]) -> None:
        self.root = Node(nums.pop()) if nums else None
        for num in nums:
            self.insert(num)

    def insert(self, num: int) -> None:
        if not self.root:
            self.root = Node(num)
            return
        temp = self.root
        while temp:
            if num < temp.val:
                if temp.left:
                    temp = temp.left
                else:
                    temp.left = Node(num, temp)
                    break
            else:
                if temp.right:
                    temp = temp.right
                else:
                    temp.right = Node(num, temp)
                    break

    def remove(self, num: int) -> None:
        # find node with target num
        target = self.root
        while target:
            if target.val > num:
                target = target.left
            elif target.val < num:
                target = target.right
            else:
                break

        if target is None or target.val != num:
            raise AssertionError

        # find nearest
        if target.left:
            nearest = target.left
            while nearest.right:
                nearest = nearest.right
        elif target.right:
            nearest = target.right
            while nearest.left:
                nearest = nearest.left
        else:
            nearest = target

        if nearest is self.root:
            self.root = None
            return

        # prune the nearest from its parent
        if nearest.parent.left is nearest:
            nearest.parent.left = nearest.left or nearest.right
        else:
            nearest.parent.right = nearest.left or nearest.right
        if nearest.left:
            nearest.left.parent = nearest.parent
        elif nearest.right:
            nearest.right.parent = nearest.parent

        # move the nearest to the target
        target.val = nearest.val
        nearest = None

        self.__reconstructure(target)

    def __reconstructure(self, node: Node | None) -> None:
        if node is None:
            return
        if node.left and node.val < node.left.val:
            node.val, node.left.val = node.left.val, node.val
            self.__reconstructure(node.left)
        elif node.right and node.val > node.right.val:
            node.val, node.right.val = node.right.val, node.val
            self.__reconstructure(node.right)
```

前面提到的各種操作的時間複雜度時都是「平均而言」，因為 BST 有可能不像一開始的圖一樣那麼平衡，最極端不平衡的 BST 會長的像下面這樣：

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/imbalanced-bst.png>)

這樣的 BST 其實就是一個 linked list，無論是搜尋、新增或刪除，其時間複雜度都會是 $O(n)$。為避免這種情況發生，於是有了接下來的 balanced BST。

# Balanced BST

Balanced BST 在原本的 BST 上加上了一個限制：「對於任何一個 balanced BST 及其 subtree，各個 leaf nodes 的 depth 不可相差超過 1。」

Balanced BST 只是一個分類，用來平衡樹的方法有很多種，不同方法做出來的樹名字都不同，比如 AVL tree 以及 red-black tree，詳見[[Balanced BST.canvas|本文]]。

在搜尋演算法中，balanced BST 已經是非常有效率的資料結構了，但是若整個演算過程涉及與 disk 溝通，那就要額外考慮 disk I/O 的問題（將 disk 中的資料讀進 memory，以及將 memory 中的資料寫進 disk）因為 ==disk I/O 是造成 latency 的元兇之一==。

### 資料庫的 Index 不使用 Balanced BST

對資料庫進行存取就是其中一種涉及 disk I/O 的例子，當資料庫中某張表的資料量 (n) 極大時，即使 $\log n$ 也會是一個很大的數字。在資料庫中，每往樹的下一層探索都會需要一次 disk I/O（進入 disk 將 child nodes 讀進 memory 中）因此如果樹的 depth 可以再小一點，就可以進一步減少可能的 disk I/O。

其中一個降低 depth 的方法就是==讓 tree 的每個 node 儲存不只一筆資料，並且可以擁有不只兩個 child nodes==，這樣每次進 disk 都可以多讀一點資料回 memory，**B tree** 就是這樣的資料結構。

# B Tree

B tree 也是一種 self-balancing tree，樹中的每一個 node 都可以塞入多筆資料。

一個「m 階 B tree」(B tree of order m) 必須符合下面所有規則：

- 每個 node 最多可以有 m 個 child nodes
- 除了 root node 與 leaf node 以外，其它 node 最少要有 $\lceil {m \div 2} \rceil$ 個 child nodes
- Root node 只少要有兩個 child node，除非 root 就是 leaf
- 所有 leaf nodes 都在同一層
- 一個 internal node 若有 k 個 child nodes，則代表該 node 中有 k-1 筆資料（排序好的）

下面是一個 5 階 B tree（一個深藍色方塊是一個 node，一個淺藍色方塊是一筆資料）：

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/b-tree-of-order-5.png>)

使用這種資料結構儲存資料的 DBMS 會將每個 node 存在不同的 disk unit 中，一個 disk unit 的大小為 4 KB，因此每次進 disk 讀取資料的最小量也是 4 KB。B tree 的目的其實就是盡可能地在每個 node 中塞滿 4 KB 的資料，如此一來便能最大化每次 disk I/O 的效益。

然而 B tree 還是有兩個缺點：

### 「範圍搜尋」沒有效率

範圍搜尋時，要選出所有範圍內的資料就必須遍歷樹中所有在選取範圍內的 nodes，因此須要很多次 disk I/O。

### 須要 Restructrue

若 Node 內的資料變大以致於超過 4 KB，就須要對整棵樹進行 restructure，這個問題的元兇是因為 B tree 選擇「將實際的資料存儲在 node 中」，如果可以只在樹中儲存 index 就可以避免這個問題，而其實這就是 **B+ tree**。

# B+ Tree

B+ tree 可以說是針對上述 B tree 的兩個缺點而來，之所以能克服上述兩個問題，主要係因 B+ tree 沒有將整筆資料存在 node 中，而是只在 internal nodes 中存須要排序 node 的 index，只在 leaf node 中存完整資料。

| | |
|---|---|
|B Tree|![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/b-tree.png>)|
|B+ Tree|![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/b-plus-tree.png>)|

在 B+ tree 中，由於每一筆資料都只能出現在 leaf nodes 中，因此搜尋每一筆資料時所需的 disk I/O 較平均，不會因爲該資料的 index 出現在比較上層就比較少。

B+ Tree 會將各個相鄰的 leaf nodes 串成一串，且整串的資料恰巧會是排序好的，所以範圍搜尋時就不用遍歷整棵樹，只要找到範圍的開頭，便可以直接往右或往左找到下一筆。

>[!Note]
>B tree 和 B+ tree 都是為了解決 disk I/O 問題而生的特殊資料結構，通常只會出現在 DBMS 中，其它 in-memory 的演算法通常不會用到它們。

# 參考資料

- <https://www.programiz.com/dsa/b-tree>
- <https://www.programiz.com/dsa/b-plus-tree>
- <https://ithelp.ithome.com.tw/articles/10221111>
