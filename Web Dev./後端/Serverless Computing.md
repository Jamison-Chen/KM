Serverless 不是字面上沒有 server 的意思，沒有什麼服務是不需要 server 就可以運作的，這個詞在這裡真正的意思是：

>開發者可以專注於開發，不用處理與 server 相關的事情（configure、deploy、maintain）。

為什麼可以不用處理與 server 相關的事情呢？因為雲端服務供應商會幫你把這些事情處理好。

三大雲端服務供應商都有提供 serverless computing 的服務，它們的名稱如下：

- AWS Lambda
- Microsoft Azure Functions
- Google Cloud Functions

這些服務被歸類為 **FaaS (function as a service)**，它們都有一個共同點：

>Server 只會在使用者呼叫 funcitons 時才動起來。

這使得：

- 服務收取的費用由 function 的使用量決定
- 若太久沒 call function，則下一次 call function 時須要多等一段 server wake-up 的時間
