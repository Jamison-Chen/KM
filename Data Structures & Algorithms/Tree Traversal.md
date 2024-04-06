# 概述

Tree traversal 依不同的造訪順序，可分為以下四種：

- [Preorder Traversal](<#DFS - Preorder Traversal>)
- [Postorder Traversal](<#DFS - Postorder Traversal>)
- [Inorder Traversal](<#DFS - Inorder Traversal>)
- [Level-order Traversal](<#BFS - Level-Order Traversal>)

其中前三種又叫做 Depth-First Search (DFS)；最後一種又叫做 Breadth-First Search (BFS)。

而實作上面四種 tree traversal 的方法有三種，分別是：

- Recursion
- Iteration + Stack/Queue
- Morris Tree Traversal

# DFS - Preorder Traversal

### 概念

先處理自己，再由左到右處理小孩。

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/preorder-traversal.png>)

### Pre0rder Traversal 的應用

- 瀏覽器渲染 DOM tree 結構

### 使用 Recursion

```Python
def preorder(root):
    if root:
        visit(root)
        for child in root.children:
            preorder(child)
```

### 使用 Iteration + Stack

#TODO

### 使用 Morris Tree Traversal

#TODO

# DFS - Postorder Traversal

### 概念

先由左到右處理小孩，再處理自己。

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/postorder-traversal.png>)

### 應用

- 計算整個資料夾及其子資料夾之大小

### 使用 Recursion

```Python
def postorder(root):
    if root:
        for child in root.children:
            postorder(child)
        visit(root)
```

### 使用 Iteration + Stack

#TODO

### 使用 Morris Tree Traversal

#TODO

# DFS - Inorder Traversal

### 概念

先處理左小孩，再處理自己，最後處理右小孩。（只有 binary tree 可以做 in-order traversal）

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/inorder-traversal.png>)

### 應用

#TODO

### 使用 Recursion

```Python
def inorder(root):
    if root:
        inorder(root.left)
        visit(root)
        inorder(root.right)
```

### 使用 Iteration + Stack

```Python
def inorder(root):
    stack = []
    while True:
        while root:
            stack.append(root)
            root = root.left
        if stack == []:
            break
        root = stack.pop()
        visit(root)
        root = root.right
```

（除非有必要，否則不推薦這個寫法，因為不直覺。）

### 使用 Morris Tree Traversal

#TODO

# BFS - Level-Order Traversal

### 概念

同一層的由左到右處理完，再處理下一層。

![](<https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/level-order-traversal.png>)

### 應用

#TODO

### 使用 Recursion

Level-Order Traversal 無法使用 Recursion 做到。

### 使用 Iteration + Queue

#TODO

### 使用 Morris Tree Traversal

#TODO

**參考資料｜**<https://www.geeksforgeeks.org/level-order-traversal-of-binary-tree-using-morris-traversal/>
