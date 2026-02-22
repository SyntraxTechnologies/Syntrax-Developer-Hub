import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json, os, re, uuid, random, base64, difflib, subprocess, psutil, csv, requests

class ThemeManager:
    def __init__(self, root):
        self.root = root
        self.dark = False
        self.style = ttk.Style()
        self.style.theme_use("default")

    def toggle(self):
        self.dark = not self.dark
        if self.dark:
            bg = "#1e1e1e"
            fg = "#ffffff"
            widget_bg = "#2a2a2a"
        else:
            bg = "#f0f0f0"
            fg = "#000000"
            widget_bg = "#ffffff"

        self.root.configure(bg=bg)

        self.style.configure("TFrame", background=bg)
        self.style.configure("TLabel", background=bg, foreground=fg)
        self.style.configure("TButton", padding=6)
        self.style.configure("Treeview",
                             background=widget_bg,
                             fieldbackground=widget_bg,
                             foreground=fg)

def clear_frame(frame):
    for w in frame.winfo_children():
        w.destroy()

class JSONFormatter:
    def __init__(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(fill="both", expand=True)

        ttk.Button(frame, text="Format JSON", command=self.format_json).pack()

        self.text = tk.Text(frame)
        self.text.pack(fill="both", expand=True)

    def format_json(self):
        try:
            parsed = json.loads(self.text.get("1.0", tk.END))
            self.text.delete("1.0", tk.END)
            self.text.insert(tk.END, json.dumps(parsed, indent=4))
        except Exception as e:
            messagebox.showerror("Error", str(e))

class RegexTester:
    def __init__(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Pattern").pack(anchor="w")
        self.pattern = ttk.Entry(frame)
        self.pattern.pack(fill="x")

        ttk.Label(frame, text="Text").pack(anchor="w")
        self.text = tk.Text(frame, height=8)
        self.text.pack(fill="both")

        ttk.Button(frame, text="Run", command=self.run).pack()

        self.output = tk.Text(frame, height=8)
        self.output.pack(fill="both")

    def run(self):
        try:
            matches = re.findall(
                self.pattern.get(),
                self.text.get("1.0", tk.END)
            )
            self.output.delete("1.0", tk.END)
            self.output.insert(tk.END, "\n".join(map(str, matches)))
        except Exception as e:
            self.output.insert(tk.END, str(e))

class Base64Tool:
    def __init__(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(fill="both", expand=True)

        self.text = tk.Text(frame)
        self.text.pack(fill="both", expand=True)

        btn_frame = ttk.Frame(frame)
        btn_frame.pack()

        ttk.Button(btn_frame, text="Encode", command=self.encode).pack(side="left")
        ttk.Button(btn_frame, text="Decode", command=self.decode).pack(side="left")

    def encode(self):
        data = self.text.get("1.0", tk.END).encode()
        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, base64.b64encode(data).decode())

    def decode(self):
        try:
            data = base64.b64decode(self.text.get("1.0", tk.END))
            self.text.delete("1.0", tk.END)
            self.text.insert(tk.END, data.decode())
        except:
            messagebox.showerror("Error", "Invalid base64")

class UUIDTool:
    def __init__(self, parent):
        frame = ttk.Frame(parent)
        frame.pack()

        self.text = tk.Text(frame, height=2)
        self.text.pack()

        ttk.Button(frame, text="Generate UUID", command=self.gen).pack()

    def gen(self):
        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, str(uuid.uuid4()))

class DiffTool:
    def __init__(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(fill="both", expand=True)

        self.text1 = tk.Text(frame)
        self.text1.pack(side="left", fill="both", expand=True)

        self.text2 = tk.Text(frame)
        self.text2.pack(side="left", fill="both", expand=True)

        ttk.Button(frame, text="Compare", command=self.compare).pack()

        self.output = tk.Text(frame)
        self.output.pack(fill="both", expand=True)

    def compare(self):
        a = self.text1.get("1.0", tk.END).splitlines()
        b = self.text2.get("1.0", tk.END).splitlines()
        diff = difflib.unified_diff(a, b)

        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, "\n".join(diff))

class APITester:
    def __init__(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="URL").pack(anchor="w")
        self.url = ttk.Entry(frame)
        self.url.pack(fill="x")

        ttk.Button(frame, text="Send GET", command=self.send).pack()

        self.output = tk.Text(frame)
        self.output.pack(fill="both", expand=True)

    def send(self):
        try:
            r = requests.get(self.url.get())
            self.output.delete("1.0", tk.END)
            self.output.insert(tk.END, r.text)
        except Exception as e:
            self.output.insert(tk.END, str(e))

class PortChecker:
    def __init__(self, parent):
        import socket

        self.socket = socket
        frame = ttk.Frame(parent)
        frame.pack()

        ttk.Label(frame, text="Host").pack()
        self.host = ttk.Entry(frame)
        self.host.pack()

        ttk.Label(frame, text="Port").pack()
        self.port = ttk.Entry(frame)
        self.port.pack()

        ttk.Button(frame, text="Check", command=self.check).pack()

    def check(self):
        s = self.socket.socket()
        try:
            s.settimeout(1)
            s.connect((self.host.get(), int(self.port.get())))
            messagebox.showinfo("Port", "Open")
        except:
            messagebox.showinfo("Port", "Closed")
        s.close()

class PingTool:
    def __init__(self, parent):
        frame = ttk.Frame(parent)
        frame.pack()

        ttk.Label(frame, text="Host").pack()
        self.host = ttk.Entry(frame)
        self.host.pack()

        ttk.Button(frame, text="Ping", command=self.ping).pack()

        self.out = tk.Text(frame, height=10)
        self.out.pack()

    def ping(self):
        host = self.host.get()
        result = subprocess.getoutput(f"ping -n 4 {host}")
        self.out.delete("1.0", tk.END)
        self.out.insert(tk.END, result)

class ProcessViewer:
    def __init__(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(frame, columns=("pid","cpu"), show="headings")
        self.tree.heading("pid", text="PID")
        self.tree.heading("cpu", text="CPU")
        self.tree.pack(fill="both", expand=True)

        self.update()

    def update(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        for p in psutil.process_iter(['pid','cpu_percent']):
            self.tree.insert("", "end", values=(p.info['pid'], p.info['cpu_percent']))

        self.tree.after(2000, self.update)

class EnvViewer:
    def __init__(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(fill="both", expand=True)

        text = tk.Text(frame)
        text.pack(fill="both", expand=True)

        for k,v in os.environ.items():
            text.insert(tk.END, f"{k} = {v}\n")

class FileSearch:
    def __init__(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(fill="both", expand=True)

        ttk.Button(frame, text="Select Folder", command=self.load).pack()
        self.text = tk.Text(frame)
        self.text.pack(fill="both", expand=True)

    def load(self):
        folder = filedialog.askdirectory()
        for root, dirs, files in os.walk(folder):
            for f in files:
                self.text.insert(tk.END, os.path.join(root,f) + "\n")

class CSVViewer:
    def __init__(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(fill="both", expand=True)

        ttk.Button(frame, text="Open CSV", command=self.open).pack()

        self.text = tk.Text(frame)
        self.text.pack(fill="both", expand=True)

    def open(self):
        file = filedialog.askopenfilename(filetypes=[("CSV","*.csv")])
        with open(file) as f:
            reader = csv.reader(f)
            for row in reader:
                self.text.insert(tk.END, ",".join(row) + "\n")

class SyntraxHub:
    def __init__(self, root):

        self.root = root
        root.title("Syntrax Developer Hub")
        root.geometry("1200x750")

        self.theme = ThemeManager(root)

        bar = ttk.Frame(root)
        bar.pack(fill="x")

        ttk.Button(bar, text="Toggle Dark Mode",
                   command=self.theme.toggle).pack(side="right")

        container = ttk.Frame(root)
        container.pack(fill="both", expand=True)

        self.sidebar = ttk.Treeview(container)
        self.sidebar.pack(side="left", fill="y")

        self.main = ttk.Frame(container)
        self.main.pack(side="left", fill="both", expand=True)

        self.tools = {
            "Code Tools": {
                "JSON Formatter": JSONFormatter,
                "Regex Tester": RegexTester,
                "Text Diff": DiffTool,
                "Base64 Tool": Base64Tool
            },
            "Network": {
                "API Tester": APITester,
                "Port Checker": PortChecker,
                "Ping Tool": PingTool
            },
            "System": {
                "Process Viewer": ProcessViewer,
                "Environment Viewer": EnvViewer
            },
            "File Tools": {
                "File Search": FileSearch,
                "CSV Viewer": CSVViewer
            },
            "Generators": {
                "UUID Generator": UUIDTool
            }
        }

        for cat, tools in self.tools.items():
            parent = self.sidebar.insert("", "end", text=cat)
            for name in tools:
                self.sidebar.insert(parent, "end", text=name)

        self.sidebar.bind("<<TreeviewSelect>>", self.load_tool)

    def load_tool(self, event):
        sel = self.sidebar.selection()
        if not sel:
            return

        item = self.sidebar.item(sel)
        tool_name = item["text"]
        parent = self.sidebar.parent(sel)

        if not parent:
            return

        category = self.sidebar.item(parent)["text"]
        tool_class = self.tools[category][tool_name]

        clear_frame(self.main)
        tool_class(self.main)

if __name__ == "__main__":
    root = tk.Tk()
    app = SyntraxHub(root)
    root.mainloop()