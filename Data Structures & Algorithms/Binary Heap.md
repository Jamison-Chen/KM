# 定義

- Binary heap 是一種 binary tree
- 分為 **min heap** 與 **max heap**
    - Min heap 的每個 node 的值必定「小於或等於」自己的兩個 child nodes 的值
    - Max heap 的每個 node 的值必定「大於或等於」自己的兩個 child nodes 的值
    - 同 parent 的兩個 children 間的大小關係沒有限制
- 由左往右完全填滿一層後，才可以有下一層（binary heap 是一種 self-balanced tree）

# 性質

- 如果一個節點只能存一筆資料，則一個 depth 為 n 的 binary heap 可以存 $2^{n - 1}$ ~ $2^n - 1$ 筆資料
- 一個 binary heap 的任何一個 subtree 也會是一個 binary heap
- Min heap 的 root 一定是最小值；max heap 的 root 一定是最大值

# 建構 Binary Heap 的方式

建構 binary heap 這個動作又叫做 "**heapify**"，分為 top-down 與 bottom-up 兩種方式，top-down 比較直覺、好實作，bottom-up 則比較有效率。

### Top-Down Heapify

（假設要實作 max heap）從 root node 開始建立，若新建立的 node 有 parent，則要比較 parent 的值與新 node 的值，如果 parent 的值比較小，就要將新 node 的值與 parent 的值對調 (swap)；只要有對調，拿到新值的 parent node 就須要再往上與它的 parent 比較，一直比到沒有 swap 發生或抵達 root node 為止。（往上比較的過程叫做 "**up-heap**"）

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/max-heap-top-down-heapify.png>)

Time complexity: $O(n \cdot \log n)$

### Bottom-Up Heapify

（以 max heap 為例）由於其實在給定元素個數時就可以知道 heap 的形狀了，因此可以先建立好一個所有 nodes 都沒有值的空 heap，並依下列規則填入值：

- 從「最底層最左邊」的 node 開始填入值
- 如果要填入值的 node 沒有 child node 則可直接繼續填下一個 node
- 若要填入值的 node 有 child node(s)，則先拿 child node(s) 中較大的值與要填入的值比較，若要填入的值較小，則將該值與 larger child 的值對調 (swap)，反之則直接填入
- 若有因前項規則而發生 swap，則拿到新值的 child node 要再與它的 larger child 比較，一直比到沒有對調發生或抵達 leaf node 為止（往下比較的過程叫做 "**down-heap**"）

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/max-heap-bottom-up-heapify.png>)

Time complexity: $O(n)$

>[!Note]
>Bottom-up heapify 的 time complexity 之所以是 $O(n)$ 不是 $O(n \cdot \log n)$，是因為整個 bottom-up construction 過程中，swap 次數不會超過 2n 次。

# 移除最大／最小值

因為 max heap 的 root 一定是最大值、min heap 的 root 一定是最小值，所以直接看 root 就可以知道最大／最小值為何（時間複雜度為 $O(1)$），但如果要將這個值移除，就勢必會動到 heap 的結構，最有效率的方法就是「取得 root 的值後，把 heap 中的最後一個 node 拔下來，放在 root 的位置，然後從 root 的位置開始視情況進行 down heap。」

下圖以 min heap 為例：

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/min-heap-extract-min.png>)

# Data Structure Base

可以先實作 `Node` 資料結構，再將 nodes 串起來，也可以直接使用 array，以 max heap 為例：

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/binary-heap-tree-array-representation.png>)

### Node-Based

- 每個 node 須要有 `value`、`parent`、`left_child`、`right_child`、`next` 五個 properties。
- Push 時須要找到 new node 要加在哪裡，演算法如下：
    - 有一個 pointer 記錄目前的 last node
    - 從 last node 開始往上走，直到第一次遇到一個 left child，或遇到 root（如果 last node 自己就是 left child，這個步驟就不用動）
    - 若遇到的是 left child，則再多走一步到該層的 right child。如果 right child 不存在，則直接新增一個 node 並讓它成為 right child，並將 last node 指向新增的 node，演算法結束；否則進入下一步
    - 經過以上步驟後，會停在 root 或某個 right child
    - 如果目前所在的 node 沒有 right child，則直接新增一個 node 並讓它成為 right child，並將 last node 指向新增的 node；如果目前所在的 node 有 right child，則持續往「左下」走，直到走到 leaf node，然後新增一個 node 並讓它成為 leaf node 的 left child，然後將 last node 指向新增的 node
    - e.g. ![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/update-the-last-node-in-a-min-heap.png>)
    - Time complexity: $O(\log{n})$

比起 node，array 輕量許多，所以簡單的 heap 通常不會用 node 實作。

# 實作

以 Python 實作：

- Bottom-up heapify
- Array-based
- Pop method
- Push method

```Python
class MinHeap:
    def __init__(self, nums: list[int]) -> None:
        self.__h = self.__construct(list(nums))

    @property
    def size(self) -> int:
        return len(self.__h)

    def __construct(self, nums: list[int]) -> list[int]:
        import math

        result: list = [None] * len(nums)
        depth = math.floor(math.log2(len(nums)))
        while nums:
            for idx in range(2**depth - 1, len(nums)):
                result[idx] = nums.pop()
                self.__downheap(result, idx)
            depth -= 1
        return result

    @staticmethod
    def __downheap(heap: list[int], idx: int) -> None:
        while (l := idx * 2 + 1) < len(heap):
            if (r := idx * 2 + 2) < len(heap):
                if heap[l] < heap[r] and heap[l] < heap[idx]:
                    heap[idx], heap[l] = heap[l], heap[idx]
                    idx = l
                elif heap[r] < heap[idx]:
                    heap[idx], heap[r] = heap[r], heap[idx]
                    idx = r
                else:
                    break
            elif heap[l] < heap[idx]:
                heap[idx], heap[l] = heap[l], heap[idx]
                idx = l
            else:
                break

    @staticmethod
    def __upheap(heap: list[int], idx: int) -> None:
        while idx > 0:
            parent_idx = (idx - 1) // 2
            if heap[idx] < heap[parent_idx]:
                heap[idx], heap[parent_idx] = heap[parent_idx], heap[idx]
                idx = parent_idx
            else:
                break

    def pop(self) -> int:
        if len(self.__h) == 1:
            return self.__h.pop()
        result = self.__h[0]
        self.__h[0] = self.__h.pop()
        self.__downheap(self.__h, 0)
        return result

    def push(self, num: int) -> None:
        self.__h.append(num)
        self.__upheap(self.__h, len(self.__h) - 1)
```

使用方法如下：

```Python
h = MinHeap([4, 1, 2, 5, 3, 6])
h.pop()  # 1
h.push(3)
```

>[!Note]
>其實 Python 有內建 [heapq](https://docs.python.org/3/library/heapq.html) library，不須要自己實作。

# 應用

### Priority Queue

Priority queue 的定義：「不論 enqueue 元素的順序為何，每次 dequeue 都會將 queue 中優先序最高的元素拿出。」Heap 可以用 $O(\log n)$ 的時間複雜度做到 enqueue 與 dequeue。

### Heap Sort

將所有元素放進 heap，然後再逐一 pop 出來。Heap sort 具有 $O(n \cdot \log n)$ 的時間複雜度，詳見 [Sorting Algorithms](</Data Structures & Algorithms/Sorting Algorithms.canvas>)。

# 其它 Heap

- [Fibonacci heap](https://www.youtube.com/watch?v=6JxvKfSV9Ns)

# 參考資料

- <https://en.wikipedia.org/wiki/Binary_heap>
- <https://www.enjoyalgorithms.com/blog/introduction-to-heap-data-structure>
- <https://www.enjoyalgorithms.com/blog/heapify-operation-heap-data-structure>
