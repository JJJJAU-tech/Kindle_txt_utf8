# Kindle_txt_utf8
Kindle 文本编码清洗工具  一键解决简体中文 txt 文件在 Calibre 转换为 AZW3 后打开乱码的问题。（繁体中文未测试）

## 🚀 使用方法
1. 下载 `Kindle_txt_utf8.exe`
2. 双击打开
3. 拖入存放乱码 txt 的文件夹
4. 点击「开始洗书」
5. 所有文件将转换为标准的 UTF-8 编码，放回 Calibre 转换即可正常阅读

## 🧠 核心逻辑
- 使用 `chardet` 智能嗅探原文件编码
- 内置非中文编码黑名单（如 Cyrillic, Latin-1），自动修正为 `GB18030`
- 适合处理从简体中文 txt 文件在 Calibre 转换为 AZW3 时打开乱码的问题
