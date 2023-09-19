from playwright.sync_api import sync_playwright, Page
import random
import time
import re
import shutil
import requests
import uuid
import credentials

image_name = "!"

def random_sleep():
    """Sleep for a random amount of time between 1 and 5 seconds."""
    #time.sleep(5)
    time.sleep(random.randint(1, 2))

def main(bot_command: str, channel_url: str, PROMPT: str):
    try:
        browser = None
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("https://www.discord.com/login")

            # Get credentials securely
            email = "sebastian.furn@gmail.com"
            password = credentials.password
            if not email or not password:
                print("Email or password not provided in credentials.txt.")
                raise ValueError("Email or password not provided in credentials.txt.")
            
            page.fill("input[name='email']", email)
            random_sleep()
            page.fill("input[name='password']", password)
            random_sleep()
            page.click("button[type='submit']")
            random_sleep()
            page.wait_for_url("https://discord.com/channels/@me", timeout=15000)
            print("Successfully logged into Discord.")
            random_sleep()
            open_discord_channel(page, channel_url, bot_command, PROMPT)
    except Exception as e:
        print(f"Error occurred: {e} while executing the main function.")
        raise e

    return image_name

def open_discord_channel(page, channel_url: str, bot_command: str, PROMPT: str):
    """
    Function to open a Discord channel and send a bot command.

    Parameters:
    - page: The page object representing the current browser context.
    - channel_url (str): The URL of the channel to open.
    - bot_command (str): The bot command to send.
    - PROMPT (str): The prompt text.

    Returns:
    - None
    """
    try:
        page.goto(f"{channel_url}")
        random_sleep()
        page.wait_for_load_state("networkidle")
        print("Successfully opened the appropriate channel.")

        print("Entering the specified bot command.")
        send_bot_command(page, bot_command, PROMPT)
    
    except Exception as e:
        print(f"An error occurred while opening the channel and entering the bot command: {e}")
        raise e

def send_bot_command(page, command: str, PROMPT: str):
    """
    Function to send a command to the bot in the chat bar.

    Parameters:
    - page: The page object representing the current browser context.
    - command (str): The command to send to the bot.
    - PROMPT (str): The prompt for the command.

    Returns:
    - None
    """
    try:
        print("Clicking on chat bar.")
        chat_bar = page.locator('xpath=//*[@id="app-mount"]/div[2]/div[1]/div[1]/div/div[2]/div/div/div/div/div[3]/div[2]/main/form/div/div[1]/div/div[3]/div/div[2]/div')
        random_sleep()

        print("Typing in bot command")
        chat_bar.fill(command)
        random_sleep()

        print("Selecting the prompt option in the suggestions menu")
        prompt_option = page.locator('xpath=/html/body/div[1]/div[2]/div[1]/div[1]/div/div[2]/div/div/div/div/div[3]/div[2]/main/form/div/div[2]/div/div/div[2]/div[1]/div/div/div')
        random_sleep()
        prompt_option.click()

        print("Generating prompt using OpenAI's API.")
        generate_prompt_and_submit_command(page, PROMPT)

    except Exception as e:
        print(f"An error occurred while sending the bot command: {e}")
        raise e

def generate_prompt_and_submit_command(page, prompt: str):
    try:
        prompt_text = prompt
        random_sleep()
        pill_value_locator = 'xpath=//*[@id="app-mount"]/div[2]/div[1]/div[1]/div/div[2]/div/div/div/div/div[3]/div/main/form/div/div[2]/div/div[2]/div/div/div/span[2]/span[2]'
        page.fill(pill_value_locator, prompt_text)
        random_sleep()
        page.keyboard.press("Enter")
        print(f'Successfully submitted prompt: {prompt_text}')
        wait_and_select_upscale_options(page, prompt_text)
    except Exception as e:
        print(f"An error occurred while submitting the prompt: {e}")
        raise e

def wait_and_select_upscale_options(page, prompt_text: str):
    """
    Function to wait for and select upscale options.

    Parameters:
    - page: The page to operate on.
    - prompt_text (str): The text of the prompt.

    Returns:
    - None
    """
    try:
        prompt_text = prompt_text.lower()

        # Repeat until upscale options are found
        while True:
            last_message = get_last_message(page)

            # Check for 'U1' in the last message
            if 'U1' in last_message:
                print("Found upscale options. Attempting to upscale first generated image.")
                try:
                    select_upscale_option(page, 'U1')
                    time.sleep(random.randint(3, 5))
                except Exception as e:
                    print(f"An error occurred while selecting upscale options: {e}")
                    raise e

                download_upscaled_image(page, prompt_text)
                break  # Exit the loop when upscale options have been found and selected

            else:
                print("Upscale options not yet available, waiting...")
                time.sleep(random.randint(3, 5))

    except Exception as e:
        print(f"An error occurred while finding the last message: {e}")
        raise e

def get_last_message(page) -> str:
    """
    Function to get the last message from the provided page.

    Parameters:
    - page: The page from which to fetch the last message.

    Returns:
    - str: The text of the last message.
    """
    try:
        messages = page.query_selector_all(".messageListItem-ZZ7v6g")
        if not messages:
            print("No messages found on the page.")
            raise ValueError("No messages found on the page.")
        
        last_message = messages[-1]
        last_message_text = last_message.evaluate('(node) => node.innerText')

        if not last_message_text:
            print("Last message text cannot be empty.")
            raise ValueError("Last message text cannot be empty.")
        
        last_message_text = str(last_message_text)
        # Commented out for now, as it's not needed.
        # print(f"Last message: {last_message_text}")
        return last_message_text
    
    except Exception as e:
        print(f"Error occurred: {e} while getting the last message.")
        raise e

def select_upscale_option(page, option_text: str):
    """
    Function to select an upscale option based on the provided text.

    Parameters:
    - page: The page object representing the current browser context.
    - option_text (str): The text of the upscale option to select.

    Returns:
    - None
    """
    try:
        upscale_option = page.locator(f"button:has-text('{option_text}')").locator("nth=-1")
        if not upscale_option:
            print(f"No upscale option found with text: {option_text}.")
            raise ValueError(f"No upscale option found with text: {option_text}.")
        
        upscale_option.click()
        print(f"Successfully clicked {option_text} upscale option.")
    
    except Exception as e:
        print(f"An error occurred while selecting the upscale option: {e}")
        raise e

def download_upscaled_image(page, prompt_text: str):
    try:
        messages = page.query_selector_all(".messageListItem-ZZ7v6g")
        upscaled_image = messages[-1]
        
        message_text = upscaled_image.evaluate_handle('(node) => node.innerText')
        message_text = str(message_text)

        if 'Vary (Strong)' in message_text and 'Web' in message_text:
            try:
                image_elements = page.query_selector_all('.originalLink-Azwuo9')
                upscaled_image = image_elements[-1]

                src = upscaled_image.get_attribute('href')
                url = src
                response = re.sub(r'[^a-zA-Z0-9\s]', '', prompt_text)
                response = response.replace(' ', '_').replace(',', '_')
                response = re.sub(r'[\<>:"/|?*]', '', response)
                response = response.replace('\n\n', '_')
                response = response[:50].rstrip('. ')
                download_response = requests.get(url, stream=True)
                file_name = str(response) + str(uuid.uuid1()) + ".png"

                with open(f'images/{file_name}', 'wb') as out_file:
                    shutil.copyfileobj(download_response.raw, out_file)
                    global image_name
                    image_name = f'images/{file_name}'
                del download_response

            except Exception as e:
                print(f"An error occurred while downloading the images: {e}")

        else:
            download_upscaled_image(page, prompt_text)

    except Exception as e:
        print(f"An error occurred while finding the last message: {e}")

