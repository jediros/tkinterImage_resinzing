###############################################################################

import subprocess

# List of required modules
required_modules = [
    'opencv-python',
    'Pillow',
    # Add other modules as needed
]

def install_modules():
    for module in required_modules:
        try:
            subprocess.check_call(['pip', 'install', module])
            print(f'Successfully installed {module}')
        except subprocess.CalledProcessError:
            print(f'Error installing {module}')

# Install required modules
install_modules()
###############################################################################

import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
import cv2
import glob
import os

class ImageResizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Resizer")

        # Initialize variables
        self.image_paths = []
        self.images = []
        self.output_folder = ""

        # Create UI elements
        self.select_images_button = tk.Button(root, text="Select Images", command=self.select_images)
        self.select_images_button.pack(pady=10)

        self.resize_button = tk.Button(root, text="Resize Images", command=self.resize_images)
        self.resize_button.pack(pady=10)

    def select_images(self):
        # Allow the user to select a directory containing images
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.image_paths = glob.glob(f"{folder_path}/*.jpg") + glob.glob(f"{folder_path}/*.png")
            self.images = [cv2.imread(image) for image in self.image_paths]
            print(f"Selected {len(self.image_paths)} images.")

    def resize_images(self):
        if not self.images:
            tk.messagebox.showwarning("Warning", "Select images first.")
            return

        # Ask the user for the resize dimensions
        resize_dimensions = simpledialog.askstring("Resize Dimensions", "Enter dimensions (width x height):")

        if resize_dimensions:
            try:
                width, height = map(int, resize_dimensions.split('x'))
            except ValueError:
                tk.messagebox.showwarning("Warning", "Invalid dimensions. Please use the format 'width x height'.")
                return

            # Ask the user for the destination folder
            self.output_folder = filedialog.askdirectory()

            if self.output_folder:
                for i, image_path in enumerate(self.image_paths):
                    # Read the original image to get the extension
                    original_extension = os.path.splitext(os.path.basename(image_path))[1][1:]

                    # Resize the image
                    resized_img = cv2.resize(self.images[i], (width, height))

                    # Save the resized image to the user-selected output folder with the original extension
                    output_path = os.path.join(self.output_folder, f"resized_image_{i + 1}.{original_extension}")
                    cv2.imwrite(output_path, resized_img)

                tk.messagebox.showinfo("Information", f"Images resized and saved to {self.output_folder}.")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("250x100") #size of window
    app = ImageResizerApp(root)
    root.mainloop()
    
