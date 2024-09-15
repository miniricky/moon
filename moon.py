
from colorama import Fore, Back, Style, init
from PIL import Image
import cv2
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

    subprocess.Popen(command)

def search_moon():
    y = random.randint(50, 70)
    x = random.randint(196, 470)
    
    move_to_location(x, y)

    pyautogui.typewrite('https://earnbitmoon.club/', interval=0.1)
    pyautogui.press('enter')

    time.sleep(5)

def move_to_location(x, y):
    pyautogui.moveTo(x, y, duration=random.uniform(0.5, 2.0))
    pyautogui.click()

def init_roll(confidence_level=0.9):
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

                num_parts = split_image()

                print(num_parts)

                min_pairs = float('inf')
                min_icon = None

                for i in range(1, num_parts):
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
                    time.sleep(random.randint(3, 4))

                    image_press = 'images/press.png'
                    image_press = pyautogui.locateOnScreen(image_press, confidence=confidence_level)

                    if image_press:
                        print(f"Imagen Press encontrada")
                        pyautogui.moveTo(image_press, duration=random.uniform(0.5, 2.0))
                        pyautogui.click()
                        time.sleep(random.randint(4, 5))

    close_browser()

#Save each part as a new image
def split_image(fixed_width=55, fixed_height=55):
    image_path = 'captcha/icons.png'
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Threshold to detect contours
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV, 11, 2)
    
    kernel = np.ones((5, 5), np.uint8)
    dilated = cv2.dilate(thresh, kernel, iterations=1)
    
    # Find contours of icons
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    min_contour_area = 500
    valid_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_contour_area]
    
    icon_num = 1
    for cnt in valid_contours:
        # Get the bounding box of each icon
        x, y, w, h = cv2.boundingRect(cnt)
        
        # Extract the icon area
        icon = image[y:y+h, x:x+w]

        background_color = (76, 76, 76)

        centered_icon = np.full((fixed_height, fixed_width, 3), background_color, dtype=np.uint8)

        # Calculate the position to center the icon
        x_offset = (fixed_width - w) // 2
        y_offset = (fixed_height - h) // 2
        
        # Insert the icon into the center of the blank image
        centered_icon[y_offset:y_offset+h, x_offset:x_offset+w] = icon
        
        # Save the centered icon
        cv2.imwrite(f'captcha/icon_{icon_num}.png', centered_icon)
        print(f"Icono {icon_num} guardado en 'captcha/icon_{icon_num}.png'")
        icon_num += 1

    return icon_num

# Convert image to grayscale
def convert_to_grayscale(image):
    image_gray = image.convert('L')
    image_array = np.array(image_gray)
    non_white_pixels = np.sum(image_array < 255)
    
    return non_white_pixels
    
def close_browser():
    try:
        pyautogui.hotkey('alt', 'f4')
        print("Navegador cerrado exitosamente.")
    except Exception as e:
        print(f"Error al cerrar el navegador: {e}")

# Run the search
if __name__ == "__main__":
    args = parse_arguments()
    init_moon_browser(args.windows_user, args.profile_directory)
    time.sleep(random.randint(2, 3))

    search_moon()
    init_roll()