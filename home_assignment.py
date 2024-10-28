import unittest

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy

capabilities = dict(
    platformName='Android',
    automationName='uiautomator2',
    deviceName='Android',
    appPackage='com.android.settings',
    appActivity='.Settings',
    language='en',
    locale='US'
)

appium_server_url = 'http://localhost:4723'


class TestAppium(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities))

        self.driver.implicitly_wait(5)

    def tearDown(self) -> None:
        if self.driver:
            self.driver.quit()

    def test_find_battery(self) -> None:
        el = self.driver.find_element(by=AppiumBy.XPATH, value='//*[@text="Battery"]')
        el.click()

        battery_text = self.driver.find_element(by=AppiumBy.XPATH,
                                                value='//android.widget.TextView[@resource-id="com.android.settings:id/usage_summary"]')

        assert battery_text.text == "100%"

        show_battery_percentage_toggle = self.driver.find_element(by=AppiumBy.XPATH,
                                                                  value='//android.widget.Switch[@resource-id="com.android.settings:id/switchWidget"]')
        show_battery_percentage_toggle.click()


if __name__ == '__main__':
    unittest.main()
