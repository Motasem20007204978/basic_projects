from selenium import webdriver
from io import BytesIO
from PIL import Image
from selenium.webdriver.firefox.options import Options

OPTIONS = Options.add_argument('--headless')


def init_driver(browser:str):
	if browser == 'firefox':
		return __init_firefox()
	elif browser == 'chrome':
		return __init_chrome()
	else:
		print('browser not supported')
		exit()

def __init_firefox():
	print('initializing browser...')
	try:
		return webdriver.Firefox()
	except:
		print('driver does not exist')
		exit()

def __init_chrome():
	print('initializing browser...')
	try:
		return webdriver.Chrome()
	except:
		print('driver does not exist')
		exit()


def __conv_rgba_to_rgb(img):
    # convert rgba to rgb
    _rgba = Image.open(img)
    _rgb = Image.new('RGB', _rgba.size, (255, 255, 255))
    _rgb.paste(_rgba, mask=_rgba.split()[3])
    return _rgb


def get_screenshots_for_imgs(imgs):

    list_bytes = []

    for img in imgs:
        png = BytesIO(img.screenshot_as_png)
        png = __conv_rgba_to_rgb(png)
        list_bytes.append(png)
	
    return list_bytes


def convert_imgs_list_into_pdf(bytes_imgs:list, pdf_file):
    bytes_imgs[0].save(pdf_file, save_all=True, append_images=bytes_imgs[1:])
    print(bytes_imgs.__len__(), 'images stored as pdf successfully')


def save_images_to_pdf(images, pdf):
    #save images to pdf
    print('\nsaving images to pdf...')
    screenshots = get_screenshots_for_imgs(images)
    convert_imgs_list_into_pdf(screenshots, pdf)



	