# Yangtzeu_lib
library seat of Yangtze University

[toc]

## 安装python

如果你已安装python请忽略。

如果你未安装python，你需要向我询问安装包，弹出以下画面。

![install_python](https://image-1314205794.cos.ap-chengdu.myqcloud.com/install_python.png)

首先，我们需要勾选左下方的 ’Add python.exe to PATH’ ,之后点击 ‘install now’。然后等待加载完成，我们就完成了python的安装。

## 安装所需python库

这里我们需要安装python的第三方库：requests，lxml，selenium。

如何安装呢？我们只需双击解压包中的 ‘install_pakage.py’。

待其输出了三行 ‘pakage of * was installed!!!’ 时，我们就已经完成了第三方库的安装。

## webdriver获取

首先我们需要知道你的edge浏览器的版本。如下操作：打开edge浏览器——>菜单——>帮助与反馈——>关于Microsoft Edge。

我们会看到如下界面，

![edege](https://image-1314205794.cos.ap-chengdu.myqcloud.com/edege.png)

记住它的版本号与位数，打开网址：[mswebdriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)

下载对应版本与位数的webdriver，并将下载的文件解压，找到 ‘msedgedriver.exe’ 文件复制到本解压包文件目录下。若遇到提示则选择覆盖。

**注：若你的Edge浏览器的版本与我的一样，则可以跳过本步骤**



## 修改所需信息

这里我进行了简化操作。

**修改账密：**双击解压包中的 ‘users_setting.py’ ，根据提示填写账密后关闭窗口。

**修改预约信息：**双击解压包中的 ‘setting.py’ ，根据提示填写账密后关闭窗口。

**注：预约开始时间和预约结束时间需要注意格式，例：7:00需写为7；18:30需写为18.5**

## 定时运行

windows自带了定时运行的程序：任务计划程序

下面开始介绍如何创建定时任务…

首先，我们需要找到它。

![find_wait_time_program](https://image-1314205794.cos.ap-chengdu.myqcloud.com/find_wait_time_program.png)

如上图，在状态栏点击搜索，并输入‘任务计划程序’，回车， 我们就打开了任务计划程序。

![wait_time_program](https://image-1314205794.cos.ap-chengdu.myqcloud.com/wait_time_program.png)

然后，我们需要点击右侧方框中的 ‘创建任务…’，之后就会弹出以下弹窗。

![create_plan](https://image-1314205794.cos.ap-chengdu.myqcloud.com/create_plan.png)

我们在名称处输入一个任务名称。输入完成后，我们再点击 ‘触发器’ 按钮。

![flip_flop_page](https://image-1314205794.cos.ap-chengdu.myqcloud.com/flip_flop_page.png)

这里我们需要添加一个触发器，我们点击 ‘新建’ 。

![flip_flop](https://image-1314205794.cos.ap-chengdu.myqcloud.com/flip_flop.png)

按上图所示进行设置后，点击确定。

我们再点击 ‘操作’ 按钮。

![operation_page](https://image-1314205794.cos.ap-chengdu.myqcloud.com/operation_page.png)

再次新建，在程序或脚本框需要输入python.exe所在的路径。其默认路径为：C:\Users\Administrator\AppData\Local\Programs\Python\Python311\python.exe

![create_operation](https://image-1314205794.cos.ap-chengdu.myqcloud.com/create_operation.png)

在添加参数框输入 ‘Yangtzeu_lib_5.py’ 的所在路径。

下面讲解怎么获取该文件的路径，我们需要: 单击该文件——>右键单击——>属性——>安全，之后会出现以下画面。

![get_path](https://image-1314205794.cos.ap-chengdu.myqcloud.com/get_path.png)

我们复制对象名称，这样我们就获取到了该文件的所在路径。

我们将其粘贴到 ‘添加参数’ 框。

**之后，我们还需要填写 ’起始于‘ 输入框，我们需要输入解压包文件夹的路径，与文件路径类似。**

**文件夹路径示例：C:\Users\Administrator\Desktop\本地化cookie版**

最后我们点击确定，我们就完成了定时任务的设置。

## 结束语

终于，写完了。设置完成后，我们就可以不用每天为图书馆抢不到座而忧愁了>__<
