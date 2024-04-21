#AWS #WebDevPractice

- [官方文件](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/recognize-expanded-volume-linux.html)
- [影片](https://www.youtube.com/watch?v=smuSDWglwEs)

要加大 AWS EC2 instance 上的儲存空間 (EBS volume)，並不是單純透過 UI 修改 storage volume 的配置就好，還須要到主機內使用指令擴展 file system 的大小，否則修改後的儲存空間並不會真實反映到 file system 上。

整個修改 sotorage volume 的流程大致如下：

- Step1: 到 AWS console 透過 UI 修改修改配置給你的 EC2 instance 的 storage volume
- Step2: 等待 Volume state 從 modifying 變成 In-use（大概要等三到五分鐘）
- Step3: 到 [AWS CloudShell](https://console.aws.amazon.com/cloudshell) 輸入指令查詢你的 EC2 instance type（分為 nitro-based 跟 xen-based）
- Step4: SSH 至 EC2 主機
- Step5: 使用指令將 disk partition 擴展
- Step6: 使用指令將 file  system 擴展（須注意 file system type）
