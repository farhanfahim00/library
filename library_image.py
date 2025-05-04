#By Sami Ul Haq & Farhan Fahim
#sami.haq@stud.th-deg.de
#farhan.taimoor@stud.th-deg.de

#All Imports
import tkinter as tk
from PIL import Image, ImageTk, ImageOps
import pyocr
import pyocr.builders
from tkinter import filedialog
from PIL.Image import Resampling
from tkinter import simpledialog, messagebox
from library_model import load_book, add_book  # reuse backend


class ImageDrawer:
    def __init__(self, root, image_path):
        self.root = root
        # Load the image
        self.original_image = Image.open(image_path)

        # Define max dimensions (you can change 700x700 if needed)
        max_width, max_height = 700, 700
        img_width, img_height = self.original_image.size

        # Resize image proportionally to fit within max dimensions
        scale = min(max_width / img_width, max_height / img_height, 1.0)  # Don't upscale
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)
        self.image = self.original_image.resize((new_width, new_height), Resampling.LANCZOS)


        # Resize window and canvas
        self.root.geometry(f"{new_width}x{new_height + 100}")
        self.canvas = tk.Canvas(root, width=new_width, height=new_height)
        self.canvas.pack()

        # Convert to PhotoImage and display
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)

        # Variables to track mouse position and rectangle drawing
        self.start_x = None
        self.start_y = None
        self.rect = None

        # Labels to show dimensions and recognized text
        self.dim_label = tk.Label(root, text="Dimensions: Width x Height", font=("Helvetica", 12))
        self.dim_label.pack(pady=10)
        self.text_label = tk.Label(root, text="Recognized Text: ", font=("Helvetica", 12))
        self.text_label.pack(pady=10)

        # Setup OCR tool using pyocr
        tools = pyocr.get_available_tools()
        if not tools:
            raise Exception("No OCR tool found. Please install Tesseract OCR or another tool.")
        self.tool = tools[0]  # Use the first available tool (usually Tesseract)

        # Bind mouse events to the canvas
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

    def on_button_press(self, event):
        # Remove previous rectangle if present
        if self.rect:
            self.canvas.delete(self.rect)
        self.start_x = event.x
        self.start_y = event.y
        # Create a new rectangle (initially zero size)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red",
                                                 width=2)

    def on_mouse_drag(self, event):
        # Update rectangle dimensions during drag
        self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)
        width = abs(event.x - self.start_x)
        height = abs(event.y - self.start_y)
        self.dim_label.config(text=f"Dimensions: {width} x {height}")

    def on_button_release(self, event):
        # Finalize rectangle when mouse button released
        self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)
        width = abs(event.x - self.start_x)
        height = abs(event.y - self.start_y)
        self.dim_label.config(text=f"Dimensions: {width} x {height}")
        self.recognize_text_in_rectangle(self.start_x, self.start_y, event.x, event.y)

    def recognize_text_in_rectangle(self, x1, y1, x2, y2):
        cropped_image = self.image.crop((x1, y1, x2, y2))
        recognized_text = self.tool.image_to_string(cropped_image, lang='eng',
                                                    builder=pyocr.builders.TextBuilder()).strip()
        self.text_label.config(text=f"Recognized Text: {recognized_text}")

        if not recognized_text:
            messagebox.showinfo("No Text Found", "No text was recognized in the selected area.")
            return

        # Search in library
        books = load_book()
        found_books = [book for book in books if
                       recognized_text.lower() in book["title"].lower() or recognized_text.lower() in book[
                           "author"].lower()]

        if found_books:
            # Show matched books
            result = "\n\n".join(
                [f'{b["title"]} by {b["author"]}, {b["year"]} - Status: {b["status"]}' for b in found_books])
            messagebox.showinfo("Book(s) Found", f"Found the following book(s):\n\n{result}")
        else:
            # Offer to add a new book
            if messagebox.askyesno("Book Not Found",
                                   f"No match for '{recognized_text}'. Would you like to add a new book?"):
                title = recognized_text
                author = simpledialog.askstring("Author", "Enter Author's Name:")
                year = simpledialog.askinteger("Year", "Enter Year of Publication:")
                if author and year:
                    add_book(title, author, year, "available")
                    messagebox.showinfo("Book Added", f"'{title}' by {author} added to the library.")

def open_image_drawer(parent_window):
    """
    Opens a file dialog to select an image, then opens the ImageDrawer window with that image.
    """
    file_path = filedialog.askopenfilename(
        parent=parent_window,
        title="Select an Image",
        filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")]
    )

    if file_path:
        new_window = tk.Toplevel(parent_window)
        new_window.title("Draw on Image & OCR")
        ImageDrawer(new_window, file_path)
    else:
        print("No image selected.")
