def configure_download(driver, download_directory):
    """
    Configures the browser to automatically download files to a specific directory.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        download_directory (str): Path to the directory where files will be downloaded.
    """
    driver.command_executor._commands['send_command'] = (
        'POST', '/session/$sessionId/chromium/send_command')
    params = {
        'cmd': 'Page.setDownloadBehavior',
        'params': {
            'behavior': 'allow',
            'downloadPath': download_directory
        }
    }
    driver.execute('send_command', params)
