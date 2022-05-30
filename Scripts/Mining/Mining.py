from Scripts.Images.Ship.Inventory import InventoryEvents as inv
import hangarEvents as Hangar


class Ship:
    hangar = Hangar.Hangar()
    inventory = inv.Inventory()
    turrets = False

    def __init(self, inventory, hangar, turrets):
        self.inventory = inventory
        self.hangar = hangar
        self.turrets = turrets

