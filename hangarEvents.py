import Scripts.Mouse.mouseEvents as ms
import python_imagesearch.imagesearch as sc
import Scripts.Images.Ship.Inventory.InventoryEvents as InventoryEvent

hangarPicture = 'Scripts/Images/Hangar/Hangar_UNDOCK.png'


def isFound(pos):
    if pos[0] == -1:

        return False
    else:

        return True


def findInAnAreaPos(img, confidence=0.8):
    return sc.imagesearch(img, precision=confidence)


def isFoundInAnArea(img, confidence=0.7):
    x = sc.imagesearch(img, precision=confidence)

    if x[0] == -1:
        del x
        return False
    else:
        del x
        return True


class Hangar:
    position = findInAnAreaPos(hangarPicture)

    def __init__(self):
        self.isInHangar = True
        self.positionUndock = 'position'
        self.inventory = InventoryEvent.Inventory()

    def isHangar(self):
        self.isInHangar = isFoundInAnArea('Hangar_UNDOCK.png')
        return self.isInHangar

    def setHangar(self):
        self.isInHangar = False

    def undock(self):
        ms.clickTo(self.positionUndock)
        self.setHangar()


def sellItems(self):
    if self.isHangar():
        print(self.positionUndock)



