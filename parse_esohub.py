# %%
from bs4 import BeautifulSoup
import json
import re
import os

from utils import clean_text

# %% parse sets
directory = "./data_source/gear_sets"
pages = [d for d in os.listdir(directory) if d.endswith(".json")]
all_sets = {}
all_sets_raw = {}
for page in pages:
    with open(f"{directory}/{page}", "r") as f:
        sets_dict = json.load(f)
        data = sets_dict["data"]
        for set_ in data:
            name = set_["name"]
            soup = BeautifulSoup(set_["html"])
            item_regex = r"\(\d item.?\)"
            bonus_keys = re.findall(item_regex, soup.text)
            assert len(bonus_keys), f"item description not found:\n {soup.text}\n\n[end]"
            bonuses = re.split(item_regex, soup.text)
            set_bonuses = {k[1:-1]:clean_text(v) for k, v in zip(bonus_keys, bonuses[1:])}
            all_sets[name] = set_bonuses
            all_sets[name].update({
                "name": name,
                "category": set_["category"],
                "class": set_["class"] if set_["class"] else ""
            })
            all_sets_raw[name] = soup.text

with open("./all_sets.json", "w+") as f:
    json.dump(all_sets, f)

with open("./all_sets_raw.json", "w+") as f:
    json.dump(all_sets_raw, f)

# %% parse skills
all_skills = {}
all_skills_raw = {}
with open("./data_source/skills.html", "r") as f:
    html_str = f.read()
    skills_soup = BeautifulSoup(html_str)
    for skill in skills_soup.find_all("div", {"class": "p-4"}, recursive=False):
        name = skill.find("a", {"class": "mt-2"}).text
        categories = [element.text for element in skill.find_all("a", {"class": "text-superior-500"})]
        skill_type = skill.find("div", {"class": "justify-between"}).find("strong").text
        description = "\n".join([element.text for element in skill.find_all("div", {"class": "text-center"})])
        all_skills[name] = {
            "name": name,
            "type": skill_type,
            "category": categories[0],
            "subcategory": categories[1],
            "description": clean_text(description)
        }
        all_skills_raw[name] = f"{skill_type}, {categories[0]}, {categories[1]}. \n{clean_text(description)}"

with open("./all_skills.json", "w+") as f:
    json.dump(all_skills, f)
with open("./all_skills_raw.json", "w+") as f:
    json.dump(all_skills_raw, f)
# %% parse cp
all_cp = {}
all_cp_raw = {}
with open("./data_source/cp.json", "r") as f:
    cp_dict = json.load(f)
