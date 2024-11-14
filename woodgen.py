from PIL import Image, ImageEnhance
import os

# Paths to the woodset directories
BLOCKS_PATH = "./basetextures/woodset/blocks"
ITEMS_PATH = "./basetextures/woodset/items"
TRAPDOOR_PATH = "./basetextures/woodset/trapdoorvariants"
DOOR_TOP_PATH = "./basetextures/woodset/doorvariants"
DOOR_ITEMS_PATH = "./basetextures/woodset/doorvariants/items"
ENTITY_BASE_PATH = "./basetextures/woodset/entities"
GENERATED_ENTITY_PATH = "./generated/entities"

# Output paths
OUTPUT_BLOCKS_PATH = "./generated/block"
OUTPUT_ITEMS_PATH = "./generated/item"

def apply_tint(image, color):
    """Apply a color tint to an image."""
    image = image.convert("RGBA")
    tint_layer = Image.new("RGBA", image.size, color + (0,))
    blended = Image.blend(image, tint_layer, alpha=0.5)
    return blended

def apply_tint_to_woodset(wood_name, door_variant, trapdoor_variant, rgb_color):
    # Ensure output directories exist
    os.makedirs(OUTPUT_BLOCKS_PATH, exist_ok=True)
    os.makedirs(OUTPUT_ITEMS_PATH, exist_ok=True)
    # Ensure the directories exist
    os.makedirs(GENERATED_ENTITY_PATH, exist_ok=True)

    # 1. Tint all block textures and rename stripped log accordingly
    for filename in os.listdir(BLOCKS_PATH):
        file_path = os.path.join(BLOCKS_PATH, filename)
        if filename.endswith(".png"):
            try:
                image = Image.open(file_path)
                tinted_image = apply_tint(image, rgb_color)

                # Rename stripped_log to stripped_<woodset_name>_log
                if filename == "stripped_log.png":
                    output_filename = f"stripped_{wood_name}_log.png"
                else:
                    output_filename = f"{wood_name}_{filename}"

                tinted_image.save(os.path.join(OUTPUT_BLOCKS_PATH, output_filename))
                print(f"Tinted and saved {filename} in blocks as {output_filename}.")
            except Exception as e:
                print(f"Error tinting {filename}: {e}")

    # 2. Tint all item textures except 'chest.png'
    for filename in os.listdir(ITEMS_PATH):
        file_path = os.path.join(ITEMS_PATH, filename)
        if filename.endswith(".png") and filename != "chest.png":
            try:
                image = Image.open(file_path)
                tinted_image = apply_tint(image, rgb_color)
                tinted_image.save(os.path.join(OUTPUT_ITEMS_PATH, f"{wood_name}_{filename}"))
                print(f"Tinted and saved {filename} in items.")
            except Exception as e:
                print(f"Error tinting {filename}: {e}")

    # 3. Handle chest_boat texture with untinted chest overlay
    chest_path = os.path.join(ITEMS_PATH, "chest.png")
    chest_boat_path = os.path.join(ITEMS_PATH, "chest_boat.png")
    try:
        chest_image = Image.open(chest_path).convert("RGBA")  # Untinted chest
        chest_boat_image = Image.open(chest_boat_path).convert("RGBA")
        tinted_chest_boat = apply_tint(chest_boat_image, rgb_color)
        chest_boat_with_overlay = Image.alpha_composite(tinted_chest_boat, chest_image)  # Overlay untinted chest
        chest_boat_with_overlay.save(os.path.join(OUTPUT_ITEMS_PATH, f"{wood_name}_chest_boat.png"))
        print("Tinted and saved chest_boat.png with untinted chest overlay.")
    except Exception as e:
        print(f"Error processing chest textures: {e}")

    # 4. Tint the selected trapdoor variant and save to blocks with wood_name
    trapdoor_file = f"{trapdoor_variant}_trapdoor.png"
    trapdoor_path = os.path.join(TRAPDOOR_PATH, trapdoor_file)
    try:
        trapdoor_image = Image.open(trapdoor_path)
        tinted_trapdoor = apply_tint(trapdoor_image, rgb_color)
        tinted_trapdoor.save(os.path.join(OUTPUT_BLOCKS_PATH, f"{wood_name}_trapdoor.png"))
        print(f"Tinted and saved trapdoor variant as {wood_name}_trapdoor.png.")
    except Exception as e:
        print(f"Error tinting trapdoor variant {trapdoor_variant}: {e}")

    # 5. Tint the selected door variant (top, bottom, and item textures) and save with wood_name
    door_top_file = f"{door_variant}_door_top.png"
    door_bottom_file = f"{door_variant}_door_bottom.png"
    door_item_file = f"{door_variant}_door.png"
    door_top_path = os.path.join(DOOR_TOP_PATH, door_top_file)
    door_bottom_path = os.path.join(DOOR_TOP_PATH, door_bottom_file)
    door_item_path = os.path.join(DOOR_ITEMS_PATH, door_item_file)

    # Tint and save door top to blocks with wood_name
    try:
        door_top_image = Image.open(door_top_path)
        tinted_door_top = apply_tint(door_top_image, rgb_color)
        tinted_door_top.save(os.path.join(OUTPUT_BLOCKS_PATH, f"{wood_name}_door_top.png"))
        print(f"Tinted and saved door top as {wood_name}_door_top.png.")
    except Exception as e:
        print(f"Error tinting door top {door_top_file}: {e}")

    # Tint and save door bottom to blocks with wood_name
    try:
        door_bottom_image = Image.open(door_bottom_path)
        tinted_door_bottom = apply_tint(door_bottom_image, rgb_color)
        tinted_door_bottom.save(os.path.join(OUTPUT_BLOCKS_PATH, f"{wood_name}_door_bottom.png"))
        print(f"Tinted and saved door bottom as {wood_name}_door_bottom.png.")
    except Exception as e:
        print(f"Error tinting door bottom {door_bottom_file}: {e}")

    # Tint and save door item to items with wood_name
    try:
        door_item_image = Image.open(door_item_path)
        tinted_door_item = apply_tint(door_item_image, rgb_color)
        tinted_door_item.save(os.path.join(OUTPUT_ITEMS_PATH, f"{wood_name}_door.png"))
        print(f"Tinted and saved door item as {wood_name}_door.png.")
    except Exception as e:
        print(f"Error tinting door item {door_item_file}: {e}")

    generate_tinted_boat_entity(wood_name, rgb_color)


def generate_tinted_boat_entity(wood_name, tint_color):
    """Tints the boat entity image for the woodset and saves it as <woodname>_boat.png."""
    boat_image_path = os.path.join(ENTITY_BASE_PATH, "boat.png")

    try:
        # Load the boat image and apply the tint
        boat_image = Image.open(boat_image_path).convert("RGBA")
        tinted_boat_image = apply_tint(boat_image, tint_color)

        # Save the tinted boat image in the generated entities directory with the woodset name
        boat_output_path = os.path.join(GENERATED_ENTITY_PATH, f"{wood_name}_boat.png")
        tinted_boat_image.save(boat_output_path, "PNG")
        print(f"Generated entity texture saved as: {boat_output_path}")

    except Exception as e:
        print(f"Error processing boat entity image: {e}")