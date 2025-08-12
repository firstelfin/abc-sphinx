# abc-sphinx
abc代码渲染扩展,适用于sphinx渲染乐谱代码

## 安装

```
pip install abcSphinx
```

## 使用

在`conf.py`中添加以下内容：

```python
extensions = [
    'abcSphinx'
]
```

然后在rst文件中使用以下语法：

```
.. abc::

    X: 24
    T: 欢乐颂
    C: Paul Rosen
    S: Copyright 2005, Paul Rosen
    M: 6/8
    L: 1/8
    Q: 3/8=116
    R: Creepy Jig
    K: Em
    |:"Em"EEE E2G|"C7"_B2A G2F|"Em"EEE E2G|\
    "C7"_B2A "B7"=B3|"Em"EEE E2G|
    "C7"_B2A G2F|"Em"GFE "D (Bm7)"F2D|\
    "Em"E3-E3:|2"Em"E3-E2B|:"Em"e2e gfe|
    "G"g2ab3|"Em"gfeg2e|"D"fedB2A|"Em"e2e gfe|\
    "G"g2ab3|"Em"gfe"D"f2d|"Em"e3-e3:|
```

注意在rst文件中，`.. abc::`下一行要接一个空行, 否则代码段不识别。

## sphinx案例

快速搭建一个sphinx项目：

```shell
$ sphinx-quickstart docs
欢迎使用 Sphinx 8.2.3 快速配置工具。

请输入接下来各项设定的值（如果方括号中指定了默认值，直接
按回车即可使用默认值）。

已选择根路径：docs

有两种方式来设置用于放置 Sphinx 输出的构建目录：
一是在根路径下创建“_build”目录，二是在根路径下创建“source”
和“build”两个独立的目录。
> 独立的源文件和构建目录（y/n） [n]: y

项目名称将会出现在文档的许多地方。
> 项目名称: abc-test
> 作者名称: elfin
> 项目发行版本 []: 1.0

如果用英语以外的语言编写文档，
你可以在此按语言代码选择语种。
Sphinx 会把内置文本翻译成相应语言的版本。

支持的语言代码列表见：
https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-language。
> 项目语种 [en]: zh_CN

正在创建文件 /Users/elfin/project/abc-test/docs/source/conf.py。
正在创建文件 /Users/elfin/project/abc-test/docs/source/index.rst。
正在创建文件 /Users/elfin/project/abc-test/docs/Makefile。
正在创建文件 /Users/elfin/project/abc-test/docs/make.bat。

完成：已创建初始目录结构。
```

**书写rst文件：**

在source文件夹内写music/music.rst文件，内容如下：

```
music test in rst
=========================


.. abc::
    
    X: 24
    T: 欢乐颂
    C: Paul Rosen
    S: Copyright 2005, Paul Rosen
    M: 6/8
    L: 1/8
    Q: 3/8=116
    R: Creepy Jig
    K: Em
    |:"Em"EEE E2G|"C7"_B2A G2F|"Em"EEE E2G|\
    "C7"_B2A "B7"=B3|"Em"EEE E2G|
    "C7"_B2A G2F|"Em"GFE "D (Bm7)"F2D|\
    "Em"E3-E3:|2"Em"E3-E2B|:"Em"e2e gfe|
    "G"g2ab3|"Em"gfeg2e|"D"fedB2A|"Em"e2e gfe|\
    "G"g2ab3|"Em"gfe"D"f2d|"Em"e3-e3:|
```

在index.rst文件中添加以下内容：

```
.. toctree::
   :maxdepth: 2
   :caption: Contents:

    music/music
```

**配置conf.py文件：**

```python
# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'abc-test'
copyright = '2025, elfin'
author = 'elfin'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'abcSphinx'
]

templates_path = ['_templates']
exclude_patterns = []

language = 'zh_CN'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
# html_extra_path = ['_abc_images']  # 配置项

abc_global_classes = ["music-sheet", "responsive"]
abc_force_rebuild = True 

```

**构建文档：**

```shell
$ cd docs
$ make clean html
```

**查看效果：**
```
$ cd docs/build/html
$ python -m http.server 8000
```

打开浏览器，访问