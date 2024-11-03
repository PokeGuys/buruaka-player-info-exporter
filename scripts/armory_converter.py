import json
from lzstring import LZString


with open("./armory_code.txt", "r", encoding="utf-8") as f:
    code = f.read()
    print(LZString.decompressFromBase64(code))
    ARMORY_TEMPLATE = json.loads(LZString.decompressFromBase64(code))


def restore_skill(level, type="O"):
    max_level = 5 if type == "EX" else 10
    return max_level if level == "M" else level


with open("./output/characters.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    db_dict = {db["id"]: db for db in data}
    for idx, s in enumerate(ARMORY_TEMPLATE["students"]):
        if s["id"] not in db_dict:
            continue
        target = db_dict[s["id"]]
        skills = [
            restore_skill(target["exSkillLevel"], "EX"),
            restore_skill(target["nsSkillLevel"]),
            restore_skill(target["enhancedSkillLevel"]),
            restore_skill(target["subSkillLevel"]),
        ]
        ARMORY_TEMPLATE["students"][idx]["skills"] = [
            {
                "studentId": s["id"],
                "index": skill_idx,
                "level": skill,
                "levelTarget": skill,
            }
            for skill_idx, skill in enumerate(skills)
        ]
        ARMORY_TEMPLATE["students"][idx]["level"] = target["level"]
        ARMORY_TEMPLATE["students"][idx]["levelTarget"] = max(
            ARMORY_TEMPLATE["students"][idx]["levelTarget"], target["level"]
        )
        ARMORY_TEMPLATE["students"][idx]["star"] = target["starGrade"]
        ARMORY_TEMPLATE["students"][idx]["starTarget"] = max(
            ARMORY_TEMPLATE["students"][idx]["starTarget"], target["starGrade"]
        )
        ARMORY_TEMPLATE["students"][idx]["weapon"] = target["ueGrade"]
        ARMORY_TEMPLATE["students"][idx]["weaponTarget"] = max(
            target["ueGrade"], ARMORY_TEMPLATE["students"][idx]["weaponTarget"]
        )
        ARMORY_TEMPLATE["students"][idx]["gear"] = (
            0 if target["uniqueItem"] == "N/A" else target["uniqueItem"]
        )
        ARMORY_TEMPLATE["students"][idx]["gearTarget"] = max(
            ARMORY_TEMPLATE["students"][idx]["gearTarget"],
            0 if target["uniqueItem"] == "N/A" else target["uniqueItem"],
        )
        ARMORY_TEMPLATE["students"][idx]["equipments"] = [
            {
                "studentId": s["id"],
                "index": eq_idx,
                "tier": target[f"equipment_{eq_idx + 1}"],
                "tierTarget": max(target[f"equipment_{eq_idx + 1}"], eq["tierTarget"]),
            }
            for eq_idx, eq in enumerate(ARMORY_TEMPLATE["students"][idx]["equipments"])
        ]
with open("./output/items.json", "r", encoding="utf-8") as f:
    items = json.load(f)
    ARMORY_TEMPLATE["stocks"] = dict({x["id"]: x["count"] for x in items})
with open("./output/equipments.json", "r", encoding="utf-8") as f:
    equipments = json.load(f)
    for eq in equipments:
        ARMORY_TEMPLATE["stocks"][2000000 + eq["id"]] = eq["count"]
with open("./armory_code.txt", "w", encoding="utf-8") as f:
    f.write(
        LZString.compressToBase64(
            json.dumps(ARMORY_TEMPLATE, indent=4, ensure_ascii=False)
        )
    )
    print("Done")
