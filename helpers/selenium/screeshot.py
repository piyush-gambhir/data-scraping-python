def take_full_page_screenshot(driver, file_name='full_screenshot.png'):
    """
    Takes a full-page screenshot by scrolling through the entire page.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        file_name (str): The file name to save the screenshot as.
    """
    total_height = driver.execute_script("return document.body.scrollHeight")
    driver.set_window_size(1920, total_height)  # Adjust width and height as needed
    driver.save_screenshot(file_name)
