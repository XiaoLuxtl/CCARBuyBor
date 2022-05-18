import time
import re
import os
from random import random, randrange, uniform
from playsound import playsound
from datetime import datetime
import threading
import easyocr
import glob

from PIL import Image, ImageOps, ImageEnhance
from io import BytesIO

import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.color import Color
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.action_chains import ActionChains


if __name__ == '__main__':
    # GLOBALES
    DEBUG = 2
    STAMP = 0
    COST = 405
    reader = easyocr.Reader(['en'])  # this needs to run only once to load the model into memory

    # Ruta de los componentes
    CHROMEDRIVER_PATH = "X:\\SCRIPTS\\NFT\\plugins\\driver\\pchromedriver.exe"
    EXTENSION_PATH = "X:\\SCRIPTS\\NFT\\plugins\\driver\\extensions"
    # Pagina del jueguito
    CCAR_PAGE = "https://cryptocars.me/"
    # Ruta soniditos
    S_HORN = 'HORN.mp3'
    S_CHORD = 'C:\\Windows\\Media\\chord.wav'
    # Ruta archivos temporales Chrome
    TMP_CHROME = r'C:\SCRIPTS\Captcha\CCAR\CCARprofileLux'

    _METAMASK_PASSWORD = ""  # Pasword que se asignara al a cuenta
    _METAMASK_ID = "nkbihfbeogaeaoehlefnkodbefgpgknn"  # Es una mamada de chrome
    _METAMASK = "\\metamask-extension_10_0_3_0.crx"  # nombre de la extension
    _METAMASK_SEED = ""  # las millonarias

    _RED_NOMBRE = 'Binance'
    _RED_RPC = 'https://bsc-dataseed1.ninicoin.io/'
    _RED_CADENAID = '56'
    _RED_SIMBOLO = 'BNB'
    _RED_EXPLORADOR = 'https://bscscan.com'

    options = uc.ChromeOptions()
    options.add_argument(f'--no-first-run --no-service-autorun --password-store=basic')
    options.user_data_dir = f'{TMP_CHROME}'
    options.add_argument(f'--disable-gpu')
    options.add_argument(f'--no-sandbox')
    options.add_argument(f'--disable-dev-shm-usage')
    options.add_argument(f'--start-maximized')

    # driver = webdriver.Chrome(options=options, executable_path=patcher.executable_path)
    driver = uc.Chrome(
        options=options,
        headless=False)

    driver.set_page_load_timeout(10)
    
    # Main Handles
    if len(driver.window_handles) == 2:
        PARENT = driver.window_handles[0]
        CHILD = driver.window_handles[1]
        print(driver.window_handles)


    # FUNCIONES
    # log in a cartera ronin

    def _child_handle():
        driver.switch_to.window(PARENT)
        driver.execute_script("window.open('','_blank');")
        time.sleep(1)
        chwd = driver.window_handles

        for w in chwd:
            # switch focus to child window
            if w != PARENT:
                driver.switch_to.window(CHILD)
                time.sleep(0.25)
                return w


    def _clean_tabs():
        for handle in driver.window_handles:
            if handle != PARENT:
                if handle != CHILD:
                    driver.switch_to.window(handle)
                    time.sleep(0.25)
                    driver.close()
        driver.switch_to.window(PARENT)


    def _open_metamask_ID_tab():
        global CHILD
        driver.switch_to.window(CHILD)
        driver.get('chrome-extension://{}/popup.html'.format(_METAMASK_ID))
        driver.execute_script("document.body.style.width = '80vw';")


    def _metamask_login():
        global PARENT
        global CHILD
        try:
            _is_metatask = driver.title == "MetaMask"
            while not _is_metatask:
                try:
                    _open_metamask_ID_tab()
                    if driver.title == "MetaMask": _is_metatask = 1
                except:
                    print("Error con handles")
                    CHILD = driver.window_handles[1]
                    print(driver.window_handles)
                    driver.switch_to.window(CHILD)
                    print(driver.title)
                    time.sleep(0.5)

            WebDriverWait(driver, 10, 0.25).until(
                EC.presence_of_element_located((By.XPATH, '//button[text()="Empezar"]')))
            driver.find_element(by=By.XPATH, value='//button[text()="Empezar"]').click()

            WebDriverWait(driver, 10, 0.25).until(
                EC.presence_of_element_located((By.XPATH, '//button[text()="Importar cartera"]')))
            driver.find_element(by=By.XPATH, value='//button[text()="Importar cartera"]').click()

            # No, gracias
            WebDriverWait(driver, 10, 0.25).until(
                EC.presence_of_element_located((By.XPATH, '//button[text()="No, gracias"]')))
            driver.find_element(by=By.XPATH, value='//button[text()="No, gracias"]').click()
            # Llenamos cmapos input
            WebDriverWait(driver, 10, 0.25).until(EC.presence_of_element_located((By.XPATH, '//input')))
            inputs = driver.find_elements_by_xpath('//input')
            inputs[0].send_keys(_METAMASK_SEED)
            inputs[1].send_keys(_METAMASK_PASSWORD)
            inputs[2].send_keys(_METAMASK_PASSWORD)

            # Acepto terminos
            _xpath_acepto = '//*[@id="app-content"]/div/div[3]/div/div/form/div[7]/div'
            WebDriverWait(driver, 10, 0.25).until(EC.presence_of_element_located((By.XPATH, _xpath_acepto)))
            driver.find_element(by=By.XPATH, value=_xpath_acepto).click()

            # CLic importamos
            WebDriverWait(driver, 10, 0.25).until(
                EC.presence_of_element_located((By.XPATH, '//button[text()="Importar"]')))
            driver.find_element(by=By.XPATH, value='//button[text()="Importar"]').click()

            # Clic Todo Listo
            WebDriverWait(driver, 10, 0.25).until(
                EC.presence_of_element_located((By.XPATH, '//button[text()="Todo listo"]')))
            driver.find_element(by=By.XPATH, value='//button[text()="Todo listo"]').click()

            # Agregamos Binance
            # Cerramos popup
            _xpath_x_pop = '//*[@id="popover-content"]/div/div/section/header/div/button'
            WebDriverWait(driver, 10, 0.25).until(EC.presence_of_element_located((By.XPATH, _xpath_x_pop)))
            driver.find_element(by=By.XPATH, value=_xpath_x_pop).click()

            # Clic en cuenta
            _xpath_config = '//*[@id="app-content"]/div/div[1]/div/div[2]/div[2]'
            WebDriverWait(driver, 10, 0.25).until(EC.presence_of_element_located((By.XPATH, _xpath_config)))
            driver.find_element(by=By.XPATH, value=_xpath_config).click()

            # Clic en configuracion
            _xpath_config_opt = '//*[@id="app-content"]/div/div[4]/div[11]'
            WebDriverWait(driver, 10, 0.25).until(EC.presence_of_element_located((By.XPATH, _xpath_config_opt)))
            driver.find_element(by=By.XPATH, value=_xpath_config_opt).click()

            # Clic en redes
            driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/popup.html#settings')
            time.sleep(0.5)
            _xpath_redes = '//*[@id="app-content"]/div/div[4]/div/div[2]/div[1]/div/button[6]/div[1]/div[1]'
            WebDriverWait(driver, 10, 0.25).until(EC.presence_of_element_located((By.XPATH, _xpath_redes)))
            driver.find_element(by=By.XPATH, value=_xpath_redes).click()
            time.sleep(0.5)

            # Clic agregar red
            _clicked = 0

            while not _clicked:
                try:
                    driver.execute_script("document.body.style.width = '1024px';")
                    _xpath_agregar_red = '//*[@id="app-content"]/div/div[4]/div/div[2]/div[2]/div/div/div[2]/button'
                    WebDriverWait(driver, 10, 0.25).until(
                        EC.presence_of_element_located((By.XPATH, _xpath_agregar_red)))
                    time.sleep(0.5)
                    driver.find_element(by=By.XPATH, value=_xpath_agregar_red).click()
                    _clicked = 1
                except:
                    print('Clic en agregar red manualmente — Error Agregando la red')
                    time.sleep(0.25)
                    _clicked = 0

            # Get Inputs
            inputs = driver.find_elements_by_xpath('//input')
            inputs[0].send_keys(_RED_NOMBRE)
            inputs[1].send_keys(_RED_RPC)
            inputs[2].send_keys(_RED_CADENAID)
            inputs[3].send_keys(_RED_SIMBOLO)
            inputs[4].send_keys(_RED_EXPLORADOR)

            # Guardamos
            WebDriverWait(driver, 10, 0.25).until(
                EC.presence_of_element_located((By.XPATH, '//button[text()="Guardar"]')))
            driver.find_element(by=By.XPATH, value='//button[text()="Guardar"]').click()

            # Cleanup??
            time.sleep(1)
            _clean_tabs()
            if len(driver.window_handles) == 1:
                print("Entramos a crear nuevo tab dentro de metamask")
                driver.execute_script("window.open('','_blank');")
                driver.execute_script("window.open('','_blank');")
                PARENT = driver.window_handles[1]
                CHILD = driver.window_handles[2]
                print(driver.window_handles)
            return 1

        except Exception as e:
            print(e)
            return 0

        except:
            print("Error Login to Metamask")
            return 0


    def _wait_until_enter():
        try:
            input("Press enter to continue")
        except SyntaxError:
            time.sleep(0.1)
            pass


    def local_time():
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        print(current_time)


    # Funciones para la lógica
    def alert(soundpath: str):  # Daemon true significa que el thread se mata al final el proceso
        threading.Thread(target=playsound, args=(soundpath,), daemon=True).start()


    def getCssHexColor(obj):
        try:
            _color = obj.value_of_css_property("background-color")
            _color = Color.from_string(_color).hex  # HEX
            return _color
        except:
            return 0



    def winmaximize(window):
        # SW_MAXIMIZE = 3
        # windowHandle = ctypes.windll.user32.FindWindowW(None, window)
        # ctypes.windll.user32.ShowWindow(windowHandle, SW_MAXIMIZE)
        SetForegroundWindow(find_window(title='taskeng.exe'))


    def captchacheck():
        _modal_xpath = '/html/body/span[3]/div'
        _find_text = 'Captcha'
        _market_xpath = '//*[@id="33"]/img'
        _load_captcha_xpath = '//*[@id="loadcaptcha"]'

        _sleep_counter = 0
        _sleep = 0.1

        try:
            ignored_exceptions = (StaleElementReferenceException, ElementNotInteractableException,)
            _text = WebDriverWait(driver, 10, _sleep, ignored_exceptions=ignored_exceptions) \
                .until(EC.visibility_of_element_located((By.XPATH, _modal_xpath))).text
        except:
            return 0

        if _find_text in _text:
            if DEBUG >= 1: print("Captcha text found")
            try:
                WebDriverWait(driver, 5, 0.1, ignored_exceptions=ignored_exceptions) \
                    .until(EC.visibility_of_element_located((By.XPATH, _load_captcha_xpath))).click()
            except:
                return 0
            while True:
                try:
                    _text = WebDriverWait(driver, 5, 0.1, ignored_exceptions=ignored_exceptions) \
                        .until(EC.visibility_of_element_located((By.XPATH, _modal_xpath))).text
                    if _find_text in _text:
                        _sleep_counter = _sleep_counter + _sleep
                    else:
                        if DEBUG >= 1: print("ya no hay letrero recaptcha")
                        WebDriverWait(driver, 5, 0.1, ignored_exceptions=ignored_exceptions) \
                            .until(EC.visibility_of_element_located((By.XPATH, _market_xpath))).click()
                        if DEBUG >= 1: print("tratamos de abrir el mercado")
                        return 1
                    if _sleep_counter > 600:
                        return 0
                except:
                    break

        try:
            WebDriverWait(driver, 5, 0.1, ignored_exceptions=ignored_exceptions) \
                .until(EC.visibility_of_element_located((By.XPATH, _market_xpath))).click()
            return 1
        except:
            return 0


    def marketcheck():
        _market_xpath = '//*[@id="33"]/img'
        _text_loading = '/html/body/div[18]'
        _modal_xpath = '/html/body/span[3]/div'

        ignored_exceptions = (StaleElementReferenceException, ElementNotInteractableException,)
        try:
            WebDriverWait(driver, 4, 0.1, ignored_exceptions=ignored_exceptions) \
                .until(EC.visibility_of_element_located((By.XPATH, _market_xpath))).click()

            # Loading desaparece
            WebDriverWait(driver, 4, 0.1).until(EC.invisibility_of_element_located((By.XPATH, _text_loading)))

            # Modal aparece
            WebDriverWait(driver, 4, 0.1, ignored_exceptions=ignored_exceptions) \
                .until(EC.visibility_of_element_located((By.XPATH, _modal_xpath)))

            return 1
        except:
            return 0


    def btn_click(xpath):
        try:
            ignored_exceptions = (StaleElementReferenceException,)
            driver.execute_script("arguments[0].click();", WebDriverWait(
                driver, 1, _sleep, ignored_exceptions=ignored_exceptions).until(
                EC.visibility_of_element_located((By.XPATH, xpath))))
        except:
            pass


    def easy_ocr(imgpath):
        result = reader.readtext(imgpath, allowlist='2345678ABCDEFGHIJKLMNPQRSTUVWXYZabcdefghjkmnpqrstuxyz')
        print(f"image: {imgpath} \t {result}")
        return result[0][1]


    def take_screenshot(element, driver, filename='screenshot.png'):
        # _xpath_svg_paths = "//*[@id='confirm-buy-car']/div/div/div/form/div/div[1]/div/svg/"
        _xpath_svg_paths = "//[@id='confirm-buy-car']/div/div/div/form/div/div[1]/div/svg/*[name()='path']"

        # _paths = driver.find_elements_by_xpath(_xpath_svg_paths)
        # _paths = WebDriverWait(driver, 5, _sleep, ignored_exceptions=ignored_exceptions) \
        #     .until(EC.visibility_of_any_elements_located((By.XPATH, _xpath_svg_paths)))

        _svg = element.find_elements_by_xpath("//*[name()='svg']")
        _paths = element.find_elements_by_xpath("//*[name()='path']")
        
        for svg in _svg:
            driver.execute_script("arguments[0].style.width = '300'; return arguments[0];", svg)
            driver.execute_script("arguments[0].style.height = '150'; return arguments[0];", svg)
            

        # pre procesamos la imagen
        n = 1
        d = 4
        for path in _paths:
            _fill = path.get_attribute("fill")
            print(f"_fill: {_fill}")
            if _fill == 'none':
                driver.execute_script("arguments[0].style.visibility = 'hidden'; return arguments[0];", path)
            else:
                if (n % d) == 0: driver.execute_script("arguments[0].style.fill = '#000'; return arguments[0];", path)
                if (n % d) == 1: driver.execute_script("arguments[0].style.fill = '#00F'; return arguments[0];", path)
                if (n % d) == 2: driver.execute_script("arguments[0].style.fill = '#F00'; return arguments[0];", path)
                if (n % d) == 3: driver.execute_script("arguments[0].style.fill = '#F0F'; return arguments[0];", path)
                n += 1

        location = element.location_once_scrolled_into_view
        size = element.size
        png = driver.get_screenshot_as_png()  # saves screenshot of entire page

        im = Image.open(BytesIO(png))  # uses PIL library to open image in memory

        left = location['x']
        top = location['y']
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']

        im = im.crop((left, top, right, bottom))  # defines crop points
        enhancer = ImageEnhance.Contrast(im)
        enhancer.enhance(2)
        im.save(f"ss/temp.png")  # saves new cropped image
        fname = easy_ocr('ss/temp.png')
        im.save(f"ss/{fname}.png")  # saves new cropped image        
        return fname


    def Price():
        global STAMP
        global COST

        filename = "price.txt"

        _current_stamp = os.stat(filename).st_mtime
        if _current_stamp != STAMP:
            # File has changed, so do something...
            STAMP = _current_stamp
            f = open(filename, "r")
            content_list = f.readlines()
            f.close()
            COST = float(content_list[0])
            print(f"\nCOST: {COST}")


    #####################################
    ############# M A I N ###############
    #####################################

    # Metamask things
    def _start():
        time.sleep(1)
        _clean_tabs()
        CHILD = _child_handle()
        _clean_tabs()
        if _metamask_login():
            # Continua normal
            # driver.switch_to.window(PARENT)
            # driver.get(CCAR_PAGE)
            _clean_tabs()
            _open_metamask_ID_tab()

        _handles = [driver, PARENT, CHILD]
        return _handles


    # handles = _start()
    driver.get(CCAR_PAGE)
    print("ABRIR EL MERCADO")
    easy_ocr("ss/temp.png")
    _wait_until_enter()

    #####################################
    ############# L O O P ###############
    #####################################

    Price()
    ignored_exceptions = (StaleElementReferenceException,)

    # BTN COLOR CONST
    _color_cyan = '#129092'
    _color_cyan2 = '#0f6567'
    _color_orange = '#bd651f'

    # money counter sleep totalusd
    _sleep = 0.1
    _loop = [0, 0, 0, 0, 0, 0]
    _retry = 0
    _t_profit = 0

    # Algunas constantes del loop
    # El chido CCAR

    _xpath_btn_refresh = '//*[@id="app"]/div[2]/div[1]/div/div/div[1]/div/div[3]/button'
    _xpath_element_one = '//*[@id="app"]/div[2]/div[2]/div[1]/div/div[1]/div[1]'
    _xpath_balance = '//*[@id="navbarNavAltMarkup"]/div[2]/a/span[1]'

    # -------------------------

    while 1:
        Price()
        _prev_balance = _loop[5]
        i = 0
        try:
            WebDriverWait(driver, 5, _sleep, ignored_exceptions=ignored_exceptions) \
                .until(EC.visibility_of_element_located((By.XPATH, _xpath_element_one)))
            
            try:            
                _loop[5] = WebDriverWait(driver, 1, _sleep, ignored_exceptions=ignored_exceptions) \
                        .until(EC.presence_of_element_located((By.XPATH, _xpath_balance))).text
            except:
                pass

            while i <= 3:
                i += 1
                _xpath_elements = f'//*[@id="app"]/div[2]/div[2]/div[1]/div/div[1]/div[{i}]'
                _xpath_btn_compra = f'/html/body/div[1]/div[2]/div[2]/div[1]/div/div[1]/div[{i}]/div/div[6]/div/button'

                _text = WebDriverWait(driver, 1, _sleep, ignored_exceptions=ignored_exceptions) \
                    .until(EC.presence_of_element_located((By.XPATH, _xpath_elements))).text

                # 13 lineas de texto
                _text = _text.splitlines()
                _type = _text[4]
                _level = int(re.findall(r"[-+]?\d*\.\d+|\d+", _text[7])[0])
                _price = _text[13].replace(",", "")
                _price = float(re.findall(r"[-+]?\d*\.\d+|\d+", _text[13])[0])

                if i == 1:
                    _loop[1] = _type
                    _loop[2] = _level
                    _loop[3] = _price

                if "Super Car" in _type:                
                    COST = COST*1.33                    
                    STAMP = 0       
                    print(f"\nsCOST: {COST}")                    
                if "Rare" in _type:
                    COST = COST*1.5
                    STAMP = 0                    
                    print(f"\nrCOST: {COST}")
                if "Legendary" in _type:                
                    COST = COST*2                    
                    STAMP = 0       
                    print(f"\nlCOST: {COST}")

                if _price <= COST:
                    Price()
                    _xpath_compra = f'/html/body/div[1]/div[2]/div[2]/div[1]/div/div[1]/div[{i}]/div/div[6]/div/button'
                    _xpath_input_captcha = '//*[@id="captcha"]'
                    _xpath_img_captcha = '//*[@id="confirm-buy-car"]/div/div/div/form/div/div[1]'
                    _xpath_modal_buy = '//*[@id="confirm-buy-car"]/div/div'
                    _xpath_modal_close = '//*[@id="confirm-buy-car"]/div/div/div/button'

                    alert(S_HORN)

                    # TEST
                    # print(driver.title)
                    # winmaximize(driver.title)
                    # driver.minimize_window()
                    # driver.fullscreen_window()
                    
                    now = datetime.now()
                    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                    print(f"\n--- {dt_string} ---")
                    print(f"_type: {_type} \t _level: {_level} \t _price: {_price}")

                    _loop[0] = 0

                    try:
                        btn_click(_xpath_compra)
                        WebDriverWait(driver, 0.3, _sleep) \
                            .until(EC.presence_of_element_located((By.XPATH, _xpath_img_captcha)))
                    except StaleElementReferenceException:
                        print("StaleElementReferenceException")
                        i -= 1
                        continue
                    except:                        
                        print("no _xpath_img_captcha retry")
                        i -= 1
                        continue

                    # SS Captcha
                    try:
                        time.sleep(0.3)
                        WebDriverWait(driver, 5, _sleep, ignored_exceptions=ignored_exceptions) \
                            .until(EC.visibility_of_element_located((By.XPATH, _xpath_img_captcha)))\
                            .screenshot("ss.png")

                        _keys = take_screenshot(WebDriverWait(driver, 5, _sleep, ignored_exceptions=ignored_exceptions) \
                            .until(EC.visibility_of_element_located((By.XPATH, _xpath_img_captcha))), driver,"test.png")

                    except:
                        _keys = '0'
                        print("error ss")
                    
                    # Enviar un enter  
                    if len(_keys) == 4:
                        btn_click(_xpath_input_captcha)
                        __input = WebDriverWait(driver, 5, _sleep, ignored_exceptions=ignored_exceptions) \
                                .until(EC.visibility_of_element_located((By.XPATH, _xpath_input_captcha)))

                        action = ActionChains(driver)
                        action.move_to_element(__input).click().perform()
                        __input.send_keys(_keys)
                        __input.send_keys(Keys.RETURN)                       
                    else:
                        print("\n4 digits error")
                        btn_click(_xpath_modal_close)
                        WebDriverWait(driver, 1, _sleep, ignored_exceptions=ignored_exceptions) \
                        .until(EC.invisibility_of_element_located((By.XPATH, _xpath_input_captcha)))
                        i -= 1
                        continue

                    # if float(_loop[5]) > COST:
                        # _wait_until_enter()
                        
                    break
                
                # Resetear el precio chingado
                Price()
                
            _retry = 0


        except Exception as e:
            if DEBUG >= 1: print(e)
            if _retry < 30:
                _retry += 1
                print(f"_retry: {_retry}")
                time.sleep(5)
                try: 
                    driver.get('https://cryptocars.me/')
                    driver.get('https://cryptocars.me/play/#/marketplace')
                    driver.refresh()
                except:
                    pass
                time.sleep(5)                               
                continue
            alert(S_CHORD)
            _wait_until_enter()

        finally:
            _loop[0] += 1
            _loop[4] = uniform(2, 4)
            print(f'\r i: {_loop[0]} \t _type: {_loop[1]} \t _level: {_loop[2]} \t _price: {_loop[3]} \t zzz: {round(_loop[4], 2)} \t CCAR: {_loop[5]}', end="")
            time.sleep(_loop[4])
            btn_click(_xpath_btn_refresh)
