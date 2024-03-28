from database.item_db import ITEM_DB
from base_dumper import BlueArchiveDumper


class BlueArchiveItemDumper(BlueArchiveDumper):

    def file_name(self):
        return "items"

    def is_target_endpoint(self, url):
        return any(endpoint in url for endpoint in ["/api/item/list", "/api/gateway"])

    def is_target_protocol(self, protocol):
        return protocol == "Item_List"

    def transform(self, packet):
        return [
            {
                "id": item["UniqueId"],
                "name": ITEM_DB[item["UniqueId"]],
                "count": item["StackCount"],
            }
            for item in packet["ItemDBs"]
            if item["UniqueId"] in ITEM_DB
        ]
