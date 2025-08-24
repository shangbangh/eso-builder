def clean_text(text: str) -> str:
    return " ".join(text.strip().split())


def shred_dict_to_cp(cp):
    if type(cp) == list:
        l = []
        for item in cp:
            l.extend(shred_dict_to_cp(item))
        return l
    elif type(cp) != dict:
        raise Exception(f"unexpected type {type(cp)}: {cp}")
    if "max_points" in cp:
        return [cp]
    cp_stars = []
    for v in cp.values():
        if type(v) in (list, dict):
            cp_stars.extend(shred_dict_to_cp(v))
    return cp_stars