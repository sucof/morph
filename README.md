# About

Morph is an open source browser fuzzing framework written by Walkerfuz of Taurus Security.

It provides an automated way to fuzz a browser, like IE, Firefox, Chrome, etc.

You can write yourself fuzzer for morph, for example nduja, fileja, cross_fuzz.

### Features

* 支持多种浏览器，例如IE、Chrome、Firefox等
* 支持自定义扩展插件，比如nduja、fileja、cross_fuz

### Requirements

* Python >= 3.4

### Installation and Usage

1.安装Windbgx86/x64和MSECExtensions !exploitable插件。

> 注意：需要在Windbg中提前测试load msec.dll是否成功，若出现Can't Load Library的错误，则需要安装Visual C++ Redistributable 2008/2012。


2.将Windbg目录下的cdb.exe设置为默认即时调试器：

> cdb.exe -iaec "-logo c:/log.txt -c \"!load msec.dll;!exploitable -v;\""

其中命令中的c:/log.txt与config.py中的Debugger中的log参数必须一致。

3.如果Fuzz目标是Firefox，则需要关闭安全模式
> 在firefox进入about:config找到toolkit.startup.max_resumed_crashes（默认是3），将其设置为-1

4.采用Windbg目录下的gflags.exe开启目标进程的页堆调试功能，比如IE浏览器：

> gflags.exe /i iexplore.exe +hpa

5.下载Morph并配置Config.py中的参数。

6.运行：
> morph.py --browser=IE --fuzzer=nduja.html

### Versions Timeline

* v0.2.1
	* 优化了Fuzzer插件的编写格式，将其分为morph_random、morph_fuzz和morph_notify_href三部分
	* 解决了连续两个样本存在Crash时Morph序号读取死循环的错误
    * 优化了样本重现时的对WebSockets有依赖的逻辑
	* 增加了关闭Firefox安全模式的方法
* v0.2.0
	* 全面改写为静态Fuzz框架 采用file:///本地打开网页进行Fuzz
* v0.1.5
	* 解决了MSECExtentions v1.6.0插件在Windbg中出现Can't load Library的错误
* v0.1.3
	* 增加了t_m.isAlive判断监控进程是否真正结束的标志
* v0.1.2
	* 解决了Process32First和Process32Next返回值不等同于Python False对象类型引起的bug
* v0.1.1
	* 解决了threading.join超时后监控CrashProc的Monitor子线程没有结束的bug
* v0.1.0
	* 解决了浏览器标签页无响应阻塞Fuzz循环继续进行的bug

如果有什么bug或建议，请邮件联系@walkerfuz。
