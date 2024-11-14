from PIL import Image
import os

# Paths
BASE_PATH = "./basetextures/oreset/stonetypes"
GENERATED_PATH = "./generated/block"  # Directory for ore textures
ITEM_BASE_PATH = "./basetextures/oreset/toolset/base"  # Base tools directory
TOOL_PATH = "./basetextures/oreset/toolset"  # Tools to apply tint
GENERATED_ITEM_PATH = "./generated/item"  # Directory for tool textures
ORE_VARIANT_PATH = "./basetextures/oreset/orevariants"
BLOCK_VARIANT_PATH = "./basetextures/oreset/blockvariants"  # Block variants path
ARMOR_PATH = "./basetextures/oreset/armor/item"  # Armor to apply tint
GENERATED_MODEL_PATH = "./generated/models/armor"  # Directory for model layers (armor models)
ARMOR_MODEL_PATH = "./basetextures/oreset/armor"  # Armor model layers to apply tint
MINERAL_VARIANT_PATH = "./basetextures/oreset/minerals"  # Path to mineral variants

# Ensure the directories exist
os.makedirs(GENERATED_PATH, exist_ok=True)
os.makedirs(GENERATED_ITEM_PATH, exist_ok=True)

# Consolidated function to apply tint and overlay for ore, block, and tools
def apply_tint_and_overlay(ore_variant_name, block_variant_name, tint_color, ore_name):
    # Process ore variant
    ore_variant_path = os.path.join(ORE_VARIANT_PATH, ore_variant_name)
    ore_variant_image = Image.open(ore_variant_path).convert("RGBA")
    ore_variant_tinted = apply_tint(ore_variant_image, tint_color)

    # Process block variant
    block_variant_path = os.path.join(BLOCK_VARIANT_PATH, block_variant_name)
    block_variant_image = Image.open(block_variant_path).convert("RGBA")
    block_variant_tinted = apply_tint(block_variant_image, tint_color)

    # Save tinted block image (block variant, like asd_block.png)
    save_tinted_image(block_variant_tinted, ore_name, "block")

    # Now handle the ore texture generation (this is for the stone variant)
    stone_name = "stone.png"
    stone_path = os.path.join(BASE_PATH, stone_name)
    stone_image = Image.open(stone_path).convert("RGBA")

    # Overlay the tinted ore onto the stone image
    combined_image = Image.alpha_composite(stone_image, ore_variant_tinted)

    # Save the combined image as the stone ore texture (asd_ore.png)
    output_path = os.path.join(GENERATED_PATH, f"{ore_name}_ore.png")
    combined_image.save(output_path, "PNG")
    print(f"Generated texture saved as: {output_path}")

    # Now handle the deepslate ore generation
    deepslate_name = "deepslate.png"
    deepslate_path = os.path.join(BASE_PATH, deepslate_name)
    deepslate_image = Image.open(deepslate_path).convert("RGBA")

    # Overlay the tinted ore onto the deepslate image
    combined_deepslate_image = Image.alpha_composite(deepslate_image, ore_variant_tinted)

    # Save the combined image as the deepslate ore texture (asd_deepslate_ore.png)
    deepslate_output_path = os.path.join(GENERATED_PATH, f"{ore_name}_deepslate_ore.png")
    combined_deepslate_image.save(deepslate_output_path, "PNG")
    print(f"Generated texture saved as: {deepslate_output_path}")

    # Generate tool textures for this ore
    apply_tint_to_tools(tint_color, ore_name)

    # Generate armor textures for this ore
    apply_tint_to_armor(tint_color, ore_name)
    
    
    # Generate armor model layer textures for this ore
    apply_tint_to_armor_model_layers(tint_color, ore_name)


# Helper function to apply tint to an image
def apply_tint(image, tint_color):
    tinted_image = Image.new("RGBA", image.size)
    for x in range(image.width):
        for y in range(image.height):
            r, g, b, a = image.getpixel((x, y))
            brightness = 0.299 * r + 0.587 * g + 0.114 * b
            new_r = int(tint_color[0] * (brightness / 255))
            new_g = int(tint_color[1] * (brightness / 255))
            new_b = int(tint_color[2] * (brightness / 255))
            if a > 0:
                tinted_image.putpixel((x, y), (new_r, new_g, new_b, a))
            else:
                tinted_image.putpixel((x, y), (r, g, b, a))
    return tinted_image

# Save the tinted image to the specified output path
def save_tinted_image(tinted_image, ore_name, variant_type):
    output_path = os.path.join(GENERATED_PATH, f"{ore_name}_{variant_type}.png")
    tinted_image.save(output_path, "PNG")
    print(f"Generated {variant_type} texture saved as: {output_path}")

# Apply tint to the tool images
def apply_tint_to_tools(tint_color, ore_name):
    tool_names = ['axe.png', 'sword.png', 'pickaxe.png', 'shovel.png', 'hoe.png']
    base_names = ['axebase.png', 'swordbase.png', 'pickaxebase.png', 'shovelbase.png', 'hoebase.png']

    for tool_name, base_name in zip(tool_names, base_names):
        tool_image_path = os.path.join(TOOL_PATH, tool_name)
        base_image_path = os.path.join(ITEM_BASE_PATH, base_name)

        try:
            tool_image = Image.open(tool_image_path).convert("RGBA")
            base_image = Image.open(base_image_path).convert("RGBA")
        except Exception as e:
            print(f"Error loading tool image or base image: {tool_name} or {base_name}", e)
            continue

        # Apply the same tint to the tool image
        tinted_tool_image = apply_tint(tool_image, tint_color)

        # Overlay the tinted tool image onto the base image
        combined_tool_image = Image.alpha_composite(base_image, tinted_tool_image)

        # Save the final image to the generated/item directory
        tool_output_path = os.path.join(GENERATED_ITEM_PATH, f"{ore_name}_{tool_name.split('.')[0]}.png")
        combined_tool_image.save(tool_output_path, "PNG")
        print(f"Generated tool texture saved as: {tool_output_path}")

# Apply tint to the armor images
def apply_tint_to_armor(tint_color, ore_name):
    armor_names = ['helmet.png', 'chestplate.png', 'leggings.png', 'boots.png']

    for armor_name in armor_names:
        armor_image_path = os.path.join(ARMOR_PATH, armor_name)

        try:
            armor_image = Image.open(armor_image_path).convert("RGBA")
        except Exception as e:
            print(f"Error loading armor image: {armor_name}", e)
            continue

        # Apply the tint to the armor image
        tinted_armor_image = apply_tint(armor_image, tint_color)

        # Save the final armor texture to the generated/item directory
        armor_output_path = os.path.join(GENERATED_ITEM_PATH, f"{ore_name}_{armor_name}")
        tinted_armor_image.save(armor_output_path, "PNG")
        print(f"Generated armor texture saved as: {armor_output_path}")

# Apply tint to the armor model layers (layer_1.png, layer_2.png)
def apply_tint_to_armor_model_layers(tint_color, ore_name):
    layer_names = ['layer_1.png', 'layer_2.png']

    for layer_name in layer_names:
        layer_image_path = os.path.join(ARMOR_MODEL_PATH, layer_name)

        try:
            layer_image = Image.open(layer_image_path).convert("RGBA")
        except Exception as e:
            print(f"Error loading armor model layer image: {layer_name}", e)
            continue

        # Apply the tint to the armor model layer image
        tinted_layer_image = apply_tint(layer_image, tint_color)

        # Save the final armor model layer texture to the generated/models/armor directory
        layer_output_path = os.path.join(GENERATED_MODEL_PATH, f"{ore_name}_{layer_name}")
        tinted_layer_image.save(layer_output_path, "PNG")
        print(f"Generated armor model layer texture saved as: {layer_output_path}")

# Apply tint to the selected mineral image
def apply_tint_to_mineral(tint_color, ore_name, mineral_variant):
    mineral_image_path = os.path.join(MINERAL_VARIANT_PATH, f"{mineral_variant}.png")

    try:
        mineral_image = Image.open(mineral_image_path).convert("RGBA")
    except Exception as e:
        print(f"Error loading mineral variant image: {mineral_variant}.png", e)
        return

    # Apply the tint to the mineral image
    tinted_mineral_image = apply_tint(mineral_image, tint_color)

    # Save the final mineral texture to the generated/item directory
    mineral_output_path = os.path.join(GENERATED_ITEM_PATH, f"{ore_name}.png")
    tinted_mineral_image.save(mineral_output_path, "PNG")
    print(f"Generated mineral texture saved as: {mineral_output_path}")