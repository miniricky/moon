
from colorama import Fore, Back, Style, init
from PIL import Image
import numpy as np
import subprocess
import argparse
import random
import time
import pyautogui

# Argument parser for widows user and directory
def parse_arguments():
    parser = argparse.ArgumentParser(description='Swash script with Chrome profile and user data directory')
    parser.add_argument('--windows-user', required=True, help='Windows User')
    parser.add_argument('--profile-directory', required=True, help='Chrome profile directory name')
    return parser.parse_args()

# Configure the swash browser
def init_moon_browser(windows_user, profile_directory):
    browser_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"
    user_data_dir = f"C:/Users/{windows_user}/AppData/Local/Google/Chrome/User Data"
    profile_arg = f"--profile-directory={profile_directory}"

    # Command to open the browser with the profile
    command = [
        browser_path,
        "--start-maximized",
        f"--user-data-dir={user_data_dir}",
        profile_arg
    ]

    process = subprocess.Popen(command)
    return process

def init_roll(process, confidence_level=0.9):
    image_roll = 'images/roll.png'
    image_roll_location = pyautogui.locateOnScreen(image_roll, confidence=confidence_level)
    
    if image_roll_location:
        print(f"Imagen Roll encontrada")
        pyautogui.moveTo(image_roll_location, duration=random.uniform(0.5, 2.0))
        pyautogui.click()
        time.sleep(random.randint(1, 2))

        image_verify = 'images/verify.png'
        image_verify_location = pyautogui.locateOnScreen(image_verify, confidence=confidence_level)
        
        if image_verify_location:
            print(f"Imagen Verify encontrada")
            pyautogui.moveTo(image_verify_location, duration=random.uniform(0.5, 2.0))
            pyautogui.click()
            time.sleep(random.randint(1, 2))

            image_text = 'images/text.png'
            image_text_location = pyautogui.locateOnScreen(image_text, confidence=confidence_level)

            if image_text_location:
                top, left, width, height = image_text_location

                left = int(left + 41)
                top = int(top)
                width = int(width)
                height = int(55)

                screenshot = pyautogui.screenshot(region=(top, left, width, height))
                screenshot.save('captcha/icons.png')
                print(f"Captura guardada en 'captcha/icons.png'")

                split_image()

                num_parts = 5
                min_pairs = float('inf')
                min_icon = None

                for i in range(1, num_parts + 1):
                    icon_path = f'captcha/icon_{i}.png'
                    icon_image = Image.open(icon_path)
                    
                    non_white_pixels = convert_to_grayscale(icon_image)
                    print(f"Icono {i} tiene {non_white_pixels} píxeles no blancos")
                    
                    if non_white_pixels < min_pairs:
                        min_pairs = non_white_pixels
                        min_icon = icon_path

                icon_locaton = pyautogui.locateOnScreen(min_icon, confidence=confidence_level)
                if icon_locaton:
                    print(f"Imagen Roll encontrada")
                    pyautogui.moveTo(icon_locaton, duration=random.uniform(0.5, 2.0))
                    pyautogui.click()

                    image_press = 'images/press.png'
                    image_press = pyautogui.locateOnScreen(image_press, confidence=confidence_level)

                    if image_press:
                        print(f"Imagen Press encontrada")
                        pyautogui.moveTo(image_press, duration=random.uniform(0.5, 2.0))
                        pyautogui.click()
                        time.sleep(random.randint(1, 2))

    close_browser(process)

# # Save each part as a new image
def split_image():
    image_path = 'captcha/icons.png'
    image = Image.open(image_path)

    width, height = image.size
    num_parts = 5
    part_width = width // num_parts

    for i in range(num_parts):
        left = i * part_width
        top = 0
        right = left + part_width
        bottom = height
        
        part = image.crop((left, top, right, bottom))
        
        part.save(f'captcha/icon_{i + 1}.png')
        print(f"Parte {i + 1} guardada en 'captcha/icon_{i + 1}.png'")

# Convert image to grayscale
def convert_to_grayscale(image):
    image_gray = image.convert('L')
    image_array = np.array(image_gray)
    non_white_pixels = np.sum(image_array < 255)
    
    return non_white_pixels

def search_moon():
    y = random.randint(50, 70)
    x = random.randint(196, 470)
    
    move_to_location(x, y)

    pyautogui.typewrite('https://earnbitmoon.club/', interval=0.1)
    pyautogui.press('enter')

    time.sleep(10)

def move_to_location(x, y):
    pyautogui.moveTo(x, y, duration=random.uniform(0.5, 2.0))
    pyautogui.click()

    
def close_browser(process):
    try:
        process.terminate()
        print("Navegador cerrado exitosamente.")
    except Exception as e:
        print(f"Error al cerrar el navegador: {e}")

# Run the search
if __name__ == "__main__":
    args = parse_arguments()
    process = init_moon_browser(args.windows_user, args.profile_directory)
    time.sleep(random.randint(1, 2))

    search_moon()
    init_roll(process)