SOLID Principles 是 Uncle Bob (Robert C. Martin) 在 2004 年整理的五個軟體設計原則的縮寫（但有些原則不是 Uncle Bob 自己提出的），它們分別是：

- [Single Responsibility Principle](<#Single Responsibility Principle>)
- [Open Closed Principle](<#Open Closed Principle>)
- [Liskov Substitution Principle](<#Liskov Substitution Principle>)
- [Interface Segregation Principle](<#Interface Segregation Principle>)
- [Dependency Inversion Principle](<#Dependency Iversion Principle>)

# Single Responsibility Principle

>一個 class 不應該同時為多個「角色」實作功能，應只對一個角色負責。

### 範例

一間公司裡有三種職位：`hr`、`accounting` 與 `engineer`，每個員工都有 `reviewPerformance` 與 `askForLeave` 兩個動作，其中不同職位的 `reviewPerformance` 方式不同，但他們 `askForLeave` 的方式都相同。

###### 錯誤做法

把所有邏輯都在 `Employee` 中實作，透過 if-else 來管理不同職位 `reviewPerformance` 的方法，這樣很容易讓個 method 看起來又臭又長：

```TypeScript
class Employee {
  public reviewPerformance(title: "hr"|"accounting"|"engineer"): number {
    if (title === "hr") {
        // implement algorithm for hr
    } else if (title === "accounting") {
        // implement algorithm for accounting
    } else {
        /// implement algorithm for engineer
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

# Open Closed Principle

>一個

# Liskov Substitution Principle

# Interface Segregation Principle

# Dependency Iversion Principle

# 參考資料

- <https://khalilstemmler.com/articles/solid-principles/solid-typescript/>
