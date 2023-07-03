[Pinkoi 文件](https://paper.dropbox.com/doc/Profiling--B6_BsreINkDPjQsYSmtwSMPiAg-e2Gvadg5BAsgu4pujb0Qw)

# Profile & Visualize

e.g.

```bash
make shell

cd ./pinkoi/scripts

python debug_url.py /apiv2/app/get_product -q "{\"tid\": \"qnN4MJhY\"}" -p get_product_jamison.pstats

gprof2dot -f pstats get_product_jamison.pstats | dot -T svg -o get_product_jamison.svg
```
