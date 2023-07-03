[內部文件](https://paper.dropbox.com/doc/Peewee--B65qsfklx2_PBCzkbUWkP4TXAg-LcYA12VdZMHpzBN31nXJy)

### 生成整個 Database 中所有 Tables 的 Models

```bash
python pinkoi/scripts/willchang/pwiz.py
```

### 生成指定 Table 的 Model

```bash
python pinkoi/scripts/will_chang/pwiz.py -t <TABLE_NAME>
```

# Some Details

- Model 要繼承 `BasePeeWeeModel` instead of  `peewee.Model`
- Timestamp 型態的 field 要使用 `MysqlTimestampField` instead of `peewee.DateTimeField`
