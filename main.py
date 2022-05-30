import keyboard
import python_imagesearch.imagesearch as sc
import pyautogui as py
import Scripts.Mouse.mouseEvents as ms

inventoryFull = 'Scripts/Images/Ship/Inventory/Inv_Full.png'
inventoryPicture = 'Scripts/Images/Ship/Inventory/Inventory.png'
Search = 'Scripts/Images/Ship/Inventory/INV_Search.png'
DroneBay = 'Scripts/Images/Ship/Inventory/Inventory_DroneBay.png'
ItemHangar = 'Scripts/Images/Ship/Inventory/Inventory_ItemHangar.png'
MiningHold = 'Scripts/Images/Ship/Inventory/Inventory_MiningHold.png'
ShipHangar = 'Scripts/Images/Ship/Inventory/Inventory_ShipHangar.png'
hangarPicture = 'Hangar_UNDOCK.png'


def isFound(pos):
    if pos[0] == -1:

        return False
    else:

        return True


def findInAnAreaPos(img, confidence=0.8):
    return sc.imagesearch(img, precision=confidence)


def isFoundInAnArea(img, confidence=0.9):
    x = sc.imagesearch(img, precision=confidence)

    if x[0] == -1:
        del x
        return False
    else:
        del x
        return True


class Inventory:
    isFull = False
    isOpen = False
    position = ''

    def __init__(self):
        self.isFull = False
        self.isOpen = False
        self.position = None

    def openInventory(self):
        if not self.isOpen:
            py.keyDown('alt')
            py.press('c')
            py.keyUp('alt')
            self.isOpen = True

    def isFulled(self):
        self.isFull = isFoundInAnArea(inventoryFull)
        return self.isFull

    def positionOf(self):
        self.position = findInAnAreaPos(inventoryPicture)
        if self.position[0] != -1:
            self.isOpen = True
        else:
            self.isOpen = False
            self.openInventory()

    def checkInventory(self):
        py.moveTo(findInAnAreaPos('Scripts/Images/Ship/Inventory/InventoryBar.png'))
        self.positionOf()
        self.isFulled()


class Ship:

    def __init__(self):
        self.isInHangar = False
        self.positionUndock = 'position'
        self.inventory = Inventory()
        self.inField = False
        self.inSpace = False
        self.TargetOn = False
        self.Target = {'Mine': 'Scripts/Images/Overview/Mine/Small/S_Mine.png', }
        self.SelectedTarget = {'Mine': 'Scripts/Images/Overview/Mine/Small/TARGET_S_Mine.png'}
        self.TargetedTarget = ''
        self.Overview = {'General': 'Scripts/Images/Overview/Tag/Overview_General.png',
                         'Mining': 'Scripts/Images/Overview/Tag/Overview_Mining.png',
                         'AstroidBelt': 'Scripts/Images/Overview/Field/Overview_AstroidBelt.png',
                         'Station': 'Scripts/Images/Overview/StationOrGate/Overview_Station.png'}
        self.Mouse = {'Dock': 'Scripts/Images/Mouse/Right/Target/Mouse_Right_Dock_png.png',
                      'Warp': 'Scripts/Images/Mouse/Right/Target/Mouse_Right_Warp0.png',
                      'SelectAll': 'Scripts/Images/Mouse/Inventory/Mouse_Inventory_SelectAll.png',
                      'Sell': 'Scripts/Images/Mouse/Inventory/Mouse_Inventory_Sell.png',
                      'SellItem': 'Scripts/Images/Mouse/Inventory/SellItem.png'}

    def checkPosition(self):
        print('Sleeping 10 second')
        py.sleep(10)
        print('Checking Position')
        self.inventory.checkInventory()
        print('Inventory Checked: Inventory open is {0} and Inventory'
              ' Full is {1}'.format(self.inventory.isOpen, self.inventory.isFull))
        self.isHangar()
        print('Ship in Hangar {0}, in Space {1}, in Field {2}'.format(self.isInHangar, self.inSpace, self.inField))
        print('*************************')
        if self.isInHangar:
            print('Started Hangar Process')
            self.sellItems()
            print('Hangar Process Done')
        else:
            print('Starting Space Synchronization')
            self.isInField()
            print('is in Field {0}, is in Space {1}'.format(self.inField, self.inSpace))
            print('*************************')
            if self.inSpace:
                print('in Space formation started warping to...{0} '.format(self.Overview['AstroidBelt']))
                warpToField(img=self.Overview['AstroidBelt'], choose=self.Mouse['Warp'])
                self.checkPosition()
            elif self.inField:
                if self.inventory.isFull:
                    warpToStation(img=self.Overview['Station'], choose=self.Mouse['Dock'])
                else:
                    self.checkTarget()
            else:
                print('No Space,No Field returning Station')
                warpToStation(img=self.Overview['Station'], choose=self.Mouse['Dock'])

    def isInField(self):  # Not in Hangar 2
        print('Checking if ship in Field')
        if not self.isInHangar and not self.TargetOn:
            ms.clickTo(findInAnAreaPos(self.Overview['Mining']))
        if isFoundInAnArea(self.Target['Mine']):
            print('Marketable objects are found')
            self.inField = True
            self.inSpace = False

        elif isFoundInAnArea(self.SelectedTarget['Mine']):
            print('Selected target is found ')
            self.inField = True
            self.inSpace = False

        else:
            print('There is no markable object')
            self.inField = False
            self.inSpace = True
            self.isInHangar = False

    def isHangar(self):  # Find if in Hangar    1
        x = findInAnAreaPos('Scripts/Images/Hangar/Hangar_UNDOCK.png')
        self.positionUndock = x

        if x[0] != -1:
            self.isInHangar = True
            self.inField = False
            self.inSpace = False
            del x
            return self.isInHangar
        else:
            self.isInHangar = False
        del x
        return self.isInHangar

    def setHangar(self):
        self.isInHangar = False

    def undock(self):

        ms.clickTo(self.positionUndock)

        self.setHangar()

    def sellItems(self):

        if self.isInHangar:
            self.inventory.checkInventory()
            sellItem(self)

    def checkTurrets(self):  # Not in Hangar Not in Space (in Field)
        x = sc.imagesearch('Scripts/Images/Ship/UI/Targeted/weaponOn.png',precision=0.7)

        if x[0] != -1:
            self.TargetOn = True

            x = sc.imagesearch_count('Scripts/Images/Ship/UI/Targeted/weaponOn.png')
            print('There are {0} Target'.format(x))
            del x
            print('sleeping 60 second')
            py.sleep(60)
        else:
            del x
            self.TargetOn = False

    def checkTarget(self):  # Not in Space not in Hangar (in Field) 1

        if self.inField:
            if not self.TargetOn:
                ms.clickTo(findInAnAreaPos(self.Overview['Mining']))

            x = findInAnAreaPos(self.Target['Mine'])
            y = findInAnAreaPos(self.SelectedTarget['Mine'])
            if y[0] != -1:
                self.checkTurrets()
                if not self.TargetOn:
                    py.keyDown('q')
                    ms.clickTo(y)
                    py.keyUp('q')

                if not self.TargetOn:
                    py.sleep(.3)
                    py.press(['f1', 'f2'])
                del x
            else:
                py.keyDown('ctrl')
                py.sleep(.01)
                ms.clickTo(x,duration=0.02)
                py.keyUp('ctrl')
                py.press('q')
                ms.clickTo(x,duration=0.01)
                del x
                py.sleep(20)

        del y


def sellItem(hangar):  # not in field not in space (in Hangar)
    x = findInAnAreaPos(MiningHold)
    ms.clickTo(x)
    ms.rightClickTo((x[0] + 175, x[1] + 100))
    ms.clickTo(findInAnAreaPos(hangar.Mouse['SelectAll']))
    ms.holdAndGrapTarget(firstPosition=(x[0] + 175, x[1]), secondPosition=findInAnAreaPos(ItemHangar), duration=0.2)
    ms.rightClickTo(pos=(x[0] + 175, x[1]))
    ms.clickTo(findInAnAreaPos(hangar.Mouse['SelectAll']))
    ms.rightClickTo(pos=(x[0] + 175, x[1]))
    py.sleep(.4)
    del x
    x = findInAnAreaPos(hangar.Mouse['Sell'])
    ms.clickTo(x)
    py.sleep(1.2)
    if x[0] != -1:

        x = findInAnAreaPos(hangar.Mouse['SellItem'])
        ms.clickTo(x)
        py.sleep(0.6)
        ms.clickTo(x)
        del x
        hangar.undock()

    else:
        hangar.undock()


def warpToField(img, choose):  # not in field not in hangar(in Space)
    ms.clickTo(findInAnAreaPos('Scripts/Images/Overview/Tag/Overview_Mining.png'))
    y = findInAnAreaPos(img, confidence=0.9)

    if y[0] != -1:
        ms.clickTo(y)
        ms.rightClickTo(y)
        x = findInAnAreaPos(choose, confidence=0.9)
        if x[0] != -1:
            ms.clickTo(x)
            py.sleep(12)
        del x
    del y


def warpToStation(img, choose):  # not in space not in hangar(in field)
    ms.clickTo(findInAnAreaPos('Scripts/Images/Overview/Tag/Overview_General.png'))
    y = findInAnAreaPos(img, confidence=0.9)

    if y[0] != -1:
        ms.clickTo(y)
        ms.rightClickTo(y)
        x = findInAnAreaPos(choose, confidence=0.9)
        if x[0] != -1:
            ms.clickTo(x)
            py.sleep(12)
        del x
        ms.clickTo((y[0] - 100, y[1]))
    del y


while not keyboard.is_pressed('q'):
    py.sleep(2)
    a = Ship()
    a.checkPosition()
