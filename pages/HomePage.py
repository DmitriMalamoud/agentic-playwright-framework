from pages.BasePage import BasePage

class HomePage(BasePage):
    URL = "https://www.demoblaze.com/"
    
    # Locators
    CATEGORIES_HEADER = "#cat"
    PHONES_LINK = "//a[text()='Phones']"
    LAPTOPS_LINK = "//a[text()='Laptops']"
    MONITORS_LINK = "//a[text()='Monitors']"
    PRODUCT_CONTAINER = "#tbodyid"

    def open(self):
        self.navigate_to(self.URL)

    def verify_categories_visible(self):
        assert self.is_visible(self.CATEGORIES_HEADER), "Categories header not visible"
        assert self.is_visible(self.PHONES_LINK), "Phones link not visible"
        assert self.is_visible(self.LAPTOPS_LINK), "Laptops link not visible"
        assert self.is_visible(self.MONITORS_LINK), "Monitors link not visible"

    def get_products_content(self):
        """Returns the inner HTML of the product container to track state."""
        return self.page.inner_html(self.PRODUCT_CONTAINER)

    def click_monitors(self):
        self.click_element(self.MONITORS_LINK)

    def wait_for_products_to_load(self):
        """Waits for the product container to be visible."""
        self.wait_for_selector(self.PRODUCT_CONTAINER)
