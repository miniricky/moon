import argparse
import cv2
import numpy as np
import os
import pyautogui
import random
import requests
import subprocess
import telebot
import time
from colorama import Fore, Back, Style, init
from PIL import Image

# Import the functions from openvpn
from openvpn import connect_vpn, disconnect_vpn

TOKEN = '7517601793:AAEOKrkom7DWB13skzKUETr9aT7YCgBCJzw'
CHAT_ID = '505309958'

bot = telebot.TeleBot(TOKEN)

#Send messge to telegram
def send_status_update(message):
    try:
        bot.send_message(CHAT_ID, message)
    except Exception as e:
        print(f"Error al enviar mensaje de Telegram: {e}")

# Argument parser for widows user and directory
def parse_arguments():
    parser = argparse.ArgumentParser(description='Moon script with Chrome profile and user data directory')
    parser.add_argument('--profile-directory', required=True, help='Chrome profile directory name')
    return parser.parse_args()

# Configure the moon browser
def init_moon_browser(user_name, profile):
    browser_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"
    user_data_dir = f"C:/Users/{user_name}/AppData/Local/Google/Chrome/User Data"
    profile_arg = f"--profile-directory=Profile {profile}"

    # Command to open the browser with the profile
    command = [
        browser_path,
        "--start-maximized",
        f"--user-data-dir={user_data_dir}",
        profile_arg
    ]

    subprocess.Popen(command)

# Navigates to the specific URL and prepares for further actions
def search_moon():
    y = random.randint(50, 70)
    x = random.randint(196, 470)
    
    move_to_location(x, y)

    pyautogui.typewrite('https://earnbitmoon.club/', interval=0.1)
    pyautogui.press('enter')

    time.sleep(random.randint(1, 2))

# Moves the mouse cursor to a specific location
def move_to_location(x, y):
    pyautogui.moveTo(x, y, duration=random.uniform(0.5, 2.0))
    pyautogui.click()

# Initialize the roll functionality, attempting to find and click the 'Roll' image and verify captcha
def init_roll(confidence_level=0.9, threshold=500, max_attempts=5):
    image_roll = 'images/roll.png'
    attempts = 0
    image_roll_location = None
    roll = True

    while attempts < max_attempts:
        try:
            image_roll_location = pyautogui.locateOnScreen(image_roll, confidence=confidence_level)
        except pyautogui.ImageNotFoundException:
            image_roll_location = None
        
        if image_roll_location:
            print(f"Imagen Roll encontrada")
            pyautogui.moveTo(image_roll_location, duration=random.uniform(0.5, 1.5))
            pyautogui.click()
            time.sleep(random.randint(1, 2))
            break
        else:
            print(f"Imagen Roll no encontrada, reintentando en 1 segundo... ({attempts+1}/{max_attempts})")
            time.sleep(1)
            attempts += 1

    if not image_roll_location:
        print(f"No se pudo encontrar la imagen Roll después de varios intentos.")
        roll = None
        return roll

    image_verify = 'images/verify.png'
    attempts = 0
    image_verify_location = None
    
    while attempts < max_attempts:
        try:
            image_verify_location = pyautogui.locateOnScreen(image_verify, confidence=confidence_level)
        except pyautogui.ImageNotFoundException:
            image_verify_location = None
            
        if image_verify_location:
            print(f"Imagen Verify encontrada")
            pyautogui.moveTo(image_verify_location, duration=random.uniform(0.5, 1.0))
            pyautogui.click()
            time.sleep(random.randint(3, 4))
            break
        else:
            print(f"Imagen Verify no encontrada, reintentando en 1 segundo... ({attempts+1}/{max_attempts})")
            time.sleep(1)
            attempts += 1

    if not image_verify_location:
        print("No se pudo encontrar la imagen Verify después de varios intentos.")
        roll = None
        return roll

    response = solve_captcha()
    if not response:
        return
             
    image_mistake = 'images/mistake.png'
    attempts = 0
    image_mistake_location = None

    while attempts < max_attempts:
        try:
            image_mistake_location = pyautogui.locateOnScreen(image_mistake, confidence=confidence_level)
        except pyautogui.ImageNotFoundException:
            image_mistake_location = None
        
        if image_mistake_location:
            print(f"hubo un error al resolver el icon captcha, reintentando en 3 segundos... ({attempts+1}/{max_attempts})")
            solve_captcha()
            time.sleep(3)
            attempts += 1
        else:
            break
    
    return roll

# Handles the captcha solution process by identifying similar images
def solve_captcha(confidence_level=0.9, threshold=500, max_attempts=5):
    image_text = 'images/text.png'
    attempts = 0
    image_text_location = None
    response = True

    # Check if the captcha folder exists, if not, create it
    if not os.path.exists('captcha'):
        os.makedirs('captcha')
        print("Carpeta 'captcha' creada.")
    
    while attempts < max_attempts:
        try:
            image_text_location = pyautogui.locateOnScreen(image_text, confidence=confidence_level)
        except pyautogui.ImageNotFoundException:
            image_text_location = None

        if image_text_location:
            top, left, width, height = image_text_location

            left = int(left + 41)
            top = int(top)
            width = int(width)
            height = int(55)

            screenshot = pyautogui.screenshot(region=(top, left, width, height))
            screenshot.save('captcha/icons.png')
            print(f"Captura guardada en 'captcha/icons.png'")
            break
        else:
            print(f"Imagen Text no encontrada, reintentando en 1 segundo... ({attempts+1}/{max_attempts})")
            time.sleep(1)
            attempts += 1
    
    if not image_text_location:
        print(f"No se pudo encontrar la imagen Text después de varios intentos.")
        response = None
        return response

    num_parts = split_image()

    pair_counts = {}

    for i in range(1, num_parts):
        icon_path_1 = f'captcha/icon_{i}.png'
        pair_counts[icon_path_1] = 0
        
        for j in range(1, num_parts):
            if i != j:
                icon_path_2 = f'captcha/icon_{j}.png'
                
                # Check if the images are similar
                if compare_images(icon_path_1, icon_path_2, threshold):
                    pair_counts[icon_path_1] += 1

    # Find the image with the least number of pairs
    least_paired_icon = min(pair_counts, key=pair_counts.get)
    min_pairs = pair_counts[least_paired_icon]

    print(f"El icono con menos pares es: {least_paired_icon} con {min_pairs} pares.")

    attempts = 0
    image_icon_location = None

    while attempts < max_attempts:
        try:
            image_icon_location = pyautogui.locateOnScreen(least_paired_icon, confidence=confidence_level)
        except pyautogui.ImageNotFoundException:
            image_icon_location = None

        if image_icon_location:
            print(f"Imagen Icon encontrada")
            pyautogui.moveTo(image_icon_location, duration=random.uniform(0.5, 1.0))
            pyautogui.click()
            time.sleep(random.randint(3, 4))
            break
        else:
            print(f"Imagen Icon no encontrada, reintentando en 2 segundos... ({attempts+1}/{max_attempts})")
            time.sleep(2)
            attempts += 1
    
    if not image_icon_location:
        print(f"No se pudo encontrar la imagen Icon después de varios intentos.")
        response = None
        return response
    
    image_press = 'images/press.png'
    attempts = 0
    image_press_location = None

    while attempts < max_attempts:
        try:
            image_press_location = pyautogui.locateOnScreen(image_press, confidence=confidence_level)
        except pyautogui.ImageNotFoundException:
            image_press_location = None
        
        if image_press_location:
            print(f"Imagen Press encontrada")
            pyautogui.moveTo(image_press_location, duration=random.uniform(0.5, 1.0))
            pyautogui.click()
            time.sleep(random.randint(2, 3))
            break
        else:
            print(f"Imagen Press no encontrada, reintentando en 1 segundo... ({attempts+1}/{max_attempts})")
            time.sleep(1)
            attempts += 1

    if not image_press_location:
        print(f"No se pudo encontrar la imagen Press después de varios intentos.")
        response = None
        return response
    
    return response

# Save each part of the captcha as a separate image
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

# Compare two images and return whether they are similar based on their histogram
def compare_images(image1_path, image2_path, threshold=500):
    img1 = cv2.imread(image1_path, 0)
    img2 = cv2.imread(image2_path, 0)

    diff = cv2.absdiff(img1, img2)

    non_zero_count = np.count_nonzero(diff)
    
    return non_zero_count < threshold
    
def close_browser():
    try:
        pyautogui.hotkey('alt', 'f4')
        print(f"Navegador cerrado exitosamente.")
    except Exception as e:
        print(f"Error al cerrar el navegador: {e}")

def main():   
    user_name = os.getlogin()
    args = parse_arguments()
    profile_list = [item.strip() for item in args.profile_directory.split(",")]

    time_list = {
        1: "5",
        2: "2.7",
        3: "1.8",
        4: "1.45",
        5: "1.20"
    }

    ovpn_list = {
        1: "us-free-104063.protonvpn.udp.ovpn",
        2: "us-free-113078.protonvpn.udp.ovpn",
        3: "us-free-110062.protonvpn.udp.ovpn",
        4: "us-free-108069.protonvpn.udp.ovpn",
        5: "us-free-114155.protonvpn.udp.ovpn"
    }

    index = 0
    count = len(profile_list)
    seconds = float(time_list[count])
    minutes = int(seconds * 60)
    while True:
        start_time = time.time()
        minutes_sleep = minutes
       
        # Connect openvpn
        vpn_process = None

        if index > 0:
            vpn_config = f'C:/Users/{user_name}/OpenVPN/config/{ovpn_list[index]}'
            auth_file = f'C:/Users/{user_name}/OpenVPN/config/credentials.txt'

            # Connect to the VPN
            vpn_process = connect_vpn(vpn_config, auth_file)
        
            if not vpn_process:
                break    
        
        # Get the public IP with ipinfo.io and geolocation information
        response = requests.get('https://ipinfo.io')
        data = response.json()
        country = data.get('country', 'N/A')

        profile = profile_list[index]
        init_moon_browser(user_name, profile)
        time.sleep(random.randint(4, 5))

        search_moon()
        roll = init_roll()

        image_expired = 'images/expired.png'
        attempts = 0
        max_attempts = 3
        confidence_level=0.9
        image_expired_location = None

        while attempts < max_attempts:
            try:
                image_expired_location = pyautogui.locateOnScreen(image_expired, confidence=confidence_level)
            except pyautogui.ImageNotFoundException:
                image_expired_location = None
            
            if image_expired_location:
                print(f"hubo un error al cargar el icon captcha, reintentando en 3 segundos... ({attempts+1}/{max_attempts})")
                pyautogui.hotkey('ctrl', 'r')
                time.sleep(random.randint(1, 2))
                init_roll()
                attempts += 1
            else:
                break

        close_browser()

        if roll:
            send_status_update(f'Claim: {user_name} - perfil {profile} - región {country}.')

        if vpn_process:
            disconnect_vpn(vpn_process)
            time.sleep(random.randint(3, 4))

        if index + 1 == count:
            index = 0
        else:
            index += 1

        end_time = time.time()
        execution_time = int(end_time - start_time)
        
        print(f"Terminó en {execution_time}")
        if minutes_sleep > execution_time:
            minutes_sleep = int(minutes_sleep - execution_time)
        else:
            minutes_sleep = int(random.randint(4, 5))

        print(f"Siguiente perfil en {minutes_sleep}")
        time.sleep(minutes_sleep)

# Init the script
if __name__ == "__main__":
    main()