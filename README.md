# Spider

一些爬虫的实现。


### xmly.py 

喜马拉雅免费专辑下载爬虫，参数 `-a` 指定专辑id ， 类似如`https://www.ximalaya.com/yinyue/20248318/` 这种网址， 其中 `20248318` 就是专辑id；`-o` 指定排序，可选 `1` 或 `-1` 。

```bash
python3 xmly.py -a 20248318 -o 1
```

