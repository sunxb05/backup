#! python3
import pyautogui, sys

im = pyautogui.screenshot(region=(220,100, 500, 530))
# im.show()


im.save(str(sys.argv[1])+".png")

