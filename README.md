## UCAS 课程网站批量下载课件脚本

### 0. 脚本目的
- 由于课程网站不支持批量下载，当老师上传课程材料较多时，如大量的论文等，手动点击下载耗时费力。 

- 本脚本**仅用于**批量下载课件，以及相关课程资料。

- 本脚本对比了国科大另一学长开源的[UCAS课件批量下载脚本](https://blog.csdn.net/lusongno1/article/details/79995009)，他的脚本主要基于 **requests 模块**，特点是速度快，但是一旦更改网站的URL以及关于Cookie等信息，该脚本会失效；本脚本主要基于 **Selenium 模块**，特点是速度较 requests 慢，但是可见即可爬，若网站前端代码进行修改，也有可能会失效。

  

### 1. 环境搭建

**1. 编码环境**
- Python 3.7
- MacOS

**2. 浏览器环境**

- Mac 版本的 Chrome 浏览器，若未下载 Chrome 浏览器，可点击[官方链接](https://www.google.com/chrome/)下载。

- 编码、测试时使用 Chrome 版本为 V 74.0.3729.169。

**3. 浏览器驱动环境配置**

- 本代码基于自动测试工具 [Selenium](https://www.seleniumhq.org) 进行编写，因此需要安装相应的 Chrome 浏览器驱动，可于[官方链接](http://chromedriver.chromium.org)下载与浏览器对应的版本。

**4. 配置环境测试**

- 请打开 Python IDE 进行测试环境是否搭建成功，测试代码如下：

```python
from selenium import webdriver

browser = webdriver.Chrome
browser.get("https://www.baidu.com")
browser.close()
```

- 若成功打开了 Chrome 浏览器，并访问"百度"的网址成功，最后关闭浏览器，则说明环境搭建成功。
- 若测试代码无法运行，请检查环境搭建问题（请 Baidu / Google）。

**5. 安装相应的package**

```pip
pip install beautifulsoup4
```

or

```
pip3 install beautifulsoup4
```



#### 2. 代码说明

**Download_Chrome.py 思路**  

1） 使用 Selenium 打开具有一定配置的 Chrome 浏览器；

2）Login；

3）进入课程网站；

4）列出所有课程；

5）选择课程；

6）选择该课程的资源；

7）下载与文件整理；

8）Logout。



#### 3. License

```
MIT License

Copyright (c) 2019 Yantong Lai

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

