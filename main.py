import tkinter as tk
from tkinter import simpledialog, colorchooser
from PIL import Image, ImageTk
import os
from oregen import apply_tint_and_overlay, apply_tint_to_mineral  # Import functions from oregen.py
from woodgen import apply_tint_to_woodset  # Import the wood tinting function from woodgen.py

# Paths to the variant images
ORE_VARIANT_PATH = "./basetextures/oreset/orevariants"
BLOCK_VARIANT_PATH = "./basetextures/oreset/blockvariants"
MINERAL_VARIANT_PATH = "./basetextures/oreset/minerals"
DOOR_VARIANT_PATH = "./basetextures/woodset/doorvariants"
TRAPDOOR_VARIANT_PATH = "./basetextures/woodset/trapdoorvariants"

# Updated function to open the mineral variant selection
def open_mineral_variant_selection(ore_name, ore_variant, block_variant, rgb_color):
    # Create a new window for selecting the mineral variant
    mineral_variant_window = tk.Toplevel()
    mineral_variant_window.title(f"Choose Mineral Variant for {ore_name}")

    # Load and display each mineral variant image as a button
    for variant in range(1, 6):  # Assuming 5 mineral variants
        image_path = os.path.join(MINERAL_VARIANT_PATH, f"{variant}.png")
        try:
            image = Image.open(image_path).resize((64, 64), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
        except Exception as e:
            print(f"Error loading image {variant}.png:", e)
            continue

        # Create a button with the image
        button = tk.Button(mineral_variant_window, image=photo, command=lambda v=variant: [mineral_variant_window.destroy(), apply_tint_to_mineral(rgb_color, ore_name, v)])
        button.image = photo
        button.grid(row=(variant-1) // 3, column=(variant-1) % 3, padx=10, pady=10)
    
    mineral_variant_window.geometry("300x200")

# Function for picking color and applying ore textures
def open_color_picker(ore_name, ore_variant, block_variant):
    color_code = colorchooser.askcolor(title=f"Select Color for Ore {ore_name}")[1]
    if color_code:
        print(f"Color selected for Ore {ore_name}: {color_code}")
        rgb_color = tuple(int(color_code[i:i+2], 16) for i in (1, 3, 5))
        apply_tint_and_overlay(ore_variant, block_variant, rgb_color, ore_name)
        open_mineral_variant_selection(ore_name, ore_variant, block_variant, rgb_color)
    else:
        print("No color selected.")

# Wood set color picker function
def open_wood_color_picker(wood_name, door_variant, trapdoor_variant):
    color_code = colorchooser.askcolor(title=f"Select Color for Wood Set {wood_name}")[1]
    if color_code:
        rgb_color = tuple(int(color_code[i:i+2], 16) for i in (1, 3, 5))
        print(f"Color selected for Wood {wood_name}: {color_code}")
        apply_tint_to_woodset(wood_name, door_variant, trapdoor_variant, rgb_color)
    else:
        print("No color selected.")

# Wood set door variant selection
def open_door_variant_selection(wood_name):
    door_variant_window = tk.Toplevel()
    door_variant_window.title(f"Choose Door Variant for {wood_name}")
    
    for variant in range(1, 12):  # Assuming 11 door variants
        image_path = os.path.join(DOOR_VARIANT_PATH, f"{variant}_door_top.png")
        try:
            image = Image.open(image_path).resize((64, 64), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
        except Exception as e:
            print(f"Error loading image {variant}_door_top.png:", e)
            continue

        button = tk.Button(door_variant_window, image=photo, command=lambda v=variant: [door_variant_window.destroy(), open_trapdoor_variant_selection(wood_name, v)])
        button.image = photo
        button.grid(row=(variant-1) // 4, column=(variant-1) % 4, padx=10, pady=10)
    
    door_variant_window.geometry("300x200")

# Wood set trapdoor variant selection
def open_trapdoor_variant_selection(wood_name, door_variant):
    trapdoor_variant_window = tk.Toplevel()
    trapdoor_variant_window.title(f"Choose Trapdoor Variant for {wood_name}")

    for variant in range(1, 12):  # Assuming 11 trapdoor variants
        image_path = os.path.join(TRAPDOOR_VARIANT_PATH, f"{variant}_trapdoor.png")
        try:
            image = Image.open(image_path).resize((64, 64), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
        except Exception as e:
            print(f"Error loading image {variant}_trapdoor.png:", e)
            continue

        button = tk.Button(trapdoor_variant_window, image=photo, command=lambda v=variant: [trapdoor_variant_window.destroy(), open_wood_color_picker(wood_name, door_variant, v)])
        button.image = photo
        button.grid(row=(variant-1) // 4, column=(variant-1) % 4, padx=10, pady=10)

    trapdoor_variant_window.geometry("300x200")

def open_variant_selection(ore_name):
    # Existing function for selecting ore variants
    ore_variant_window = tk.Toplevel()
    ore_variant_window.title(f"Choose Ore Variant for {ore_name}")
    
    for variant in range(1, 8):  # Assuming 7 ore variants
        image_path = os.path.join(ORE_VARIANT_PATH, f"{variant}.png")
        try:
            image = Image.open(image_path).resize((64, 64), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
        except Exception as e:
            print(f"Error loading image {variant}.png:", e)
            continue

        button = tk.Button(ore_variant_window, image=photo, command=lambda v=variant: [ore_variant_window.destroy(), select_block_variant(ore_name, v)])
        button.image = photo
        button.grid(row=(variant-1) // 4, column=(variant-1) % 4, padx=10, pady=10)
    
    ore_variant_window.geometry("300x200")

def select_block_variant(ore_name, ore_variant):
    # Existing function for selecting block variants
    block_variant_window = tk.Toplevel()
    block_variant_window.title(f"Choose Block Variant for {ore_name}")

    for variant in range(1, 7):  # Assuming 6 block variants
        image_path = os.path.join(BLOCK_VARIANT_PATH, f"{variant}.png")
        try:
            image = Image.open(image_path).resize((64, 64), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
        except Exception as e:
            print(f"Error loading image {variant}.png:", e)
            continue

        button = tk.Button(block_variant_window, image=photo, command=lambda v=variant: [block_variant_window.destroy(), open_color_picker(ore_name, f"{ore_variant}.png", f"{v}.png")])
        button.image = photo
        button.grid(row=(variant-1) // 4, column=(variant-1) % 4, padx=10, pady=10)

    block_variant_window.geometry("300x200")

def open_ore_or_block_selection():
    # Ask for the ore name and start variant selection
    ore_name = simpledialog.askstring("Input", "Enter the Ore Name:")
    if ore_name:
        open_variant_selection(ore_name)

def open_wood_selection():
    # Ask for the wood set name, then start door variant selection
    wood_name = simpledialog.askstring("Input", "Enter the Wood Set Name:").lower()
    if wood_name:
        open_door_variant_selection(wood_name)

def create_window():
    window = tk.Tk()
    window.title("Minecraft Texture Generator")

    wood_button = tk.Button(window, text="Wood Set", command=open_wood_selection)
    ore_button = tk.Button(window, text="Ore Set", command=open_ore_or_block_selection)

    wood_button.pack(pady=10)
    ore_button.pack(pady=10)

    window.geometry("300x200")
    window.mainloop()

if __name__ == "__main__":
    create_window()
