from base_dumper import BlueArchiveDumper


class BlueArchiveCharacterDumper(BlueArchiveDumper):

    def file_name(self):
        return "characters"

    def is_target_endpoint(self, url):
        return any(
            endpoint in url for endpoint in ["/api/account/loginsync", "/api/gateway"]
        )

    def is_target_protocol(self, protocol):
        return protocol == "Account_LoginSync"

    def transform(self, packet):
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
                    "level": db["Level"],
                    "starGrade": db["StarGrade"],
                    "ueGrade": 0 if weapon is None else weapon.get("StarGrade", 1),
                    "ueLevel": 0 if weapon is None else weapon.get("Level", 1),
                    "exSkillLevel": (
                        "M" if db["ExSkillLevel"] == 5 else db["ExSkillLevel"]
                    ),
                    "nsSkillLevel": (
                        "M" if db["PublicSkillLevel"] == 10 else db["PublicSkillLevel"]
                    ),
                    "enhancedSkillLevel": (
                        "M"
                        if db["PassiveSkillLevel"] == 10
                        else db["PassiveSkillLevel"]
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
                    "uniqueItem": (
                        gear.get("Tier", "N/A") if gear is not None else "N/A"
                    ),
                    "favorRank": db["FavorRank"],
                }
            )
        return characters
