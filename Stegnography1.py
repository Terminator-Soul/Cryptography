from PIL import Image


def encode_text_in_image(image_path, output_path, text):
    img = Image.open(image_path)
    encoded = img.copy()
    width, height = img.size
    pixels = (
        encoded.load()
    )  # Append a delimiter to the text to indicate end of the text
    text += "<<<END>>> "
    binary_text = "".join(format(ord(char), "08b") for char in text)
    bin_index = 0
    for i in range(width):
        for j in range(height):
            pixel = list(pixels[i, j])  # Get the RGB values of the pixel
            for k in range(3):  # Modify the RGB channels
                if bin_index < len(binary_text):
                    pixel[k] = pixel[k] & ~1 | int(binary_text[bin_index])
                    bin_index += 1
            pixels[i, j] = tuple(pixel)
            if bin_index >= len(binary_text):
                break
        if bin_index >= len(binary_text):
            break
    encoded.save(output_path)
    print(f"Text successfully encoded into {output_path}")


def decode_text_from_image(image_path):
    img = Image.open(image_path)
    width, height = img.size
    pixels = img.load()
    binary_text = ""
    for i in range(width):
        for j in range(height):
            pixel = list(pixels[i, j])
            for k in range(
                3
            ):  # Retrieve the least significant bit from each RGB channel
                binary_text += str(pixel[k] & 1)  # Convert binary string to text
    all_bytes = [binary_text[i : i + 8] for i in range(0, len(binary_text), 8)]
    decoded_text = "".join(chr(int(byte, 2)) for byte in all_bytes)
    delimiter = "<<<END>>>"
    if delimiter in decoded_text:
        decoded_text = decoded_text[: decoded_text.index(delimiter)]
    else:
        raise ValueError("No hidden text found in the image.")
    return decoded_text  # Example usage: # Encode text


encode_text_in_image(
    "Facebook.png", "outputimage.png", "Hidden message goes here!"
)  # Decode text
hidden_text = decode_text_from_image("outputimage.png")
print(f"Decoded text: {hidden_text}")
