#OOP 

SOLID Principles 是 Uncle Bob (Robert C. Martin) 在 2004 年整理的五個 OOP 設計原則的縮寫（但有些原則不是 Uncle Bob 自己提出的），它們分別是：

- [Single Responsibility Principle](<#Single Responsibility Principle>)
- [Open Closed Principle](<#Open Closed Principle>)
- [Liskov Substitution Principle](<#Liskov Substitution Principle>)
- [Interface Segregation Principle](<#Interface Segregation Principle>)
- [Dependency Inversion Principle](<#Dependency Iversion Principle>)

# Single Responsibility Principle

>一個 class 不應該同時為多個「角色」實作功能，應只對一個角色負責。

### 範例

一間公司裡有三種職位：`hr`、`accounting` 與 `engineer`，每個員工都有 `reviewPerformance` 與 `askForLeave` 兩個動作，不同職位的 `reviewPerformance` 方式不同，但他們 `askForLeave` 的方式都相同。

###### 錯誤做法

把所有邏輯都在 `Employee` 中實作，透過 if-else 來管理不同職位 `reviewPerformance` 的方法，這樣很容易讓整個 method 看起來又臭又長：

```TypeScript
class Employee {
  public reviewPerformance(title: "hr"|"accounting"|"engineer"): number {
    if (title === "hr") {
        // implement algorithm for hr
    } else if (title === "accounting") {
        // implement algorithm for accounting
    } else {
        // implement algorithm for engineer
    }
  }
  public askForLeave(): void {
    // implement algorithm for hr, accounting and engineer
  }
}
```

###### 建議做法

把每個職位獨立成一個 class，`Employee` class 拉成階層較高的 abstract class，只實作內容相同的部分（如 `askForLeave` method），其它交由各個繼承 `Employee` 的 class 實作：

```TypeScript
abstract class Employee {
  protected abstract reviewPerformance (): number;
  protected askForLeave (): void {
    // implement algorithm for hr, accounting and engineer
  }
}

class Hr extends Employee {
  protected reviewPerformance (): number {
    // implement algorithm
  }
}

class Accounting extends Employee {
  protected reviewPerformance (): number {
    // implement own algorithm
  }
}

class Engineer extends Employee {
  protected reviewPerformance (): number {
    // implement algorithm
  }
}
```

### 參考資料

- <https://medium.com/%E7%A8%8B%E5%BC%8F%E6%84%9B%E5%A5%BD%E8%80%85/c2c4bd9b4e79>
- <https://www.jyt0532.com/2020/03/18/srp/>

# Open-Closed Principle

>一個系統應該要可以擴充功能，且擴充功能時應不須要修改到既有功能的 code，也不用擔心既有的功能壞掉。

實務上的例子如 Google Chrome，你可以在上面安裝多個 plugins，這些 plugins 的開發者不須要修改到 Google Chrome 的底層程式碼就可以開發出各式各樣的 plugins。

### 參考資料

- <https://medium.com/%E7%A8%8B%E5%BC%8F%E6%84%9B%E5%A5%BD%E8%80%85/f7eaf921eb9c>
- <https://www.jyt0532.com/2020/03/19/ocp/>

# Liskov Substitution Principle

詳見 [[Liskov Substitution Principle]]。

### 重點摘要

- 若在可運行的函式（或程式碼片段）中，將任何型別為 $T$ 的物件替換成型別為 $S$ 的物件後，函式／程式碼片段應該仍然可以正常運行，則稱型別 $S$ 為型別 $T$ 的 subtype，或說 $T$ 為 $S$ 的 supertype
- ==Subtype 與 subclass 是兩個完全不相干的概念==，只有遵守特定規則來繼承，才會形成 subtype，否則就只是 subclass
- 當你想要使用繼承時要非常小心，因為==大多數的情況都不該用繼承==，繼承是所有依賴關係裡面最強的，而太過依賴總是沒啥好事

# Interface Segregation Principle

>Interface 不要定義地太過全面，因為不是大家都想實作你定義的所有 methods。反過來說，class 也不要隨便實作一些自己其實用不到的 interfaces。

### 參考資料

- <https://www.jyt0532.com/2020/03/23/isp/>

# Dependency Inversion Principle

>1. 表層模組不應依賴於底層模組，兩者都應依賴於 interface/abstract class。
>
>2. Interface/abstract class 不應依賴於具體實作，反而是具體實作應該依賴於 interface/abstract class。

### 何謂「依賴」？

想了解「依賴」(dependency) 的定義，可以參考 [[Dependency Injection]]，但請注意，dependency injection 與 dependency inversion principle 是不同的概念。

### 實現方式

[[Inversion of Control]] (IoC)

>[!Note]
>IoC 是一個比較廣義的概念，並不是所有形式的 IoC 都遵守 Dependency Inversion Principle。

### 參考資料

- <https://www.jyt0532.com/2020/03/24/dip/>
