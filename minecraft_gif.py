import requests
from PIL import Image
from io import BytesIO
from tqdm import tqdm
import os

def download_image(player_name, y_value, save_path):
    url = f"https://visage.surgeplay.com/full/384/{player_name}?y={y_value}"
    response = requests.get(url)
    
    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        image.save(os.path.join(save_path, f"{y_value}.png"))
    else:
        print(f"Failed to download image for y={y_value}")

def create_gif(player_name, save_path):
    images = []
    y_values = list(range(0, 361, 10))

    for y_value in tqdm(y_values, desc="Downloading images"):
        download_image(player_name, y_value, save_path)

    for y_value in tqdm(y_values, desc="Processing images"):
        image_path = os.path.join(save_path, f"{y_value}.png")
        if os.path.exists(image_path):
            images.append(Image.open(image_path))

    gif_path = os.path.join(save_path, player_name + ".gif")
    images[0].save(gif_path, save_all=True, append_images=images[1:], duration=70, disposal=2, loop=0)
    print(f"GIF created and saved at {gif_path}")

if __name__ == "__main__":
    player_name = input("Please enter Minecraft username: ")
    save_path = player_name + "_gif"

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    create_gif(player_name, save_path)