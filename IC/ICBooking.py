import time

from CredentialsIC import CredentialsIC
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select


class ICBooking:
    """
    This class is responsible for booking train tickets based on: starting point, destination, day and time.
    """

    def __init__(self, destination_from: str, destination_to: str, when_date: str, when_hours: str,
                 return_when_date: str, return_when_hours: str):
        # get website by driver chrome
        self.driver = webdriver.Chrome('./chromedriver')
        self.driver.get("https://bilet.intercity.pl/logowanie.jsp")
        self.destination_from = destination_from
        self.destination_to = destination_to
        self.when_date = when_date
        self.when_hours = when_hours
        self.return_when_date = return_when_date
        self.return_when_hours = return_when_hours

    def log(self):
        # log on company IC account using dataclass
        self.driver.implicitly_wait(1)
        self.driver.find_element("xpath", '//*[@id="content"]/div[1]/div[2]/div/div[1]/ul/li[2]/a').click()
        login = self.driver.find_element("xpath", '//*[@id="icWebUserLogin"]/div[1]/fieldset/input')
        login.click()
        login.send_keys(CredentialsIC.login)
        password = self.driver.find_element("xpath", '//*[@id="icWebUserLogin"]/div[2]/fieldset/input')
        password.click()
        password.send_keys(CredentialsIC.password)
        self.driver.find_element("xpath", '//*[@id="icWebUserLogin"]/div[5]/input').click()

        # looking for connection - w8 for dates,hour and from where to where data
        self.driver.find_element("xpath", '//*[@id="content"]/div[1]/div[2]/div/div[1]/ul/li[4]/a').click()

    def change_connection_data(self):
        """
        definition of master data
        """
        destination_from = input("Skąd chciałbyś jechać?")  # Swarzędz
        destination_to = input("Dokąd chciałbyś jechać?")  # Warszawa Zachodnia
        when_date = input("Kiedy? (yyyy-mm-dd)")  # '2022-12-07'
        when_hours = input("O jakiej godzinie? (hh:mm)")  # '05:00'
        return_when_date = input("Kiedy chcesz wrócić? (yyyy-mm-dd)")  # '2022-12-08'
        return_when_hours = input("O jakiej godzinie powrót? (hh:mm)")  # '17:00'

        self.destination_from = destination_from
        self.destination_to = destination_to
        self.when_date = when_date
        self.when_hours = when_hours
        self.return_when_date = return_when_date
        self.return_when_hours = return_when_hours

    def _get_return_connection_data(self):
        """
        set new walue for pkp search form
        """
        # get another ticket
        self.driver.find_element("xpath", '//*[@id="print_area"]/div/div/table/tbody/tr[3]/td/input').click()

        # take value of next day
        # date = datetime.strptime(self.when_date, "%Y-%m-%d")
        # modified_date = date + timedelta(days=1)
        # self.when_date = datetime.strftime(modified_date, "%Y-%m-%d")

        # set new value
        self.when_date = self.return_when_date
        self.when_hours = self.return_when_hours
        self.destination_from, self.destination_to = self.destination_to, self.destination_from

    def _is_connection_available(self):
        """
        check if such a connection exists, looking for the element that appears when the connection is not established
        """
        try:
            self.driver.find_element("xpath", '//*[@id="doBT"]/button').click()
        except NoSuchElementException:
            pass

    def retunr_ticket(self):
        """
        make action for return tickets
        """
        self._get_return_connection_data()
        self.pkp_search_form()
        self.pkp_choose_seat_form()
        self.driver.find_element("xpath", '//*[@id="dodaj-do-koszyka-button"]').click()

    def pkp_search_form(self):
        """
        this function is filling search form, using data that we provide at the beginning and mark directly connection
        """
        time.sleep(2)
        from_form = self.driver.find_element("xpath", '//*[@id="stname-0"]')
        to_form = self.driver.find_element("xpath", '//*[@id="stname-1"]')
        when_date_form = self.driver.find_element("xpath", '//*[@id="date_picker"]')
        when_hours_form = self.driver.find_element("xpath", '//*[@id="ic-seek-time"]')

        # clear and fill form,  click ,,połączenie bezpośrednie" and search
        time.sleep(1)
        from_form.click()
        from_form.clear()
        from_form.send_keys(self.destination_from)
        time.sleep(2)
        from_form.send_keys(Keys.DOWN)
        from_form.send_keys(Keys.RETURN)

        time.sleep(1)
        to_form.click()
        to_form.clear()
        to_form.send_keys(self.destination_to)
        time.sleep(2)
        to_form.send_keys(Keys.DOWN)
        to_form.send_keys(Keys.RETURN)

        time.sleep(1)
        when_date_form.send_keys(Keys.CONTROL, 'a')
        when_date_form.send_keys(self.when_date)
        when_date_form.send_keys(Keys.ENTER)
        when_date_form.click()

        time.sleep(2)
        when_hours_form.send_keys(Keys.CONTROL, 'a')
        when_hours_form.send_keys(self.when_hours)
        when_hours_form.send_keys(Keys.ENTER)

        # scroll and confirm form
        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(2)
        # directly
        self.driver.find_element("xpath", '//*[@id="searchTrainForm"]/div[1]/div[4]/fieldset/div[1]/label').click()
        self.driver.find_element("xpath", '//*[@id="searchTrainForm"]/div[3]/div[2]/button').click()

    # choose train and class and discount
    def pkp_choose_seat_form(self):
        """
        this function is filling form for seat, it choose discount bilet for students and seats near window
         in compartment without cabin
        """
        self._is_connection_available()

        selector_normal_nb = self.driver.find_element("xpath", '//*[@id="liczba_n"]')
        selector_normal_nb = Select(selector_normal_nb)
        selector_normal_nb.select_by_value('0')

        time.sleep(2)
        selector_discount_nb = self.driver.find_element("xpath", '//*[@id="liczba_u"]')
        selector_discount_nb = Select(selector_discount_nb)
        selector_discount_nb.select_by_value('1')

        time.sleep(1)

        selector_discount = self.driver.find_element("xpath", '//*[@id="kod_znizki"]')
        selector_discount = Select(selector_discount)
        selector_discount.select_by_value('99')  # 51% stydencka do 26 roku

        selector_compartment = self.driver.find_element("xpath", '//*[@id="rodzaj_wagonu"]')
        selector_compartment = Select(selector_compartment)
        selector_compartment.select_by_value('2')  # wagon bez przedziałów

        selector_seat = self.driver.find_element("xpath", '//*[@id="usytuowanie"]')
        selector_seat = Select(selector_seat)
        selector_seat.select_by_value('1')  # okno

        self.driver.find_element("xpath", '//*[@id="strefa_modal"]').click()

        # check and confirm ticket
        time.sleep(2)
        self.driver.find_element("xpath",
                                 '//*[@id="formPodgladBiletu"]/div[4]/div/div[2]/div/div[2]/div/div[1]/div[4]/div/div').click()

    def main(self):
        self.log()
        self.pkp_search_form()
        self.pkp_choose_seat_form()
        self.retunr_ticket()


if __name__ == '__main__':
    # initialize data
    destination_from = input("Skąd chciałbyś jechać?")  # Swarzędz
    destination_to = input("Dokąd chciałbyś jechać?")  # Warszawa Zachodnia
    when_date = input("Kiedy? (yyyy-mm-dd)")  # '2022-12-07'
    when_hours = input("O jakiej godzinie? (hh:mm)")  # '05:00'
    return_when_date = input("Kiedy chcesz wrócić? (yyyy-mm-dd)")  # '2022-12-08'
    return_when_hours = input("O jakiej godzinie powrót? (hh:mm)")  # '17:00'
    ic = ICBooking(destination_from, destination_to, when_date, when_hours, return_when_date, return_when_hours)
    ic.main()
