import os
import chardet
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinterdnd2 import DND_FILES, TkinterDnD

# 探测器说是这些编码，一律按 GB18030 处理 ---
WEIRD_ENCODINGS = ['koi8-u', 'cp1250', 'cp1251', 'cp1252', 'ISO-8859-1', 'latin-1', 'ascii']

class KindleWasherPro:
    def __init__(self, root):
        self.root = root
        root.title("洗书机 · 智能编码修复版")
        root.geometry("650x420")
        
        self.src_path = tk.StringVar()
        self.dst_path = tk.StringVar()
        
        # --- UI 绘制 ---
        tk.Label(root, text="Kindle 乱码终结者 Pro", font=("微软雅黑", 18, "bold")).pack(pady=10)
        
        # 源文件夹（支持拖拽）
        tk.Label(root, text="📂 源文件夹（拖拽文件夹到下方框内）", font=("微软雅黑", 10)).pack()
        self.src_entry = tk.Entry(root, textvariable=self.src_path, width=60)
        self.src_entry.pack(pady=5)
        self.src_entry.drop_target_register(DND_FILES)
        self.src_entry.dnd_bind("<<Drop>>", self.drop_src)
        tk.Button(root, text="浏览选择", command=self.select_src).pack(pady=2)
        
        # 目标文件夹
        tk.Label(root, text="💾 保存位置", font=("微软雅黑", 10)).pack(pady=(15,0))
        self.dst_entry = tk.Entry(root, textvariable=self.dst_path, width=60)
        self.dst_entry.pack(pady=5)
        self.dst_entry.drop_target_register(DND_FILES)
        self.dst_entry.dnd_bind("<<Drop>>", self.drop_dst)
        tk.Button(root, text="浏览选择", command=self.select_dst).pack(pady=2)
        
        # 进度条
        self.progress = ttk.Progressbar(root, length=550, mode="determinate")
        self.progress.pack(pady=20)
        
        # 状态
        self.status_label = tk.Label(root, text="待命，请拖入文件夹", font=("微软雅黑", 9))
        self.status_label.pack()
        
        # 开始按钮
        self.start_btn = tk.Button(root, text="🚀 开始洗书（非中文编码自动拦截）", 
                                   font=("微软雅黑", 11, "bold"), 
                                   bg="#D32F2F", fg="white", padx=20, pady=8,
                                   command=self.start_wash)
        self.start_btn.pack(pady=15)
        
    def drop_src(self, event):
        path = event.data.strip().replace("{", "").replace("}", "")
        if os.path.isdir(path):
            self.src_path.set(path)
        else:
            dir_path = os.path.dirname(path)
            if os.path.isdir(dir_path):
                self.src_path.set(dir_path)
                
    def drop_dst(self, event):
        path = event.data.strip().replace("{", "").replace("}", "")
        if os.path.isdir(path):
            self.dst_path.set(path)
        else:
            dir_path = os.path.dirname(path)
            if os.path.isdir(dir_path):
                self.dst_path.set(dir_path)
    
    def select_src(self):
        path = filedialog.askdirectory()
        if path:
            self.src_path.set(path)
    
    def select_dst(self):
        path = filedialog.askdirectory()
        if path:
            self.dst_path.set(path)
    
    def start_wash(self):
        src = self.src_path.get().strip()
        dst = self.dst_path.get().strip()
        
        if not src or not dst:
            messagebox.showerror("醒醒", "源文件夹和保存位置都得选呀！")
            return
        
        if not os.path.exists(dst):
            os.makedirs(dst)
            
        files = [f for f in os.listdir(src) if f.lower().endswith(".txt")]
        if not files:
            messagebox.showinfo("没活干", "源文件夹里一个 .txt 都没有。")
            return
        
        total = len(files)
        self.progress["maximum"] = total
        self.progress["value"] = 0
        self.status_label.config(text="正在嗅探编码，非中文编码自动拦截...")
        self.start_btn.config(state="disabled")
        self.root.update()
        
        success = 0
        for i, filename in enumerate(files):
            file_path = os.path.join(src, filename)
            try:
                # --- 核心：嗅探 + 黑名单过滤（来自你验证通过的逻辑）---
                with open(file_path, "rb") as f:
                    raw = f.read(30000)
                    result = chardet.detect(raw)
                    encoding = result["encoding"]
                    
                    if encoding is None or encoding.lower() in WEIRD_ENCODINGS:
                        encoding = "gb18030"
                
                with open(file_path, "r", encoding=encoding, errors="ignore") as f:
                    content = f.read()
                with open(os.path.join(dst, filename), "w", encoding="utf-8") as f:
                    f.write(content)
                
                success += 1
                self.status_label.config(text=f"✅ {filename} (编码强制修正为: {encoding})")
            except Exception as e:
                self.status_label.config(text=f"❌ {filename} 失败: {str(e)[:30]}")
            
            self.progress["value"] = i + 1
            self.root.update()
        
        self.status_label.config(text=f"✨ 完成！成功清洗 {success}/{total} 本。顽固乱码已被镇压。")
        self.start_btn.config(state="normal")
        messagebox.showinfo("报告", f"洗完了！\n成功：{success} 本\n保存位置：{dst}")

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = KindleWasherPro(root)
    root.mainloop()