#OOP 

# Attribute

Python 中的 class 與其它 OOP 語言一樣，可以有 class attribute 以及 instance attribute，class attribute 須定義在 constructor (`__init__` method) 之前；instance attribute 則須定義在 constructor 裡面，舉例如下：

```Python
class Dog:
    # class attributes
    max_age = 20;

    def __init__(self):
        # instance attributes
        self.age = 0
        self.weight = 10
```

與其它 OOP 語言一樣，雖然 class attribute 其實也可以用 instance 來存取，但一般而言不會這麼做。

# Method

在一般的 OOP 語言（比如 Java、C++ 和 C#）中，method 只分為 instance method 與 class method 兩種，然而 Python class 的 method 卻有三種，分別是 instance method、class method 以及 static method，這是因為 ==Python 把其它 OOP 語言的 class method 細分成 class method 與 static method==。

### Instance Method

Instance method 專門給實例化後的 object 使用，這點 Python 和其它 OOP 語言是一樣的，範例程式碼如下：

```Python
class Dog:
    def __init__(self):
        self.age = 0
        self.weight = 10

    def eat(self, n):
        self.weight += n

    def grow(self):
        self.eat(1)
        self.age += 1

if __name__ == "__main__":
    d = Dog()
    d.grow()
```

###### `self` 參數

- 定義 constructor 與其他 instance methods 時，第一個參數固定用來代表 instance 本身，這個參數通常被命名為 `self`
- 擁有 `self` 參數使得 instance methods 可以存取其他 instance attributes/methods，比如上例中的 `self.age = 0` 與 `self.eat(1)`
- 呼叫 instance method 時，並==不須要填入引數給 `self`==。以上例而言，在 `grow` method 裡呼叫 `eat` method 時只給了一個引數 `1`（給參數 `n`）；object `d` 呼叫 `grow` method 時，則沒有填任何參數

>[!Info]
>在大部分其他 OOP 程式語言中，定義 instance method 時並沒有在第一個參數寫 `self` 的規則。因為大多數 OOP 程式語言中會有保留字 `this`，使用 `this.x` 即可存取 instance attribute `x`。

### Class Method

e.g.

```Python
class Dog:
    max_age = 10

    @classmethod
    def set_max_age(cls, age):
        cls.max_age = age
    
    @classmethod
    def evolve(cls):
        cls.set_max_age(cls.max_age + 10)

if __name__ == "__main__":
    d1, d2 = Dog(), Dog()

    Dog.set_max_age(20)
    print(d1.max_age, d2.max_age, Dog.max_age) # 20 20 20

    Dog.evolve()
    print(d1.max_age, d2.max_age, Dog.max_age) # 30 30 30
```

雖說 class method 是給 class 使用的 method，然而其實==在 Python 中也可以用 instance 呼叫 class method==，效果與用 class name 呼叫是一樣的。

###### `@classmethod` Decorator

每一個 class method 的開頭都必須使用 decorator `@classmethod`。

###### `cls` 參數

- 定義 class method 時，第一個參數固定用來代表 class 本身，通常被命名為 `cls`
- 擁有 `cls` 參數使得 class method 可以存取其他 class attributes/methods，比如上例中的 `cls.set_max_age(cls.max_age + 10)`
- 在 class 外呼叫 class method 時，==並不須要填入引數給 `cls`==，以上例而言，class `Dog` 呼叫 `set_max_age` method 時，只填入一個數字作為 `max_age`
- Class attributes 必須定義於 constructor method (`__init__`) 外面，通常是上面，也就是最開頭，並不用以 `cls.` 開頭，比如上例中的 `max_age = 10`

>[!Info]
>在大部分其他 OOP 程式語言中，定義 class method 時並沒有在第一個參數寫 `cls` 的規則。在 class 內，`Dog.x` 即表示 `Dog` class 的 class attribute `x`。

### Static Method

在 Python 中，static method 通常被用來做「不會存取到任合 class attribute、instance attribute、class method 與 instance method 的工作」，所以 static method 通常是 pure function。

其實 static method 也可以透過 `<CLASS_NAME>.` 的方式來存取 class attribute/class method/static method，事實上這樣一來 static method 可以做到所有 class method 做得到的事，但建議盡量避免避免將 static method 與 class method 混用，否則容易造成其他人的誤用。

e.g.

```Python
class Dog:
    max_age = 10
    
    @staticmethod
    def say_something(message):
        print(say_something)
    
    @staticmethod
    def say_hi():
        Dog.say_something("hi")

if __name__ == "__main__":
    Dog.say_hi()  # hi
    
    d = Dog()
    d.say_hi()  # hi
```

- 由上例可見，用 instance 呼叫 static method 也行得通
- 每一個 static method 的開頭都必須使用 decorator `@staticmethod` 裝飾之
- 與 class method 不同的是，定義 static method 時，沒有所謂「第一個參數固定用來代表 class 本身」的規則
- Static method 也可以在 class method 或 instance method 中被呼叫，其方法皆是 `<Class_name>.<static_method>()`

# 參考資料

- <https://www.tutorialspoint.com/class-method-vs-static-method-in-python>
