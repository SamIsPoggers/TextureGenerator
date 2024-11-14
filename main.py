import tkinter as tk
from tkinter import simpledialog, colorchooser
from PIL import Image, ImageTk
import os
from oregen import apply_tint_and_overlay, apply_tint_to_mineral  # Import the new function from oregen.py

# Paths to the variant images
ORE_VARIANT_PATH = "./basetextures/oreset/orevariants"
BLOCK_VARIANT_PATH = "./basetextures/oreset/blockvariants"  # Path to block variants
MINERAL_VARIANT_PATH = "./basetextures/oreset/minerals"  # Path to mineral variants

# Updated function to open the mineral variant selection
def open_mineral_variant_selection(ore_name, ore_variant, block_variant, rgb_color):
    # Create a new window for selecting the mineral variant
    mineral_variant_window = tk.Toplevel()
    mineral_variant_window.title(f"Choose Mineral Variant for {ore_name}")

    # Load and display each mineral variant image as a button
    for variant in range(1, 6):  # There are 5 mineral variants (1.png to 5.png)
        image_path = os.path.join(MINERAL_VARIANT_PATH, f"{variant}.png")
        
        # Load and resize the image
        try:
            image = Image.open(image_path).resize((64, 64), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
        except Exception as e:
            print(f"Error loading image {variant}.png:", e)
            continue

        # Create a button with the image
        button = tk.Button(mineral_variant_window, image=photo, command=lambda v=variant: [mineral_variant_window.destroy(), apply_tint_to_mineral(rgb_color, ore_name, v)])
        button.image = photo  # Keep a reference to avoid garbage collection
        button.grid(row=(variant-1) // 3, column=(variant-1) % 3, padx=10, pady=10)
    
    mineral_variant_window.geometry("300x200")

def open_color_picker(ore_name, ore_variant, block_variant):
    # Open color picker and show the selected color.
    color_code = colorchooser.askcolor(title=f"Select Color for Ore {ore_name}")[1]
    if color_code:
        print(f"Color selected for Ore {ore_name}: {color_code}")
        
        # Convert hex color to RGB tuple
        rgb_color = tuple(int(color_code[i:i+2], 16) for i in (1, 3, 5))
        
        # Now, apply tint and overlay for ore, block, and toolset images
        apply_tint_and_overlay(ore_variant, block_variant, rgb_color, ore_name)

        # After applying tint to ore, block, and toolset, show mineral variant selection
        open_mineral_variant_selection(ore_name, ore_variant, block_variant, rgb_color)

    else:
        print("No color selected.")

def open_variant_selection(ore_name):
    # Create a new window for selecting the ore variant
    ore_variant_window = tk.Toplevel()
    ore_variant_window.title(f"Choose Ore Variant for {ore_name}")
    
    # Load and display each ore variant image as a button
    for variant in range(1, 8):  # Assuming there are 7 ore variants
        image_path = os.path.join(ORE_VARIANT_PATH, f"{variant}.png")
        
        # Load and resize the image
        try:
            image = Image.open(image_path).resize((64, 64), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
        except Exception as e:
            print(f"Error loading image {variant}.png:", e)
            continue

        # Create a button with the image
        button = tk.Button(ore_variant_window, image=photo, command=lambda v=variant: [ore_variant_window.destroy(), select_block_variant(ore_name, v)])
        button.image = photo  # Keep a reference to avoid garbage collection
        button.grid(row=(variant-1) // 4, column=(variant-1) % 4, padx=10, pady=10)
    
    ore_variant_window.geometry("300x200")

def select_block_variant(ore_name, ore_variant):
    # After selecting the ore variant, ask for the block variant selection
    block_variant_window = tk.Toplevel()
    block_variant_window.title(f"Choose Block Variant for {ore_name}")

    # Load and display each block variant image as a button
    for variant in range(1, 7):  # Assuming there are 6 block variants
        image_path = os.path.join(BLOCK_VARIANT_PATH, f"{variant}.png")
        
        # Load and resize the image
        try:
            image = Image.open(image_path).resize((64, 64), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
        except Exception as e:
            print(f"Error loading image {variant}.png:", e)
            continue

        # Create a button with the image
        button = tk.Button(block_variant_window, image=photo, command=lambda v=variant: [block_variant_window.destroy(), open_color_picker(ore_name, f"{ore_variant}.png", f"{v}.png")])
        button.image = photo  # Keep a reference to avoid garbage collection
        button.grid(row=(variant-1) // 4, column=(variant-1) % 4, padx=10, pady=10)

    block_variant_window.geometry("300x200")

def open_ore_or_block_selection():
    # Ask for the ore name before showing the variants
    ore_name = simpledialog.askstring("Input", "Enter the Ore Name:")
    
    if ore_name:
        # First, show the ore variant selection
        open_variant_selection(ore_name)

def create_window():
    # Create the main window
    window = tk.Tk()
    window.title("Minecraft Texture Generator")

    # Create and place the buttons
    wood_button = tk.Button(window, text="Wood Set", command=lambda: open_color_picker("Wood", "Wood"))
    ore_button = tk.Button(window, text="Ore Set", command=open_ore_or_block_selection)

    wood_button.pack(pady=10)
    ore_button.pack(pady=10)

    window.geometry("300x200")
    window.mainloop()

if __name__ == "__main__":
    create_window()
