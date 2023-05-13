> [!Note]
> 1. Celery Task 只有在 api 裡 call 會有 async 的效果，用 crontab 或 script call 會是 sync 的。
> 2. 在 Local，需要 `make tunnel` $\rightarrow$ `make celery-debug`，才能讓 Celery 開始運行。

### Step1: 定義 Task

定義 task 的地方有兩個，分別是`background/tasks/event.py` 與 `background/tasks/longrun.py`，若執行 task 需要 30 秒以內，則放 `event`；若介於 31 ~ 300 秒，則放 `longrun`；會超過 300 秒的 task 須切分成多個 longrun task。

Task 的命名傳統是以 `task_` 開頭，可以接收 0 到多個參數，舉例而言：

```python
# background/tasks/event.py
def task_do_somthing(uids):
    ...
```

### Step2: 在 API Endpoint 中呼叫 Task 的 `delay` Function

Call `delay` function 後再把 task 吃的參數放進去，舉例而言：

```python
from background.tasks.event import task_do_something

def an_api_endpoint():
    task_do_something.delay(uids=[1, 2, 3])
```

### Step3: Reload Celery: `make celery-reload`

`make celery-reload` = `make celery-stop` + `make celery-start`