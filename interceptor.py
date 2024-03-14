import json

from character_db import CHARACTER_DICT
from item_db import ITEM_DB


TARGET_ENDPOINTS = [
    # Global server
    "/api/account/loginsync",
    "/api/item/list",
    # Japan server
    "/api/gateway",
]

TARGET_PROTOCOLS = [
    "Account_LoginSync",
    "Item_List",
]


def is_target_endpoint(url):
    for endpoint in TARGET_ENDPOINTS:
        if endpoint in url:
            return True
    return False


def is_bluearchive_api(url):
    return is_global_server(url) or is_japan_server(url)


def is_japan_server(url):
    return "prod-game.bluearchiveyostar.com" in url


def is_global_server(url):
    return "bagl.nexon.com" in url


def is_target_protocol(protocol):
    for target_protocol in TARGET_PROTOCOLS:
        if protocol == target_protocol:
            return True
    return False


def transform_account_loginsync(packet):
    weapon_dict = dict(
        {
            db["BoundCharacterServerId"]: db
            for db in packet["CharacterListResponse"]["WeaponDBs"]
        }
    )
    gear_dict = dict(
        {
            db["BoundCharacterServerId"]: db
            for db in packet["CharacterGearListResponse"]["GearDBs"]
        }
    )
    equipment_dict = dict(
        {
            db["ServerId"]: db
            for db in packet["EquipmentItemListResponse"]["EquipmentDBs"]
        }
    )
    characters = []
    for db in packet["CharacterListResponse"]["CharacterDBs"]:
        weapon = weapon_dict.get(db["ServerId"])
        gear = gear_dict.get(db["ServerId"])
        equipments = [
            equipment_dict.get(serverId) for serverId in db["EquipmentServerIds"]
        ]
        characters.append(
            {
                "id": db["UniqueId"],
                "name": CHARACTER_DICT[db["UniqueId"]],
                "level": db["Level"],
                "starGrade": db["StarGrade"],
                "ueGrade": 0 if weapon is None else weapon.get("StarGrade", 1),
                "ueLevel": 0 if weapon is None else weapon.get("Level", 1),
                "exSkillLevel": "M" if db["ExSkillLevel"] == 5 else db["ExSkillLevel"],
                "nsSkillLevel": (
                    "M" if db["PublicSkillLevel"] == 10 else db["PublicSkillLevel"]
                ),
                "enhancedSkillLevel": (
                    "M" if db["PassiveSkillLevel"] == 10 else db["PassiveSkillLevel"]
                ),
                "subSkillLevel": (
                    "M"
                    if db["ExtraPassiveSkillLevel"] == 10
                    else db["ExtraPassiveSkillLevel"]
                ),
                "equipment_1": (
                    equipments[0].get("Tier", 1) if equipments[0] is not None else 0
                ),
                "equipment_2": (
                    equipments[1].get("Tier", 1) if equipments[1] is not None else 0
                ),
                "equipment_3": (
                    equipments[2].get("Tier", 1) if equipments[2] is not None else 0
                ),
                "uniqueItem": gear.get("Tier", "N/A") if gear is not None else "N/A",
                "favorRank": db["FavorRank"],
            }
        )

    return characters


def transform_item_list(packet):
    return [
        {
            "id": item["UniqueId"],
            "name": ITEM_DB[item["UniqueId"]],
            "count": item["StackCount"],
        }
        for item in packet["ItemDBs"]
    ]


def transform_response(protocol, packet):
    transformer_mapping = {
        "Account_LoginSync": transform_account_loginsync,
        "Item_List": transform_item_list,
    }
    if protocol in transformer_mapping:
        return transformer_mapping[protocol](packet)
    return None


class BlueArchiveDumper:

    def response(self, flow):
        if is_bluearchive_api(flow.request.pretty_url) and is_target_endpoint(
            flow.request.pretty_url
        ):
            payload = json.loads(flow.response.content)
            if not is_target_protocol(payload["protocol"]):
                return
            response = transform_response(
                payload["protocol"], json.loads(payload["packet"])
            )
            if response is None:
                print(
                    f'Warning: response is not transformed. Please implement the {payload["protocol"]} transformer.'
                )
                return
            with open(f"{payload['protocol']}.json", "w", encoding="utf-8") as f:
                json.dump(response, f, indent=4, ensure_ascii=False)


addons = [BlueArchiveDumper()]
