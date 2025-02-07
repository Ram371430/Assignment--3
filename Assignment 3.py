
class ImageSaver:
    def __init__(self, app):
        self.app = app

    def save_image(self):
        if self.app.cropped_image is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".png")
            if file_path:
                cv2.imwrite(file_path, self.app.cropped_image)

    def undo(self):
        if len(self.app.history) > 1:
            self.app.redo_stack.append(self.app.history.pop())
            self.app.display_image(self.app.history[-1], self.app.cropped_canvas)

    def redo(self):
        if self.app.redo_stack:
            redo_image = self.app.redo_stack.pop()
            self.app.history.append(redo_image)
            self.app.display_image(redo_image, self.app.cropped_canvas)

class ImageEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Editor")

        self.image = None
        self.cropped_image = None
        self.history = []
        self.redo_stack = []

        # Canvases
        self.canvas = tk.Canvas(root, width=500, height=500, bg='gray')
        self.canvas.pack(side="left")

        self.cropped_canvas = tk.Canvas(root, width=500, height=500, bg='gray')
        self.cropped_canvas.pack(side="right")

        # Buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(fill="x")
        tk.Button(btn_frame, text="Load Image", command=self.load_image).pack(side="left")
        tk.Button(btn_frame, text="Save Image", command=self.save_image).pack(side="left")
        tk.Button(btn_frame, text="Undo", command=self.undo).pack(side="left")
        tk.Button(btn_frame, text="Redo", command=self.redo).pack(side="left")

        # Slider for resizing
        self.resize_slider = tk.Scale(root, from_=10, to=200, orient="horizontal", label="Resize %", command=self.resize_image)
        self.resize_slider.pack(fill="x")

        # Modules
        self.loader = ImageLoader(self)
        self.editor = ImageEditor(self)
        self.saver = ImageSaver(self)

        # Mouse events
        self.canvas.bind("<ButtonPress-1>", self.editor.start_crop)
        self.canvas.bind("<B1-Motion>", self.editor.draw_crop)
        self.canvas.bind("<ButtonRelease-1>", self.editor.finish_crop)

        # Keyboard shortcuts
        root.bind("<Control-z>", lambda e: self.undo())
        root.bind("<Control-y>", lambda e: self.redo())
        root.bind("<Control-s>", lambda e: self.save_image())

    # Wrapper methods for buttons and shortcuts
    def load_image(self):
        self.loader.load_image()

    def resize_image(self, value):
        self.editor.resize_image(value)

    def save_image(self):
        self.saver.save_image()

    def undo(self):
        self.saver.undo()

    def redo(self):
        self.saver.redo()

    def display_image(self, img, canvas):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_tk = ImageTk.PhotoImage(img_pil)
        canvas.image = img_tk
        canvas.create_image(0, 0, anchor="nw", image=img_tk)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditorApp(root)
    root.mainloop()
