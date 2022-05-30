import hangarEvents as he
import pyautogui as py

inventoryFull = 'Inv_Full.png'
inventoryPicture = 'Inventory.png'
Search = 'INV_Search.png'
DroneBay = 'Scripts/Screen/Images/Ship/Inventory/Inventory_DroneBay.png'
ItemHangar = 'Scripts/Screen/Images/Ship/Inventory/Inventory_ItemHangar.png'
MiningHold = 'Scripts/Screen/Images/Ship/Inventory/Inventory_MiningHold.png'
ShipHangar = 'Scripts/Screen/Images/Ship/Inventory/Inventory_ShipHangar.png'


class Inventory:
    isFull = True
    isOpen = False
    position = ''

    def __init__(self):
        self.isFull = True
        self.isOpen = True
        self.position = None

    def openInventory(self):
        if not self.isOpen:
            py.keyDown('alt')
            py.press('c')
            py.keyUp('alt')

    def isFulled(self):
        self.isFull = he.isFoundInAnArea(inventoryFull)

    def isOpened(self):
        self.isOpen = he.isFoundInAnArea(inventoryPicture)

    def positionOf(self):
        self.position = he.findInAnAreaPos(inventoryPicture)

    def checkInventory(self):
        self.positionOf()
        self.isFulled()
        self.positionOf()




