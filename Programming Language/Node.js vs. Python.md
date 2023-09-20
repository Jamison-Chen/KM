# 速度

### Iteration

e.g.

```Python
# Python 3.11
import time

start = time.time()
x = 0
for i in range(100000000):
    x += 1
print(f"{time.time() - start}s")  # 4.875 s
```

```JavaScript
// Node v18.16.1
const start = Date.now();
let x = 0;
for (let i = 0; i < 100000000; i++) {
    x++;
}
console.log(`${Date.now() - start} ms`);  // 64 ms
```

可見 Node.js 在 iteration 上比 Python 快了 80 ~ 100 倍 🚀。

### Recursion

e.g. Fibonacci Sequence

```Python
# Python 3.11
import time

def fib(n):
    if n < 2:
        return 1
    return fib(n - 1) + fib(n - 2)

start = time.time()
fib(38)
print(f"{time.time() - start}s")  # 4.333 s
```

```JavaScript
// Node v18.16.1
function fib(n) {
    if (n < 2) return 1;
    return fib(n - 1) + fib(n - 2)
}

const start = Date.now();
fib(38);
console.log(`${Date.now() - start} ms`);  // 364 ms
```

可見 Node.js 在運行 recusive function 時比 Python 快了約 10 倍。

### File Reading

e.g.

```Python
# Python 3.11
start = time.time()
with open("./big_data.json") as f:
    content = f.read()
    print(len(content))  # 87295572
    print(f"{time.time() - start}s")  # 0.031 s
```

```JavaScript
// Node v18.16.1
const fs = require("fs");
const start = Date.now();
const content = fs.readFileSync(
    "../Downloads/News_Category_Dataset_v3.json",
    "utf8"
);
console.log(content.length);  // 87295572
console.log(`${Date.now() - start} ms`);  // 50 ms
```

可見 Python 在 reading file 時比 Node.js 快了約 2 倍。

# Multi-threads 下的速度

#TODO 
