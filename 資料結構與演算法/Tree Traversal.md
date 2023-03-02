# Introduction

---

Tree Traversal 依不同的造訪順序，可分為以下四種：

- Preorder Traversal
- Postorder Traversal
- Inorder Traversal
- Level-order Traversal

其中前三種又叫做 Depth-First Search (DFS)；最後一種又叫做 Breadth-First Search (BFS)。

而實作上面四種 Tree Traversal 的方法有三種，分別是：

- Recursion
- Iteration + Stack/Queue
- Morris Tree Traversal

# DFS: Preorder Traversal

---

### 概念

>先處理自己，再由左到右處理小孩。

![[Screen Shot 2023-01-27 at 2.04.10 PM.png]]

### Pre0rder Traversal 的應用

- 瀏覽器渲染 DOM Tree 結構

### 使用 Recursion

```Python
def preorder(root):
	if root:
		visit(root)
		for child in root.children:
			preorder(child)
```

### 使用 Iteration + Stack

### 使用 Morris Tree Traversal

# DFS: Postorder Traversal

---

### 概念

>先由左到右處理小孩，再處理自己。

![[Screen Shot 2023-01-27 at 2.07.59 PM.png]]

### Postorder Traversal 的應用

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

### 使用 Morris Tree Traversal

# DFS: Inorder Traversal

---

### 概念

>先處理左小孩，再處理自己，再處理右小孩（只有 Binary Tree 可以做 In-Order Traversal）。

![[Screen Shot 2023-01-27 at 2.11.57 PM.png]]

### Inorder Traversal 的應用

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

# BFS: Level-Order Traversal

---

### 概念

>同一層的由左到右處理完，再處理下一層。

![[Screen Shot 2023-01-27 at 2.14.46 PM.png]]

### Level-Order Traversal 的應用

### 使用 Recursion

Level-Order Traversal 無法使用 Recursion 做到。

### 使用 Iteration + Queue

### 使用 Morris Tree Traversal

**參考資料｜**https://www.geeksforgeeks.org/level-order-traversal-of-binary-tree-using-morris-traversal/