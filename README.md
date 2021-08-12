# Bilibili-Danmaku-Auto-Report
<p align="center">
    <img src="https://user-images.githubusercontent.com/52315359/128585311-62d13a2f-efc2-4ed6-99ce-0264274a28f4.png" width="200" height="200">
</p>
<h4 align="center" style="italic">b站或许会倒闭，但_________。</h4>

 ## Usage
 report a specific kind of danmaku automatically

 ## How to use
 1. install all the requirements with `requirements.txt`
 2. set rules in regex expression in `rule.txt`
 3. run `danmaku.py`

 ## Configure Application 
 To configure app, go to `rule.txt` to set the key words

 for example:
 ```
 蒙古上单|陈rui|变味|倒闭|后浪
 ```
 then if a danmaku looks like this:
 ```
 陈rui，你女马什么时候死啊？？？
 ```
 it will be reported by the program automatically.

 \* supports regex expression!!

 ## Notes:
 If a danmaku matches the rule, the program can find who sent 
 it and get his user level 
 so that you can check if the result 
 is wrong. 

 The result will be in `result.xls`.

 ## Other
 Using the hash decrypt method from hash decrypt from [Aruelius/crc32-crack](https://github.com/Aruelius/crc32-crack)

 Using the bilibili api docs by [SocialSisterYi](https://github.com/SocialSisterYi/bilibili-API-collect)

 Using MIT license.
 
 Older version: [link](https://github.com/Creeper2333/Bilibili-Danmaku-Search-Uid)  PS:disabled.
