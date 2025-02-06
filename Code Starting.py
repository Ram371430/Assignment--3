import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np

# Image Loading and Display
class ImageLoader:
    def __init__(self, app):
        self.app = app

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.app.image = cv2.imread(file_path)
            self.app.display_image(self.app.image, self.app.canvas)
            self.app.history.append(self.app.image.copy())

# Crop and resize part
class ImageEditor:
    def __init__(self, app):
        self.app = app
        self.start_x = self.start_y = 0
        self.rect = None

    def start_crop(self, event):
        self.start_x, self.start_y = event.x, event.y
        if self.rect:
            self.app.canvas.delete(self.rect)
        self.rect = self.app.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red')

    def draw_crop(self, event):
        self.app.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def finish_crop(self, event):
        end_x, end_y = event.x, event.y
        if self.app.image is not None:
            x1, y1 = min(self.start_x, end_x), min(self.start_y, end_y)
            x2, y2 = max(self.start_x, end_x), max(self.start_y, end_y)
            self.app.cropped_image = self.app.image[y1:y2, x1:x2]
            self.app.display_image(self.app.cropped_image, self.app.cropped_canvas)
            self.app.history.append(self.app.cropped_image.copy())

    def resize_image(self, value):
        if self.app.cropped_image is not None:
            scale_percent = int(value)
            width = int(self.app.cropped_image.shape[1] * scale_percent / 100)
            height = int(self.app.cropped_image.shape[0] * scale_percent / 100)
            resized = cv2.resize(self.app.cropped_image, (width, height), interpolation=cv2.INTER_AREA)
            self.app.display_image(resized, self.app.cropped_canvas)
            self.app.history.append(resized.copy())