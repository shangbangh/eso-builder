# %%
from bs4 import BeautifulSoup
import json
import re
import os

from utils import clean_text, shred_dict_to_cp

# %% parse sets
all_sets = {}
all_sets_raw = {}
with open(f"./data_source/gear_set.html", "r") as f:
    html_str = f.read()
    sets_soup = BeautifulSoup(html_str)
    for gear_set in sets_soup.find_all("div", {"class": "p-4"}, recursive=False):
        name = gear_set.find("a", {"class": "mt-2"}).text
        class_set = gear_set.find("a", {"class": "text-superior-500"}).text if gear_set.find("a", {"class": "text-superior-500"}) else ""
        gear_type = gear_set.find("div", {"class": "justify-between"}).find("strong").text

        description = gear_set.find("div", {"class": "text-xs/5"}).text
        item_regex = r"\(\d item.?\)"
        bonus_keys = re.findall(item_regex, description)
        assert len(bonus_keys), f"item description not found:\n {description}\n\n[end]"
        bonuses = re.split(item_regex, description)
        set_bonuses = {k[1:-1]:clean_text(v) for k, v in zip(bonus_keys, bonuses[1:])}
        all_sets[name] = {
            "name": name,
            "type": gear_type,
            "class_set": class_set,
            "description": clean_text(description),
            **set_bonuses
        }
        all_sets_raw[name] = f"{gear_type}, {class_set}. \n{clean_text(description)}"

with open("./all_sets.json", "w+") as f:
    json.dump(all_sets, f)

with open("./all_sets_raw.json", "w+") as f:
    json.dump(all_sets_raw, f)

# %% parse skills
all_skills = {}
all_skills_raw = {}
with open("./data_source/skills.html", "r") as f:
    html_str = f.read()
    sets_soup = BeautifulSoup(html_str)
    for gear_set in sets_soup.find_all("div", {"class": "p-4"}, recursive=False):
        name = gear_set.find("a", {"class": "mt-2"}).text
        categories = [element.text for element in gear_set.find_all("a", {"class": "text-superior-500"})]
        gear_type = gear_set.find("div", {"class": "justify-between"}).find("strong").text
        description = "\n".join([element.text for element in gear_set.find_all("div", {"class": "text-center"})])
        all_skills[name] = {
            "name": name,
            "type": gear_type,
            "category": categories[0],
            "subcategory": categories[1],
            "description": clean_text(description)
        }
        all_skills_raw[name] = f"{gear_type}, {categories[0]}, {categories[1]}. \n{clean_text(description)}"

with open("./all_skills.json", "w+") as f:
    json.dump(all_skills, f)
with open("./all_skills_raw.json", "w+") as f:
    json.dump(all_skills_raw, f)
# %% parse cp
all_cp_flat = {}
all_cp = {}
all_cp_raw = {}
with open("./data_source/cp.json", "r") as f:
    cp_dict = json.load(f)
    all_cp_flat = shred_dict_to_cp(cp_dict)
    for cp in all_cp_flat:
        all_cp[cp["name"]] = {
            "name": cp["name"],
            "type": "passive" if cp["is_passive"] else "slotable",
            "max_points": cp["max_points"]
        }
        all_cp_raw[cp["name"]] = f"{cp['name']}: {cp['description']}"

with open("./all_cp_flat.json", "w+") as f:
    json.dump(all_cp_flat, f)

with open("./all_cp.json", "w+") as f:
    json.dump(all_cp, f)

with open("./all_cp_raw.json", "w+") as f:
    json.dump(all_cp_raw, f)

# %%
