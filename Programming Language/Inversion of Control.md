### 實現 IoC 的手段

- [[Dependency Injection]]
- [Service Locator Pattern](<#Service Locator Pattern>)
- [[Template Method|Template Method Pattern]]

### IoC 的目的 - 解耦 (Loose Coupling)

# Service Locator Pattern

以「人開車」為例（請先看 [[Dependency Injection#以「人開車」為例|Dependency Injection 中的這段]]）：

```TypeScript
interface Car {
    run(): void;
}

class Toyota implements Car {
    public run(): void {
        // ...
    }
}

class Tesla implements Car {
    public run(): void {
        // ...
    }
}

class CarLocator {
    public static car: Car = new Toyota();
}

class Person {
    private car: Car;
    public constructor() {
        this.car = CarLocator.car;
    }
    public drive(): void {
        this.car.run();
    }
}

const a = new Person();

CarLocator.car = new Tesla();
const b = new Person();
```

### Service Locator Pattern 的缺點

Code 的可讀性可能會比較低，因為 service locator 就像是全域變數，表層模組的 instance 的建立位置並不一定會緊跟在 service locator 的值更改之後。

以上例來說，並不是所有時候 `const b = new Person();` 都會緊跟在 `CarLocator.car = new Tesla();` 後面，所以當你想知道現在 `new Person()` 所開的 `Car` 是什麼，就要往前追到最近一次 `CarLocator.car` 的值更改時才知道。
