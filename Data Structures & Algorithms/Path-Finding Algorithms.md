在 [Graph Theory](</Data Structures & Algorithms/Graph Theory.canvas>) 中，找尋兩個節點的最短路徑是最常見的問題之一。

# Dijkstra's Algorithm

Dijkstra's algorithm 可以找到圖中「單一起點」到「所有終點」的最短路徑。許多 [network layer](</Network/OSI Model.draft.md>) 的 protocols（如 IS-IS 與 OSPF）都是使用 Dijkstra's algorithm 來尋找兩個 hosts 在網路中的最短路徑。

要使用 Dijkstra's algorithm 的先決條件是我們要知道圖中所有 vertices 與 edges 的資訊。

### Idea

- Step1: 初始化一個 `distance_map`，用來記錄起點到所有節點的最短距離與最短路徑；一個 `came_from`，記錄每個節點要從哪個節點過去
- Step2: 從起點開始找起，將起點標記為 `current`
    - 從起點到 `current` 的最短距離是 0，最短路徑就是不動 (base case)
- Step3: 探索所有與 `current` 相鄰的節點
    - Key idea: 若節點 w、v 為鄰居，則：$D(u, v) = min(D(u, v), D(u, w) + W_{w, v})$
    - 因為已經知道「起點到 `current` 的距離」了，所以就目前的資訊來說，起點到 `current` 的鄰居的距離可以是「起點到 `current` 的距離」+「`current` 到鄰居的距離」
    - 如果 `distance_map` 裡本來就有記錄「起點到 `current` 的鄰居的距離」，則在原值與新值間取較小的那個，否則直接更新 `distance_map`
    - 如果有更新到 `distance_map`，就要同時將該相鄰節點標記為「待探索節點」，也要記錄 `came_from[鄰居] = current`
- Step4: 在所有待探索節點中，找到與起點距離最短的那個節點（透過 `distance_map` 查詢）改令 `current` 為該節點，並將「待探索節點」的標記從該節點上移除
    - 如果 `current` 就是終點，則演算法結束
    - 在首次執行到這個步驟時，因為所有待探索節點都會是起點的鄰居，所以新的 `current` 到起點的最短路徑就是那條將 `current` 與起點相連的 edge；最短距離就是那條 edge 的 weight
- Step5: 如果還有「待探索節點」就回到 Step3；反之就結束

### Code

以 Python 為例：

```Python
import heapq
from collections import defaultdict


def _get_path(end: str, came_from: dict[str, str]) -> list[str]:
    path = []
    while end in came_from:
        path.append(end)
        end = came_from[end]
    if end:
        path.append(end)
    return path[::-1]


def dijkstra(
    graph: dict[str, set[tuple[str, float]]], source: str, target: str
) -> tuple[float, list[str]]:
    distance_map = defaultdict(lambda: float("inf"))
    distance_map[source] = 0
    came_from: dict[str, str] = {}
    visited: set[str] = set()

    # [(distance, vertex), ...]
    # Put distance at the first position of each tuple for heapq to sort
    unsolved_heap: list[tuple[float, str]] = [(0, source)]

    while unsolved_heap:
        current_distance, current_vertex = heapq.heappop(unsolved_heap)
        visited.add(current_vertex)
        if current_vertex == target:
            break
        for neighbor, weight in graph[current_vertex]:
            if neighbor not in visited and (new_distance := current_distance + weight) < distance_map[neighbor]:
                distance_map[neighbor] = new_distance
                came_from[neighbor] = current_vertex
                heapq.heappush(unsolved_heap, (new_distance, neighbor))
    return distance_map[target], _get_path(target, came_from)
```

### Complexity

- Time complexity: $O((E + V) \cdot \log{V})$
    - E 為 edges 的數量；V 為 vertices 的數量
    - 當 E 的數量達到 $V^2$ 量級時，可以說整個演算法的複雜度為 $O(V^2 \cdot \log{V})$
    - 若使用 Fibonacci heap 取代 [Binary Heap](</Data Structures & Algorithms/Binary Heap.md>) 來實作 priority queue，則 complexity 會變成 $O(E + V \cdot \log{V})$
        - 當 E 的數量達到 $V^2$ 量級時，則為 $O(V^2)$
- Space complexity: $O(V^2)$

# A\* Algorithm

A\* algorithm 可以被視為是 Dijkstra's algorithm 的一種延伸，其特色是會使用一個 heuristic function 來預測終點與目前位置的距離，達到加速的效果。通常 heruristic function 會是某種數學上的距離（如 Euclidean distance、Manhattan distance、Chebyshev distance 等）或是過往的統計值。

A\* algorithm 與 Dijkstra's algorithm 在效率上最大的差異在於：只要執行一次 Dijkstra's algorithm 就可以知道起點與圖中所有其它節點的最短路徑與距離；執行一次 A\* algorithm 只能知道一對起點與終點的最短路徑與距離。

### Idea

A\* algorithm 與 Dijkstra's algorithm 一樣有 $D(u, v) = min(D(u, v), D(u, w) + W_{w, v})$ 這個核心概念，只是在 A\* 中會把 $D(source, n)$ 以 $g(n)$ 表示，所以在 A\* algorithm 中會寫成：

$$
g(n) = min(g(n), g(m) + W_{m, n})
$$

另外，給定一個可以預測節點 n 到終點距離的 heruristic function $h(n)$，則「從起點經過節點 n 到終點的最短距離」的預測值會等於「從起點到節點 n 的最短距離」加上「節點 n 到終點的預測距離」

$$
f(n) = g(n) + h(n)
$$

>[!Note]
>Dijkstra's algorithm 等價於 $h(n) = 0, \forall n$ 的 A\* algorithm。

### Code

以 Python 為例：

```Python
from functools import lru_cache
import heapq


@lru_cache(maxsize=None)
def _heuristic(source: str, target: str) -> float:
    return abs(ord(source) - ord(target))


def _get_path(end: str, came_from: dict[str, str]) -> list[str]:
    path = []
    while end in came_from:
        path.append(end)
        end = came_from[end]
    if end:
        path.append(end)
    return path[::-1]


def astar(
    graph: dict[str, set[tuple[str, float]]], source: str, target: str
) -> tuple[float, list[str]]:
    g_score: dict[str, float] = defaultdict(lambda: float("inf"))
    g_score[source] = 0
    f_score: dict[str, float] = {source: _heuristic(source, target)}
    came_from: dict[str, str] = {}
    visited: set[str] = set()

    # [(distance, vertex), ...]
    # Put distance at the first position of each tuple for heapq to sort
    unsolved_heap: list[tuple[float, str]] = [(0, source)]

    while unsolved_heap:
        _, current_vertex = heapq.heappop(unsolved_heap)
        visited.add(current_vertex)
        if current_vertex == target:
            break
        for neighbor, weight in graph[current_vertex]:
            if neighbor not in visited and (new_g_score := g_score[current_vertex] + weight) < g_score[neighbor]:
                g_score[neighbor] = new_g_score
                f_score[neighbor] = g_score[neighbor] + _heuristic(neighbor, target)
                came_from[neighbor] = current_vertex
                heapq.heappush(unsolved_heap, (f_score[neighbor], neighbor))
    return g_score[target], _get_path(target, came_from)
```

### Complexity

- Time complexity: $O(b^d)$
    - b：平均每個節點有幾個鄰居
    - d：起點只少要跳幾次才能到終點（這不一定是最短距離）
- Space complexity: $O(b^d)$

# Bellman-Ford Algorithm

### Idea

### Code

### Complexity

- Time complexity: $O(V \cdot E)$
    - E 為 edges 的數量；V 為 vertices 的數量
    - 當 E 的數量達到 $V^2$ 量級時，可以說整個演算法的複雜度為 $O(V^3)$
- Space complexity: $O(V + E)$

# Floyd-Warshall Algorithm

由於 Dijkstra's algorithm 一次只能找一個起點到所有終點的最短路徑，所以如果要知到所有 node pairs 間的最短路徑，其中一種方法就是對圖中的所有節點都做一次 Dijkstra's algorithm，但==如果我們只想知道這些 node pairs 的最短路徑的距離，而不用知道這些路徑實際上會經過哪些 vertices==，則有另一個專門解決這種問題的演算法：Floyd-Warshall algorithm。

所以嚴格來說，Floyd-Warshall algorithm 並不是最短「路徑」搜尋演算法，而是最短「距離」搜尋演算法。

### Idea

假設在一個圖中有編號 1 到 n 的 n 個節點，且存在一個演算法 $f(i, j, k)$ 可以得到 vertex i 與 vertex j 之間的最短距離（在只能經過 vertices 1 ~ k 的限制下），則要找到所有 node pairs 在圖中最短路徑的方法，就是對所有 node pairs (i, j) 計算一次 $f(i, j, n)$。

假設 vertex i 與 vertext j 間的最短路徑有經過 vertext k，則如果限制「不能經過 k」，就會使得 i、j 的最短距離變長；但若 i、j 的最短路徑沒有經過 k，則這個限制就不會對最短距離造成影響。因此可以得到以下關係式：

$$
f(i, j, k) \le f(i, j, k - 1)
$$

而若 i、j 間的路徑有經過 k，則其實可以將 i → j 拆成 i → k 與 k → j 兩段，但這段經過 k 的路徑並不一定是最短的，所以：

$$
f(i, j, k) \le f(i, k, k - 1) + f(k, j, k - 1)
$$

而因為 i、j 間的最短路徑要嘛就是有經過 k，不然就是沒有經過 k，要在兩個走法間選較短的那個，所以：

$$
f(i, j, k) = min(f(i, j, k - 1), f(i, k, k - 1) + f(k, j, k - 1))
$$

最後這行關係式是一個遞迴關係式，因此我們須要知道 base case（也就是 $f(i, j, 0)$）的答案：

$$
f(i, j, 0) = edge(i, j)
$$

如果沒有 edge 連接 i、j，則 $edge(i, j) = \infty$。

### Code

以 Python 為例：

```Python
from collections import defaultdict


def shortestCost(
    vertices: list[str], edges: dict[tuple[str, str], int]
) -> dict[tuple[str, str], int]:
    result = defaultdict(lambda: float("inf"))
    for v_pair, cost in edges.items():
        result[v_pair] = cost
    for v in vertices:
        result[(v, v)] = 0
    for k in vertices:
        for i in vertices:
            for j in vertices:
                result[(i, j)] = min(result[(i, j)], result[(i, k)] + result[(k, j)])
    return result
```

### Complexity

- Time complexity: $O(n^3)$
- Space complexity: $O(n^2)$

# 參考資料

- <https://en.wikipedia.org/wiki/Shortest_path_problem>
- <https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm>
- <https://en.wikipedia.org/wiki/A*_search_algorithm>
- <https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm>
