import json

GXP_LIST = ["Spring", "Hammer", "Barrel", "Needle"]
WEAPON_LIST = ["Hat","Gloves", "Shoes", "Bag", "Badge", "Hairpin", "Charm", "Watch", "Necklace"]
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
    for i in range(1, 5):
        item = item_dict.get(9+i, None)
        if item is not None:
            JUSTIN163_TEMPLATE["owned_materials"][f"XP_{i}"] = item["count"]
    for item in items:
        JUSTIN163_TEMPLATE["owned_materials"][item["id"]] = item["count"]

with open("../output/equipments.json", "r", encoding="utf-8") as f:
    equipments = json.load(f)
    equipment_dict = {equipment["id"]: equipment for equipment in equipments}
    for i in range(1, 5):
        equipment = equipment_dict.get(i, None)
        if equipment is not None:
            JUSTIN163_TEMPLATE["owned_materials"][f"GXP_{i}"] = equipment["count"]
        for m in GXP_LIST:
            material = equipment_dict.get(GXP_LIST.index(m) * 10 + 9 + i, None)
            if material is not None:
                JUSTIN163_TEMPLATE["owned_materials"][f"T{i}_{m}"] = material["count"]
    for w in WEAPON_LIST:
        t1 = equipment_dict.get((WEAPON_LIST.index(w) + 1) * 1000, None)
        if t1 is not None:
            JUSTIN163_TEMPLATE["owned_materials"][f"T1_{w}"] = t1["count"]
        for i in range(2, 10):
            weapon = equipment_dict.get(100000 + (WEAPON_LIST.index(w) + 1) * 1000 + i - 1, None)
            if weapon is not None:
                JUSTIN163_TEMPLATE["owned_materials"][f"T{i}_{w}"] = weapon["count"]

with open("justin163.json", "w") as f:
    json.dump(JUSTIN163_TEMPLATE, f)