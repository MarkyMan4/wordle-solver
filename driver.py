from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from guesser import WordleGuesser

# keep browser open when finished
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(executable_path='drivers/chromedriver', chrome_options=chrome_options)
driver.get('https://www.nytimes.com/games/wordle/index.html')

# close tutorial window
tutorial_section = driver.execute_script('''
    return document
        .querySelector("game-app")
        .shadowRoot
        .querySelector("game-modal")
        .shadowRoot
''')

tutorial_section.find_element(by=By.CLASS_NAME, value='close-icon').click()
# game_section.find_element(By.ID, value='game')

time.sleep(1)

keyboard_section = driver.execute_script('''
    return document
        .querySelector("game-app")
        .shadowRoot
        .querySelector("game-keyboard")
        .shadowRoot
''')

keyboard = keyboard_section.find_element(by=By.ID, value='keyboard')

# make a guess
guesser = WordleGuesser()

for i in range(6):
    guess = guesser.guess_word()

    for c in guess:
        keyboard.find_element(by=By.CSS_SELECTOR, value=f"button[data-key='{c}']").click()

    # press the enter key
    keyboard.find_element(by=By.CLASS_NAME, value='one-and-a-half').click()

    time.sleep(3)

    # see the result of each letter
    result = []
    is_correct = True
    for c in guess:
        res = keyboard.find_element(by=By.CSS_SELECTOR, value=f"button[data-key='{c}']").get_attribute('data-state')
        result.append(res)

        if res != 'correct':
            is_correct = False

    guesser.set_guess_result(result)
    
    if is_correct:
        break

    
