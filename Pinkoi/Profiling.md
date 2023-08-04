[Pinkoi 文件](https://paper.dropbox.com/doc/Profiling--B6_BsreINkDPjQsYSmtwSMPiAg-e2Gvadg5BAsgu4pujb0Qw)

# At Local

```bash
cd ~/pinkoi
make tunnel
make shell

cd ./pinkoi/scripts

python debug_url.py /apiv2/app/get_product -q "{\"tid\": \"qnN4MJhY\"}" -p get_product_jamison.pstats

gprof2dot -f pstats get_product_jamison.pstats | dot -T svg -o get_product_jamison.svg
```

# At Staging

### Step1: 在 Staging 跑 Profiling

```bash
ssh staging
cd ~/pinkoi/pinkoi/
make shell

cd ./pinkoi/scripts

# 以 get_product API 為例
python debug_url.py /apiv2/app/get_product -q "{\"tid\": \"42bbieHG\"}" -p my_profiling.pstats

gprof2dot -f pstats my_profiling.pstats | dot -T svg -o my_profiling.svg
exit
```

### Step2: 在 Local `scp` Staging 的檔案

```bash
scp jamisonchen@staging:./pinkoi/pinkoi/scripts/my_profiling.svg ~/Desktop
```
