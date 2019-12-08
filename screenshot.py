from selenium import webdriver
import json
import os
import requests
import time

def determine_screenshot_filename(uuid):
	return os.getenv("WWW2PNG_SCREENSHOT_DIR") + "/" + str(uuid) + ".png"

def generate_screenshot(uuid, settings):
	url = settings["url"]
	screenshot_filename = determine_screenshot_filename(uuid)
	window_x = settings["width"]
	window_y = settings["height"]

	try:
		options = webdriver.ChromeOptions()
		options.add_argument("--ignore-certificate-errors")
		options.add_argument("--headless")
		options.add_argument("--incognito")
		options.add_argument("--hide-scrollbars")
		options.binary_location = "/usr/bin/google-chrome"

		driver = webdriver.Chrome(chrome_options=options)
		driver.set_page_load_timeout(int(os.getenv("SELENIUM_TIMEOUT")))
		driver.set_window_position(0, 0)
		driver.set_window_size(window_x, window_y)
		driver.get(url)

		if settings["fullPage"] == True:
			current_x = 0
			current_y = 0
			for x in range(0, settings["fullPageMaxLoops"]):
				required_width = driver.execute_script("return Math.max(document.body.scrollWidth, document.body.offsetWidth, document.documentElement.clientWidth, document.documentElement.scrollWidth, document.documentElement.offsetWidth)")
				required_height = driver.execute_script("return Math.max(document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight)")
				window_x = min(required_width, settings["maxWidth"])
				window_y = min(required_height, settings["maxHeight"])
				if current_x == window_x and current_y == window_y:
					break
				else:
					current_x = window_x
					current_y = window_y
					driver.set_window_size(window_x, window_y)

		if settings["delay"] > 0:
			time.sleep(settings["delay"])
		elif settings["fullPage"] == True:
			time.sleep(1)

		driver.save_screenshot(screenshot_filename)
	except Exception as e:
		raise e
	finally:
		driver.quit()
