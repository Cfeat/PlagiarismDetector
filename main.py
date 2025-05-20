import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import re

class PlagiarismCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("文本查重分析系统")
        self.root.geometry("800x600")
        self.setup_ui()
        
        self.file1_path = ""
        self.file2_path = ""

    def setup_ui(self):
        style = ttk.Style()
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TButton", font=("微软雅黑", 10), padding=6)
        style.configure("TLabel", background="#f0f0f0", font=("微软雅黑", 10))
        style.map("TButton", background=[("active", "#e6e6e6")])

        main_frame = ttk.Frame(self.root)
        main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        file_select_frame = ttk.Frame(main_frame)
        file_select_frame.pack(fill=tk.X, pady=10)

        self.btn_file1 = ttk.Button(file_select_frame, text="选择文件1", command=lambda: self.select_file(1))
        self.btn_file1.pack(side=tk.LEFT, padx=5)
        self.lbl_file1 = ttk.Label(file_select_frame, text="未选择文件")
        self.lbl_file1.pack(side=tk.LEFT, padx=10)

        self.btn_file2 = ttk.Button(file_select_frame, text="选择文件2", command=lambda: self.select_file(2))
        self.btn_file2.pack(side=tk.LEFT, padx=5)
        self.lbl_file2 = ttk.Label(file_select_frame, text="未选择文件")
        self.lbl_file2.pack(side=tk.LEFT, padx=10)

        self.btn_compare = ttk.Button(main_frame, text="开始比对", command=self.compare_files)
        self.btn_compare.pack(pady=15)

        result_frame = ttk.Frame(main_frame)
        result_frame.pack(fill=tk.BOTH, expand=True)

        self.txt_result = scrolledtext.ScrolledText(result_frame, wrap=tk.WORD, font=("微软雅黑", 10))
        self.txt_result.pack(fill=tk.BOTH, expand=True)

    def select_file(self, file_num):
        file_path = filedialog.askopenfilename(filetypes=[("文本文件", "*.txt")])
        if file_path:
            if file_num == 1:
                self.file1_path = file_path
                self.lbl_file1.config(text=file_path)
            else:
                self.file2_path = file_path
                self.lbl_file2.config(text=file_path)

    def preprocess_text(self, text):
        text = text.lower()
        text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9\s]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def levenshtein_distance(self, s1, s2):
        if len(s1) < len(s2):
            return self.levenshtein_distance(s2, s1)
        if len(s2) == 0:
            return len(s1)
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        return previous_row[-1]

    def calculate_similarity(self, text1, text2):
        processed_text1 = self.preprocess_text(text1)
        processed_text2 = self.preprocess_text(text2)

        if not processed_text1 and not processed_text2:
            return 1.0, 0
        if not processed_text1 or not processed_text2:
            max_len = max(len(processed_text1), len(processed_text2))
            return 0.0, max_len

        distance = self.levenshtein_distance(processed_text1, processed_text2)
        max_len = max(len(processed_text1), len(processed_text2))
        similarity = 1 - (distance / max_len) if max_len != 0 else 1.0
        return similarity, distance

    def read_file(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            messagebox.showerror("错误", f"无法读取文件: {str(e)}")
            return None

    def compare_files(self):
        if not self.file1_path or not self.file2_path:
            messagebox.showwarning("警告", "请先选择两个文件")
            return

        text1 = self.read_file(self.file1_path)
        text2 = self.read_file(self.file2_path)

        if text1 is None or text2 is None:
            return

        similarity, distance = self.calculate_similarity(text1, text2)
        result_text = f"""=== 分析结果 ===
Levenshtein距离: {distance}
相似度百分比: {similarity:.2%}

【预处理预览】
文件1: {self.preprocess_text(text1)[:100]}...
文件2: {self.preprocess_text(text2)[:100]}...

【结论】
"""

        if similarity >= 0.5:
            result_text += "文本高度相似（可能涉嫌抄袭）"
        elif similarity >= 0.3:
            result_text += "文本中度相似（建议人工核查）"
        else:
            result_text += "文本相似度较低"

        self.txt_result.delete(1.0, tk.END)
        self.txt_result.insert(tk.END, result_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = PlagiarismCheckerApp(root)
    root.mainloop()