            __________              ____  __    __
           /  __  __  \____  ____  / __ \/ /   / /
          /  / / / /  / __ \/  __\/ /_/ / /___/ /
         /  / / / /  / /_/ /  /  /  ___/  ___  /
         \_/  \/  \_/\____/\_/   \_/   \_/  /_/

  By Walkerfuz of Taurus Security(github.com/walkerfuz)
                                  Morph - Version 0.2.1
=====================================================================================

@PCanyi: Fuzz的关键在于好的变异引擎，有效的监控器，以及稳定的生成器。


开发历史
========

v0.2.1 2015/12/3
	   优化了Fuzzer插件的编写格式 分为morph_random morph_fuzz morph_notify_href三部分
	   解决了连续两个样本存在Crash时Morph序号读取死循环的错误
       优化了样本重现时的对WebSockets有依赖的逻辑
	   在Readme中增加了关闭Firefox安全模式的方法

v0.2.0 2015/12/2
       全面改写为静态Fuzz框架 采用file:///本地打开网页进行Fuzz
	   解决了IE因Internet和Intranet权限不同导致Morph对某些Crash并不能引起崩溃的bug

V0.1.5 2015/11/6
       解决了Subprocess.Popen出现OSError WinError 1455的错误
       解决了MSECExtentions v1.6.0插件在Windbg中出现Can't load Library的错误

v0.1.4 优化core/psutil全部采用yield生成器
       消除了hProcess句柄没有关闭的隐患
	   增加了WebServer端404返回标志

v0.1.3 增加了t_m.isAlive判断监控进程是否真正结束的标志
       解决了log.txt没有生成引起open打开文件失败的异常提示

v0.1.2 解决了Process32First和Process32Next返回值不等同于Python False对象类型错误的bug
       将while True循环修改为while 1
       增加了每次重现后log文件的删除

v0.1.1 解决了threading.join超时后监控CrashProc的Monitor子线程没有结束的bug

v0.1.0 解决了浏览器标签页无响应阻塞Fuzz循环继续进行的bug


使用前准备
==========
1. 安装Windbgx86 or Windbgx64。
   下载MSECExtensions插件放在Windbg的winext文件夹，并打开Windbg测试load msec.dll是否成功，若出现Can't Load Library的错误，则需要安装Visual C++ Redistributable for Visual Studio 2008/2012。
   注意：MSECExtensions1.6.0需要VC++2012运行时环境支持。

2. 将Windbg程序文件夹下的cdb.exe设置为默认JIT即时调试器：
   >cdb.exe -iaec "-logo c:/log.txt -c \"!load msec.dll;!exploitable -v;\""
   注意：c:/log.txt与config.py中的Debugger中的log参数必须一致

3.如果Fuzz模板是Firefox，则需要关闭安全模式
  在firefox进入about:config找到toolkit.startup.max_resumed_crashes（默认是3），将其设置为-1即可关闭Safe Mode。
  另外需要在Firefox选项-->隐私-->选择'不记录历史' 关闭Firefox的历史记录功能

4.采用Windbg目录下自带的gflags.exe开启模板进程的页堆调试功能，比如IE浏览器：
  >Gflags.exe /i iexplore.exe +hpa

5.下载Morph并配置Config.py中的默认参数。

6.运行：
  >morph.py --browser=IE --fuzzer=nduja.html

备注信息
========

1. 取消JIT即时调试器指定：
	删除
	x86: HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\AeDebug
	和
	x64: HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\Microsoft\Windows NT\CurrentVersion\AeDebug
	项下的
	Debugger 和Auto键值

TODO事项
========

P1. 检查Windbg、MSECExtensions和VC++运行时环境（必须匹配）合法性

P2. Crash文件夹创建IE11等浏览器版本子文件夹

P3. 每个Fuzzer整合为1个文件夹

P4. 增加Http协议支持，优化Fuzz效率
