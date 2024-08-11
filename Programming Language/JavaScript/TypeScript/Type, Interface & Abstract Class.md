# Type vs. Interface

有時後 `inteface` 與 `type` 可以達到一樣的效果，比如：

```TypeScript
interface Child {
  name: string;
  age: number;
  height: number;
  weight: number;
  getBMI(): number;
}

type Child = {
  name: string;
  age: number;
  height: number;
  weight: number;
  getBMI(): number;
}
```

- Class 可以 implements interface 也可以 implements type

### `interface` 做得到但 `type` 做不到的事

##### Declaration Merging

同一個檔案中，多個同名的 interfaces 的定義會自動被 merge，但同一個檔案中不能重複定義同名的 type。

e.g.

```TypeScript
interface Person {
  name: string;
}
interface Person {
  age: number
}

const p: Person = {
  name: "Alice",
  age: 18
}
```

##### Extending Class

Interface 可以 extends class、type、interface，但 type 不能 extend 任何東西。

e.g.

```TypeScript
class Animal {
  public name: string;
  
  constructor(name: string) {
    this.name = name;
  }
}

interface Dog extends Animal {
  breed: string;
}

const myDog: Dog = {
  name: "Buddy",
  breed: "Golden Retriever",
};
```

>[!Note]
>Interface 甚至可以 extends 多個 classes、interfaces 與 types（反之，一個 class 只能 extends 最多一個 class）。

### `type` 做得到但 `interface` 做不到的事

##### And/Or Operation

type 可以是多個 types/interfaces 進行聯集或交集後的結果，但定義一個 interface 時不能這麼做。

e.g.

```TypeScript
type a = 1 | 2 | 3;
type b = 2 | 3 | 4;
type c = a & b;

const num: c = 3;
```

##### Utility Types

詳見[官方文件](https://www.typescriptlang.org/docs/handbook/utility-types.html)。

##### Tuple Type

詳見[實用的 Typing 小技巧#Literal Tuple Type](</Programming Language/JavaScript/TypeScript/實用的 Typing 小技巧.md#Literal Tuple Type>)。

##### Mapped Type

詳見[實用的 Typing 小技巧#Mapped Type](</Programming Language/JavaScript/TypeScript/實用的 Typing 小技巧.md#Mapped Type>)。

##### Conditional Type

e.g.

```TypeScript
type MessageType<T> = T extends string ? string : number;
```

# Interface

e.g.

```TypeScript
interface Child {
  name: string;
  age: number;
  height: number;
  weight: number;
  getBMI(): number;
}

class Human implements Child {
  public constructor(
    public name: string,
    public age: number,
    public height: number,
    public weight: number
  ) {}

  public getBMI(): number {
    return this.weight / Math.pow(this.height, 2);
  }
}
```

### 特色

- 一個 class 可以 implements 多個 interfaces
- 定義 interface 時，attributs/methods 前面不能加上 `public`、`protected` 或 `private`，因為一定是 `public`
- 當 class A implements interface B 時，A 一定要實作所有 B 定義的 methods，以及 assign value 給 B 定義的 attributes

# Abstract Class

e.g.

```TypeScript
abstract class Child {
  public constructor(
    public name: string,
    public age: number,
    public height: number,
    public weight: number
  ) {}

  public abstract getBMI(): number;
}

class Human extends Child {
  public constructor(
    public name: string,
    public age: number,
    public height: number,
    public weight: number,
    public surname: string
  ) {
    super(name, age, height,weight)
  }

  public getBMI(): number {
    return this.weight / Math.pow(this.height, 2);
  }
}
```

### 特色

- 一個 class 只能 extends 最多一個 abstract class
- 定義 abstract class 時，可以在 attributes/methods 前加上 `public`、`protected` 或 `private`
- Abstract class 裡可以有沒有值的 abstract attributes、沒有實作的 abstract methods，也可以有有值的 concrete attributes 與已實作的 concrete methods

# 參考資料

- <https://blog.logrocket.com/types-vs-interfaces-typescript/>
- <https://hrishikeshpathak.com/blog/interface-vs-abstract-class-typescript/>
