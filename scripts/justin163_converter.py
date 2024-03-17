import json

JUSTIN163_TEMPLATE = {
    "exportVersion": 2,
    "characters": [],
    "disabled_characters": [],
    "owned_materials": {},
    "groups": {
        "Binah": [],
        "Chesed": [],
        "Hod": [],
        "ShiroKuro": [],
        "Perorodzilla": [],
        "Goz": [],
        "Hieronymous": [],
        "Kaiten": []
    },
    "language": "Tw",
    "level_cap": 87,
    "server": "Global",
    "site_version": "1.4.5",
    "character_order": []
}

def restore_skill(level, type="O"):
    max_level = 5 if type == "EX" else 10
    return max_level if level == "M" else level

def create_student(student):
    return {
        "id": student["id"],
        "name": student["name"],
        "current": {
            "level": student["level"],
            "bond": student["favorRank"],
            "star": student["starGrade"],
            "ue": student["ueGrade"],
            "ue_level": student["ueLevel"],
            "ex": restore_skill(student["exSkillLevel"], "EX"),
            "basic": restore_skill(student["nsSkillLevel"]),
            "passive": restore_skill(student["enhancedSkillLevel"]),
            "sub": restore_skill(student["subSkillLevel"]),
            "gear1": student["equipment_1"],
            "gear2": student["equipment_2"],
            "gear3": student["equipment_3"]
        },
        "target": {
            "level": student["level"],
            "bond": student["favorRank"],
            "star": student["starGrade"],
            "ue": student["ueGrade"],
            "ue_level": student["ueLevel"],
            "ex": restore_skill(student["exSkillLevel"], "EX"),
            "basic": restore_skill(student["nsSkillLevel"]),
            "passive": restore_skill(student["enhancedSkillLevel"]),
            "sub": restore_skill(student["subSkillLevel"]),
            "gear1": student["equipment_1"],
            "gear2": student["equipment_2"],
            "gear3": student["equipment_3"]
        },
        "eleph": {
            "owned": 0,
            "unlocked": True,
            "cost": 1,
            "purchasable": 20,
            "farm_nodes": 0,
            "node_refresh": False,
            "use_eligma": False,
            "use_shop": False
        },
        "enabled": True
    }

with open("../output/characters.json", "r", encoding="utf-8") as f:
    students = json.load(f)
    JUSTIN163_TEMPLATE["characters"] = [create_student(student) for student in students]

with open("../output/items.json", "r", encoding="utf-8") as f:
    items = json.load(f)
    item_dict = {item["id"]: item for item in items}
    JUSTIN163_TEMPLATE["owned_materials"]["XP_1"] = item_dict[10]["count"]
    JUSTIN163_TEMPLATE["owned_materials"]["XP_2"] = item_dict[11]["count"]
    JUSTIN163_TEMPLATE["owned_materials"]["XP_3"] = item_dict[12]["count"]
    JUSTIN163_TEMPLATE["owned_materials"]["XP_4"] = item_dict[13]["count"]
    for item in items:
        JUSTIN163_TEMPLATE["owned_materials"][item["id"]] = item["count"]

with open("justin163.json", "w") as f:
    json.dump(JUSTIN163_TEMPLATE, f)