# Spider

一些爬虫的实现。


### xmly.py 

喜马拉雅免费专辑下载爬虫，参数 `-a` 指定专辑id ， 类似如`https://www.ximalaya.com/yinyue/20248318/` 这种网址， 其中 `20248318` 就是专辑id；`-o` 指定排序，可选 `1` 或 `-1` 。

```bash
python3 xmly.py -a 20248318 -o 1
```

由于喜马拉雅下载的音频文件为 `m4a` 格式，故在这里提供一个 `shell` 脚本，转换为通用的 `mp3` 文件。该脚本依赖于 `ffmpeg`， 请先安装该依赖。`ubuntu` 下可使用下面命令安装：

```bash
sudo apt install ffmpeg
```

命令下，手动转换命令为：

```bash
ffmpeg -i mangzhong.m4a -acodec mp3 -ac 2 -ab 192k mangzhong.mp3
```

使用 `m4a2mp3` 脚本批量处理文件夹的命令为：

```bash
sudo ./m4a2mp3 /path/to/m4a/audio/files/directory/
```

参考资料：

- https://github.com/i-sync/ximalaya
- https://github.com/haensl/m4a2mp3
- https://ffmpeg.org/download.html
- https://github.com/feixiao/ffmpeg
- https://github.com/wks/chineseid3fix