import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font

class TextEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Text Editor")
        self.root.geometry("800x600")

        self.text_area = tk.Text(self.root, wrap=tk.WORD, undo=True)
        self.text_area.pack(fill=tk.BOTH, expand=True)

        self.create_menu()
        self.create_toolbar()

        self.current_file = None

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        edit_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Cut", command=self.cut_text)
        edit_menu.add_command(label="Copy", command=self.copy_text)
        edit_menu.add_command(label="Paste", command=self.paste_text)
        edit_menu.add_command(label="Undo", command=self.undo_text)
        edit_menu.add_command(label="Find", command=self.find_text)
        edit_menu.add_command(label="Replace", command=self.replace_text)

        format_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Format", menu=format_menu)
        format_menu.add_command(label="Bold", command=self.bold_text)
        format_menu.add_command(label="Italic", command=self.italic_text)
        format_menu.add_command(label="Underline", command=self.underline_text)
        format_menu.add_command(label="Font", command=self.change_font)
        format_menu.add_command(label="Font Size", command=self.change_font_size)
        format_menu.add_separator()
        format_menu.add_command(label="Left Align", command=self.left_align_text)
        format_menu.add_command(label="Center Align", command=self.center_align_text)
        format_menu.add_command(label="Right Align", command=self.right_align_text)

    def create_toolbar(self):
        toolbar = tk.Frame(self.root, bd=1, relief=tk.RAISED)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        bold_button = tk.Button(toolbar, text="B", command=self.bold_text)
        bold_button.pack(side=tk.LEFT, padx=2, pady=2)
        italic_button = tk.Button(toolbar, text="I", command=self.italic_text)
        italic_button.pack(side=tk.LEFT, padx=2, pady=2)
        underline_button = tk.Button(toolbar, text="U", command=self.underline_text)
        underline_button.pack(side=tk.LEFT, padx=2, pady=2)

    def new_file(self):
        self.current_file = None
        self.text_area.delete(1.0, tk.END)

    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            self.current_file = file_path
            with open(file_path, 'r') as file:
                content = file.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, content)

    def save_file(self):
        if self.current_file:
            with open(self.current_file, 'w') as file:
                content = self.text_area.get(1.0, tk.END)
                file.write(content)
        else:
            self.save_as_file()

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            self.current_file = file_path
            with open(file_path, 'w') as file:
                content = self.text_area.get(1.0, tk.END)
                file.write(content)

    def cut_text(self):
        self.text_area.event_generate("<<Cut>>")

    def copy_text(self):
        self.text_area.event_generate("<<Copy>>")

    def paste_text(self):
        self.text_area.event_generate("<<Paste>>")

    def undo_text(self):
        self.text_area.event_generate("<<Undo>>")

    def find_text(self):
        find_window = tk.Toplevel(self.root)
        find_window.title("Find")
        find_window.geometry("300x150")

        tk.Label(find_window, text="Find:").pack(pady=5)
        find_entry = tk.Entry(find_window, width=30)
        find_entry.pack(pady=5)

        def find():
            search_text = find_entry.get()
            content = self.text_area.get(1.0, tk.END)
            start = content.find(search_text)
            if start != -1:
                self.text_area.tag_add("found", f"1.0 + {start} chars", f"1.0 + {start + len(search_text)} chars")
                self.text_area.tag_config("found", background="yellow")
            else:
                messagebox.showinfo("Find", "Text not found")
        
        tk.Button(find_window, text="Find", command=find).pack(pady=5)

    def replace_text(self):
        replace_window = tk.Toplevel(self.root)
        replace_window.title("Replace")
        replace_window.geometry("300x200")

        tk.Label(replace_window, text="Find:").pack(pady=5)
        find_entry = tk.Entry(replace_window, width=30)
        find_entry.pack(pady=5)

        tk.Label(replace_window, text="Replace with:").pack(pady=5)
        replace_entry = tk.Entry(replace_window, width=30)
        replace_entry.pack(pady=5)

        def replace():
            find_text = find_entry.get()
            replace_text = replace_entry.get()
            content = self.text_area.get(1.0, tk.END)
            new_content = content.replace(find_text, replace_text)
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, new_content)
        
        tk.Button(replace_window, text="Replace", command=replace).pack(pady=5)

    def bold_text(self):
        current_tags = self.text_area.tag_names("sel.first")
        if "bold" in current_tags:
            self.text_area.tag_remove("bold", "sel.first", "sel.last")
        else:
            self.text_area.tag_add("bold", "sel.first", "sel.last")
            self.text_area.tag_configure("bold", font=font.Font(weight="bold"))

    def italic_text(self):
        current_tags = self.text_area.tag_names("sel.first")
        if "italic" in current_tags:
            self.text_area.tag_remove("italic", "sel.first", "sel.last")
        else:
            self.text_area.tag_add("italic", "sel.first", "sel.last")
            self.text_area.tag_configure("italic", font=font.Font(slant="italic"))

    def underline_text(self):
        current_tags = self.text_area.tag_names("sel.first")
        if "underline" in current_tags:
            self.text_area.tag_remove("underline", "sel.first", "sel.last")
        else:
            self.text_area.tag_add("underline", "sel.first", "sel.last")
            self.text_area.tag_configure("underline", font=font.Font(underline=True))

    def change_font(self):
        font_family = tk.simpledialog.askstring("Font", "Enter font family:")
        if font_family:
            self.text_area.config(font=(font_family, self.text_area.cget("font").split()[1]))

    def change_font_size(self):
        font_size = tk.simpledialog.askinteger("Font Size", "Enter font size:")
        if font_size:
            self.text_area.config(font=(self.text_area.cget("font").split()[0], font_size))

    def left_align_text(self):
        self.text_area.tag_configure("left", justify="left")
        self.text_area.tag_add("left", "1.0", "end")

    def center_align_text(self):
        self.text_area.tag_configure("center", justify="center")
        self.text_area.tag_add("center", "1.0", "end")

    def right_align_text(self):
        self.text_area.tag_configure("right", justify="right")
        self.text_area.tag_add("right", "1.0", "end")

if __name__ == "__main__":
    root = tk.Tk()
    app = TextEditorApp(root)
    root.mainloop()
