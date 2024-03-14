from database.equipment_db import EQUIPMENT_DB
from base_dumper import BlueArchiveDumper


class BlueArchiveEquipmentDumper(BlueArchiveDumper):

    def __init__(self):
        super().__init__("equipments")

    def is_target_endpoint(self, url):
        return any(
            endpoint in url for endpoint in ["/api/account/loginsync", "/api/gateway"]
        )

    def is_target_protocol(self, protocol):
        return protocol == "Account_LoginSync"

    def transform(self, packet):
        return [
            dict(
                {
                    "id": eq["UniqueId"],
                    "name": EQUIPMENT_DB[eq["UniqueId"]],
                    "count": eq["StackCount"],
                }
            )
            for eq in packet["EquipmentItemListResponse"]["EquipmentDBs"]
            if "BoundCharacterServerId" not in eq
        ]
