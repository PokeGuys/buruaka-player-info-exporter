from dumpers.characters import BlueArchiveCharacterDumper
from dumpers.equipments import BlueArchiveEquipmentDumper
from dumpers.items import BlueArchiveItemDumper


ADDONS = [
    BlueArchiveCharacterDumper(),
    BlueArchiveItemDumper(),
    BlueArchiveEquipmentDumper(),
]
