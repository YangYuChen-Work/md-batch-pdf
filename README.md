# md2pdf — 极简 Markdown 批量转 PDF 工具

> 把 `.md` 文件扔进 `Input/` 文件夹，双击脚本，PDF 自动出现在 `Output/`。什么都不用配置。

---

## 这是什么

写文档、做笔记、整理知识库的时候，经常需要把 Markdown 文件转成 PDF 分享给同事、打印或者存档。手动一个一个打开再"另存为 PDF"太痛苦了。

这个小工具就是干这个的——**批量、一键、无脑操作**。你把所有 `.md` 文件丢进 `Input` 文件夹，双击一个脚本，等几秒钟，干净漂亮的 PDF 就整整齐齐地躺在 `Output` 文件夹里了。

生成的 PDF 是 **GitHub 风格**的：白底黑字、代码块有语法高亮、表格有边框条纹、链接可以点击——就跟你在 GitHub 上看到的 README 差不多。

---

## 你需要准备的

**唯一的前提条件：Python 3.8 或以上版本。**

为什么需要 Python？因为 Python 负责把 Markdown 语法"翻译"成浏览器能懂的 HTML 网页，这个翻译过程需要用到 Python。

- **如果你还没装 Python**：去 [python.org](https://www.python.org/downloads/) 下载最新版，安装时**一定要勾选** "Add Python to PATH" 这个选项（在安装器第一屏最下面）。
- **如果你不确定装没装**：打开 CMD（Win+R 输入 `cmd` 回车），输入 `python --version`，如果能显示版本号就说明有了。

**除此之外，什么都不用装。** 不用装字体、不用装浏览器、不用装任何奇怪的依赖。你的电脑自带的 Edge 或 Chrome 浏览器就够用了。

---

## 怎么用

### Windows（推荐）

```
1. 把要转换的 .md 文件放入 Input 文件夹
2. 双击 run.bat
3. 去 Output 文件夹拿 PDF
```

第一次运行会停顿几秒（自动安装 Python 依赖），之后就是秒转。

### Mac / Linux

```
1. 把要转换的 .md 文件放入 Input 文件夹
2. 打开终端，cd 到项目目录，运行 bash run.sh
3. 去 Output 文件夹拿 PDF
```

第一次运行同理，会自动装好依赖。

---

## 效果展示

转换出来的 PDF 长什么样：

- 标题有层级（h1 有下划线分隔，h2 也有）
- 代码块有深灰背景 + 语法高亮（Python、JS、Java、Go 等语言自动识别）
- 表格有边框 + 交替行颜色
- 引用有左侧灰色竖条
- 列表、图片、链接都能正常显示
- **中文完美显示**，不会变成方块或乱码

---

## 进阶用法

### 子文件夹也支持

`Input/` 里面可以建子文件夹，结构会被原样复制到 `Output/`：

```
Input/
├── 需求文档/
│   ├── v1.0.md
│   └── v2.0.md
└── 技术方案/
    └── 架构设计.md

→ 转换后 →

Output/
├── 需求文档/
│   ├── v1.0.pdf
│   └── v2.0.pdf
└── 技术方案/
    └── 架构设计.pdf
```

### 每次用之前清一下 Output

为了避免旧文件混淆，建议每次批量转换前，把 `Output/` 文件夹清空。

---

## 常见问题

**Q: 双击 run.bat 闪退怎么办？**

A: 最可能的原因是没有装 Python，或者装了但没勾选 "Add to PATH"。重新运行 Python 安装器，选"Modify"，确保勾上 PATH 那个选项。然后重开一个新的 CMD 窗口，用 `python --version` 确认能找到。

**Q: 为什么会弹出一个浏览器窗口？**

A: 不会。工具用的是浏览器"无头模式"（headless mode），在后台静默运行，不会弹出窗口。

**Q: 转换出来的 PDF 没有中文，都是方块？**

A: 不应该。工具用的是系统自带的 Edge/Chrome 浏览器来渲染，这些浏览器天生支持中文。如果你确实遇到了，请提 Issue 并附上你的系统版本和浏览器版本。

**Q: Mac 上能用吗？Linux 上呢？**

A: 都能用。Mac 上需要系统有 Chrome 或 Edge（大多数机器都有），Linux 上需要 `google-chrome` 或 `chromium-browser`。如果没有，`sudo apt install chromium-browser` 装一个就行。

**Q: PDF 的样式能自定义吗？**

A: 可以。打开 `md2pdf.py`，找到 `CSS = """` 开头的那一大段，改里面的 CSS 就行。如果你懂前端的话，这就是普通的网页样式表。

---

## 原理简述

```
你的 .md 文件
    ↓  (Python: markdown 库翻译)
一个带 CSS 样式的 .html 网页
    ↓  (系统浏览器 Edge/Chrome 静默打开)
浏览器把网页"打印"成 PDF
    ↓
Output/ 里的 .pdf 文件
```

分两步走：
1. **Python** 负责 Markdown → HTML 的转换和代码语法高亮（用的是 `markdown` 和 `pygments` 两个库）
2. **系统浏览器** 负责 HTML → PDF 的渲染。因为浏览器对字体、CSS、排版的支持是最完美的，所以不会有任何乱码或排版问题。

这个思路的妙处在于：不用费劲去找什么 "md 转 pdf 的专用库"，那些库各有各的问题（字体不支持、CSS 残缺、依赖一大堆）。直接用世界上最好的 HTML 渲染器——你电脑上的浏览器——问题就都解决了。

---

## 项目结构

```
md2pdf/
├── Input/             ← 把 .md 文件放这里（支持子文件夹）
├── Output/            ← PDF 会出现在这里（保持原有目录结构）
├── md2pdf.py          ← 核心转换脚本
├── requirements.txt   ← Python 依赖（就 2 个包）
├── run.bat            ← Windows 用户双击这个
├── run.sh             ← Mac / Linux 用户运行这个
└── README.md          ← 你正在看的这个文件
```
