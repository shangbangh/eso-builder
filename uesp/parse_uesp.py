# %%
from bs4 import BeautifulSoup
import json
import re

from utils import clean_text

# %%
html_files = [
    "arenaSets",
    "classSets",
    "craftableSets",
    "dungeonSets",
    "jewlrySets",
    "monsterSets",
    "overlandSets",
    "pvpSets",
    "trialSets",
    # "weaponSets", # TODO: weapon sets need to be handled separately
]
set_effects = {}
for html_name in html_files:
    print(f"parsing {html_name}")
    html = open(f"./uesp/{html_name}.html", "r")
    soup = BeautifulSoup(html.read())
    body = soup.find("tbody")
    rows = [tr for tr in body.find_all("tr")]
    sets = {}

    for row in rows:
        name = clean_text(row.find("th").getText().replace("\n", ""))
        effects_td = [td for td in row.find_all("td") if td.find_all("p")]
        if not effects_td:
            print(row)
        effects = clean_text(effects_td[0].find("p").getText())
        bonuses = {
            a: b
            for (a, b) in zip(
                re.findall(r"\d items", effects),
                [
                    clean_text(bonus)
                    for bonus in re.split(r"\d items:", effects)
                    if bonus != ""
                ],
            )
        }
        if name in set_effects:
            print(f"WARNING!!! duplicate set names: {name}")
        set_effects[name] = bonuses
        if html_name in ("arenaSets", "trialSets"):
            set_effects[f"Perfected {name}"] = bonuses

with open("./uesp/all_sets.json", "w+") as f:
    json.dump(set_effects, f)

# %%
