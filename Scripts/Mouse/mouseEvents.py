import pyautogui as py


def doubleClickTarget(pos, duration, ):
    py.moveTo(pos, duration=duration)
    py.click()
    py.click()


def clickTo(pos, duration=0.1):
    py.moveTo(pos, duration=duration)
    py.click()


def rightClickTo(pos, duration=0.1):
    py.moveTo(pos, duration=duration)
    py.rightClick()


def clickTarget(pos, duration=0.1):
    py.moveTo(pos, duration=duration)
    py.click()


def holdAndGrapTarget(firstPosition, secondPosition, duration=0.1):
    py.moveTo(firstPosition, duration=duration)
    py.mouseDown()
    py.moveTo(secondPosition, duration=duration)
    py.mouseUp()
    py.click(secondPosition)
