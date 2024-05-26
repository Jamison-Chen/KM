#OOP 

- Static method/attribute 在大多數程式語言中都以 `static` 關鍵字來表示，又叫做 class mehtod/attribute
- Non-static method/attribute 則又叫做 intance method/attribute。

e.g.

```TypeScript
class A {
    public static x: nubmer = 4;  // static variable
    public y: number;  // instance variable

    public static f(): void {  // static method
        // ...
    }
    public g(): void {  // intance method
        // ...
    }
}
```



### Static Variables vs. Instance Variables

- Static variables 是所有 instances 共享的，instance variables 則是 instance 自己獨享

    Static variables 扮演的角色類似 non-OOP 中的 global variables，其作用域是整著 class 以及所有該 class 的 instances，也就是說，所有 instances 讀取到的 static variable 都是同一個記憶體位置（可以節省記憶體！）

- Static variables 的值可以直接透過 class 來存取，所以不建議使用 instance 來存取

    有些語言（如 TypeScript）甚至會直接在 compile 時就報錯，以開頭的 class `A` 為例：

    ```TypeScript
    const aa = new A();
    console.log(aa.x);  // Property 'x' does not exist on type 'A'. Did you mean to access the static member 'A.x' instead?
    ```

- Static variables 必須在定義 class 時就給予初始值，不會等到 constructor、甚至其他 method 中才給值（instance variables 則通常會等到 constructor 中才給值）

    錯誤示範：

    ```TypeScript
    class B {
        public static x;
        public constructor() {
            B.x = 0;
        }
    }
    ```

    在 TypeScript 中，因爲「沒有被初始化的變數的值都是 `undefined`」，所以這樣寫不會報錯，雖然如此，但這樣的 class 設計是不好的。
### Static Methods vs. Instance Methods

- Static methods 中只能存取 static variables/methods，不能存取 instance variables/methods；instance methods 中則沒有此限制

    錯誤示範：

    ```TypeScript
    class B {
        public a(): void {
            B.c();  // <= This is acceptable.
        }
        public static b(): void {
            this.a();  // <= You can't do this.
        }
        public static c(): void {
            // ...
        }
    }
    ```

- Static methods 可以直接透過 class 來呼叫，所以不建議使用 instance 呼叫

- Static methods 採取 **compile-time binding**，所以沒有所謂的 [method overriding](</Programming Language/OOP 四本柱.md#Override vs. Overload>)，取而代之的是 **Method Hiding**

    > [!Note] Compile-Time Binding
    >意思就是在 compile 時就已經決定好一個 class 在呼叫 static method 時實際上要執行由哪一段 code 所 compile 出來的 binary code。

    > [!Note] Method Hiding
    >和 method overriding 相似處在於，也是在 subclass 中出現一個 superclass 中已有的同名、且參數相同的 method；相異處在於，method overriding 的效果是在 run time 發生的（因為 instance 在 run time 才被生成），而 method hiding 的效果在 compile time 就已經發生了。
    
- 和 static variables 一樣，static methods 的記憶體位置也是固定且供所有 instances 共享的，所以相對於 instance methods 來說更省記憶體

# 參考資料

- <https://www.geeksforgeeks.org/static-methods-vs-instance-methods-java/>
