# subtitle-fixer
一个用于修正视频字母不同步的小工具,目前只实现了ass格式的,别的格式暂时不打算支持,当然如果愿意帮我加上对别的格式的支持我也表示欢迎.
功能包括一下几个:
* 修正字幕启示时间
* 修正字幕播放速度

###用法:
```bash
subtitle-fixer [options] -i input -o output
```
###参数列表:
```
	--encode=文件编码				设置文件编码(默认utf-8)
	--help                         显示帮助
	--offset=时间偏移量			调整字幕起始时间
	--speed=倍率					调整字幕播放速度
		--speed=视频中时间/字幕中时间
```
时间的格式按照"时:分:秒:百分数"
##关于如何支持其他的格式
在analyser目录下下派生analyser类就可以支持其他格式,具体可以看analyser.py和ass.py应该很好懂.
