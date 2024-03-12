from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from item_list import item_list_3
from selenium.webdriver.common.keys import Keys
import itertools
from webdriver_manager.chrome import ChromeDriverManager

class ChromeDriver:
    """creates chromedriver so selenium can  be initiated and interact with website"""

    def __init__(self, url, username, password):
        self.username = username
        self.password = password
        # self.chrome_driver_path = Service(fr"C:\Users\zebdu\Downloads\chromedriver_win32 (1)\chromedriver.exe")
        # self.op = webdriver.ChromeOptions()
        # self.driver = webdriver.Chrome(service=self.chrome_driver_path, options=self.op)
        # self.wait = WebDriverWait(self.driver, 10)  # Initialize WebDriverWait object
        #
        # self.driver.get(url)
        # self.driver.maximize_window()
        # self.wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body')))

        self.op = webdriver.ChromeOptions()
        self.op.add_argument("--start-maximized")
        chrome_driver_path = ChromeDriverManager().install()
        self.driver = webdriver.Chrome(executable_path=chrome_driver_path, options=self.op)
        self.wait = WebDriverWait(self.driver, 10)  # Initialize WebDriverWait object

        self.driver.get(url)
        self.wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body')))

    def login(self):
        login_page = self.wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/a[2]/button")))
        login_page.click()
        self.wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body')))

    def fill_fields(self):
        fill_username = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
        fill_password = self.wait.until(EC.presence_of_element_located((By.NAME, "password")))
        fill_username.send_keys(self.username)
        fill_password.send_keys(self.password)


        login_button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "login-button")))
        login_button.click()

        self.wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body')))

        self.handle_popup()

        time.sleep(2)

        self.click_neopets_home()

        time.sleep(3)

    def handle_popup(self):
        try:
            # Waiting for the popup to be visible
            popup_close_button = self.wait.until(
                EC.visibility_of_element_located((By.CLASS_NAME, "btn-close-popup.astro-YZJ7DDZN")))
            # Clicking the close button
            popup_close_button.click()
        except TimeoutException:
            # No popup appeared within the wait limit
            pass

    def click_neopets_home(self):
        try:
            # Waiting for the Neopets home link to be clickable
            neopets_home_link = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/header/div/nav/div/a[1]")))
            # Clicking the link
            neopets_home_link.click()

            # Waiting for the new tab to open
            WebDriverWait(self.driver, 10).until(lambda d: len(d.window_handles) > 1)

            # Switch to the new tab (which will be the last one in window_handles list)
            self.driver.switch_to.window(self.driver.window_handles[-1])

            # As we have switched to a new tab, we must also wait for the page to load
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body')))

        except TimeoutException:
            # The Neopets home link didn't become clickable within the wait limit
            pass

    def birthday_form(self, month, day, year):
        select_month = Select(self.wait.until(EC.presence_of_element_located((By.ID, "dob_m"))))
        select_month.select_by_value(f"{month}")

        select_day = Select(self.wait.until(EC.presence_of_element_located((By.ID, "dob_d"))))
        select_day.select_by_value(f"{day}")

        select_year = Select(self.wait.until(EC.presence_of_element_located((By.ID, "dob_y"))))
        select_year.select_by_value(f"{year}")

        submit_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[2]/button")))
        submit_button.click()

        self.wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body')))

    def shop_url(self, url):
        self.driver.get(url)

    def search_for_item(self):
        """this is for bidding on store items *DEPRECATED*"""
        self.driver.get(url="https://www.neopets.com/objects.phtml?type=shop&obj_type=37")
        time.sleep(.25)
        check_current_balance = self.driver.find_element(By.CLASS_NAME, "np-text__2020")
        remove_comma = check_current_balance.text.split(",")
        concantenate_splits = int(remove_comma[0]+remove_comma[1])
        if concantenate_splits < 30000:
            add_money = self.driver.find_element(By.XPATH, "/html/body/div[9]/a[1]/div/span")
            add_money.click()
            time.sleep(2)
            pin = "6812"
            enter_pin = self.driver.find_element(By.XPATH, "/html/body/div[12]/div[3]/div[3]/div[2]/div[2]/form/div[1]/input")
            enter_pin.send_keys(pin)
            time.sleep(.25)
            withdrawal_amount = self.driver.find_element(By.XPATH, "/html/body/div[12]/div[3]/div[3]/div[2]/div[2]/form/div[2]/input[1]")
            withdrawal_str = "30000"
            withdrawal_amount.send_keys(withdrawal_str)
            time.sleep(.1)
            withdrawal_button = self.driver.find_element(By.XPATH, "/html/body/div[12]/div[3]/div[3]/div[2]/div[2]/form/div[2]/input[2]")
            withdrawal_button.click()
            alert = self.driver.switch_to.alert
            time.sleep(.1)
            alert.accept()
            print("current amount was less $30,000, $50,000 was withdrawn")
            time.sleep(.5)
            self.driver.back()
        else:
            print(f"current amount is {concantenate_splits}, no money withdrawn")
        #current_items_name_list = self.driver.find_elements(By.CLASS_NAME, 'item-name')
        current_items_name_list = self.driver.find_elements(By.CLASS_NAME, 'shop-item')
        item_details = []
        item_price = []
        for item in current_items_name_list:
            item_details.append(item.text.split('\n')[0])
            item_price.append(item.text.split('\n')[2])
            #if item in item_list_2:
                #time.sleep(.25)
        #print(item_price)
        temp_name_list = []
        temp_price_list = []
        for item in item_details:
            split_name = item.split("\n")[0]
            temp_name_list.append(split_name)
        for item in item_price:
            split_price_1 = item.split(" ")[1]
            split_price_2 = split_price_1.split(" ")[0]
            if "," in item:
                split_price_3 = split_price_2.split(",")
                #print(split_price_3)
                time.sleep(1)
                conc_price = int(split_price_3[0]+split_price_3[1])
                temp_price_list.append(int(conc_price))
                #print(item_price)
            else:
                temp_price_list.append(split_price_2)

        is_true = True
        while is_true:
            for name in temp_name_list:
                if name in item_list_3:
                    #playsound.playsound(fr"C:\Users\zebdu\Downloads\mixkit-system-beep-buzzer-fail-2964.wav")
                    index = temp_name_list.index(name)
                    print(name)
                    item_button = self.driver.find_element(By.XPATH, f'//*[@id="container__2020"]/form[2]/div/div[{index + 1}]/div')
                    item_button.click()
                    time.sleep(.25)
                    are_you_sure_b = self.driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/button")
                    are_you_sure_b.click()
                    time.sleep(.25)
                    haggle_input = self.driver.find_element(By.XPATH, "/html/body/div[11]/form/div/input")
                    haggle_input.send_keys(Keys.BACKSPACE)
                    price_to_offer = int(temp_price_list[index]) + 30
                    haggle_input.send_keys(f"{str(price_to_offer)}")
                    self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                    time.sleep(2.5)
                    self.driver.get(url="https://www.neopets.com/objects.phtml?type=shop&obj_type=37")
                else:
                    time.sleep(2)
                    self.driver.refresh()
        time.sleep(2)
        self.driver.refresh()

    def search_names(self, template, name_length, is_capitalize, is_double_letter, file_path, number_of_names, time_interval):
        """for searching for unused names using a variety of parameters"""
        print("stage 1")
        try:
            start_time = time.time()  # Start time of the process
            total_names_checked = 0  # Counter for total names checke
            print('stage 2')


            # Wait for the specific element to be visible and store the element
            element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="container__2020"]/div[2]/div[3]/div/div/div/div[5]/div/div[1]')))

            # Click the element
            element.click()


            print('stage 3')
            print("Clicked 'Add a Neopet!'")

            create_new = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH,
                                                                                          "//button[contains(text(), 'Create a Neopet') and @tabindex='0' and contains(@class, 'button-default__2020') and contains(@class, 'button-blue__2020') and @onclick=\"location.href = '/reg/page4.phtml'\"]")))
            create_new.click()
            print("Clicked 'Create a Neopet'")


            num = 0
            num_2 = 0
            for name in self.generate_names(template):
                total_names_checked += 1

                time.sleep(time_interval)

                print(f"Checking name: {name}")
                if is_double_letter and not any(a == b for a, b in zip(name, name[1:])):
                    continue  # skip names that don't contain double letters
                if is_capitalize:
                    name = name.capitalize()


                # Wait until the input field is located, clear it, and then input the name
                input_field = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "neopet_name")))
                self.driver.execute_script("arguments[0].scrollIntoView();", input_field)
                input_field.clear()
                input_field.send_keys(name)


                time.sleep(1)
                # Click outside the input field to trigger validation
                body = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//body")))
                self.driver.execute_script("arguments[0].scrollIntoView();", body)
                body.click()

                time.sleep(.35)

                try:
                    # Wait for the error_container to be populated with "taken" or "available" (adjust the timeout as needed)
                    error_container = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.ID, "error_container")))

                    # Check if the name is available or taken
                    if "taken" in error_container.get_attribute("innerHTML"):
                        print(f"The name {name} is taken.")
                        num_2 += 1
                    elif "available" in error_container.get_attribute("innerHTML"):
                        print(f"The name {name} is available!")
                        with open(file_path, "a") as file:
                            file.write(name + "\n")
                        num += 1

                        # If the number of names added to the file reaches the maximum, stop
                        if num >= number_of_names:
                            break
                    else:
                        raise Exception(
                            f"Unexpected message for name {name}: {error_container.get_attribute('innerHTML')}")
                except TimeoutException:
                    print(f"TimeoutException occurred while checking the name {name}. Skipping...")
                    continue
                except Exception as e:
                    print(f"An error occurred while checking the name {name}. Skipping... Error: {e}")
                    continue

            print(
                f"Taken Number: {num_2}\nAvailable Number: {num}\nTotal Count: {num + num_2}\nPercentage Available from Search: {(num + num_2) / num_2}")

        except NoSuchElementException:
            print("Unable to locate element. Please verify the XPath.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def generate_names(self, template):
        slots = template.count('-')  # counts number of empty slots in template
        for combination in itertools.product('abcdefghijklmnopqrstuvwxyz', repeat=slots):
            name = list(template)  # convert the template string to a list
            for c in combination:
                index = name.index('-')  # find the first space in the list
                name[index] = c  # replace it with the current character from combination
            yield "".join(name).replace(" ", "")  # join the list back into a string, remove spaces and yield it

    def index_nth(self, lst, element, n):
        indices = [i for i, x in enumerate(lst) if x == element]
        if n < len(indices):
            return indices[n]
        else:
            raise ValueError('Index out of range')

    def valid_name(self, name, is_capitalize, is_double_letter):
        if is_capitalize and not name[0].isupper():
            return False
        if is_double_letter and not any(a == b for a, b in zip(name, name[1:])):
            return False
        return True

    def browser_close(self):
        self.driver.quit()




