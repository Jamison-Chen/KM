要加大 AWS EC2 instance 上的儲存空間 (storage volume)，並不是單純透過 UI 修改 storage volume 的配置就好，還須要到主機內使用指令擴展 file system 的大小，否則修改後的儲存空間並不會真實反映到 file system 上。

整個修改 sotorage volume 的流程大致如下圖：

- Step1: 到 AWS console 透過 UI 修改修改配置給你的 EC2 instance 的 storage volume
- Step2: 等待 Volume state 從 modifying 變成 In-use（大概要等三到五分鐘）
- Step2: SSH 至 EC2 主機
- Step3: #TODO 

# 參考資料

- [官方文件](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/recognize-expanded-volume-linux.html)
- <https://www.youtube.com/watch?v=smuSDWglwEs>
