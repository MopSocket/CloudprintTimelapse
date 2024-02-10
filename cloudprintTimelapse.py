from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import glob
import math
import time
import os
import PIL
from PIL import Image

startTime_date = datetime.now()
startTime = startTime_date.strftime("%Y-%m-%d_%H-%M-%S")
print(f"Print Start Time: {startTime}")

outputHomePath = "C:\\TEMP\\CloudprintTimelapses"
outputPath = f"{outputHomePath}\\{startTime}"

os.mkdir(outputPath)


driver = webdriver.Chrome()

driver.get("https://login.makerbot.com/login")

title = driver.title
#assert title == "Web form"

driver.implicitly_wait(5)

username_box = driver.find_element(by=By.ID,value="username")
password_box = driver.find_element(by=By.ID,value="password")
login_button = driver.find_element(by=By.CLASS_NAME,value="button-primary")
username_box.send_keys("<Your email here>")
password_box.send_keys("<Your Password here>")
login_button.click()

driver.implicitly_wait(30)

status = 'Idle'

i=0
while status != 'Completed':
	i = i+1
	nowTime_date = datetime.now()
	nowTime = nowTime_date.strftime("%Y-%m-%d_%H-%M-%S")
	nowTime_cli = nowTime_date.strftime("%H:%M:%S")
	elapsedSeconds = (nowTime_date-startTime_date).total_seconds()
	elapsedDays = elapsedSeconds/86400
	elapsedHours = elapsedSeconds/3600
	elapsedMinutes = elapsedSeconds/60
	totalElapsedDays = math.floor(elapsedDays)
	totalElapsedHours = math.floor(elapsedHours) - totalElapsedDays*24
	totalElapsedMinutes = math.floor(elapsedMinutes) - totalElapsedHours*60 - totalElapsedDays*1440
	totalElapsedSeconds = elapsedSeconds - totalElapsedMinutes*60 - totalElapsedHours*3600 - totalElapsedDays*86400



	statusElement = driver.find_element(by=By.CLASS_NAME,value="status-text")
	status = statusElement.text


	with open(f"{outputPath}\\{nowTime}.png","wb") as file:
		image = driver.find_element(by=By.CLASS_NAME,value="card-img-top")
		file.write(image.screenshot_as_png)

		if status == 'Printing':
			completionElement = driver.find_element(by=By.CLASS_NAME,value="percent")
			percentageCompletion = completionElement.text
			print(f"{nowTime_cli}, Screenshot {i} saved.\tPrinter Status: {status} ({percentageCompletion} Complete)\tTime Elapsed: {totalElapsedDays} dy, {totalElapsedHours} hr, {totalElapsedMinutes} min, and {totalElapsedSeconds:>.0f} s.")
		else:
			print(f"{nowTime_cli}, Screenshot {i} saved.\tPrinter Status: {status}\tTime Elapsed: {totalElapsedDays} days, {totalElapsedHours} hours, {totalElapsedMinutes} minutes, and {totalElapsedSeconds:>.0f} seconds.")




	time.sleep(90)

print("Print Complete! Making Animation")
img = []
for filename in glob.glob(f"{outputPath}\\*.png"):
	im = Image.open(filename)
	img.append(im)

img[0].save(f"{outputPath}\\PrintAnimation_{startTime}.gif",save_all=True,append_images=img[1:],optimize=False,duration=33,loop=0) # duration in ms; 33 = ~30fps