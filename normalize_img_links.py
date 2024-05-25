import os
import re
from collections import OrderedDict

from const import DIRECTORIES_TO_IGNORE, FILES_TO_IGNORE

REGEX = r"!\[\[.*?\]\]"
PRODUCTION_IMG_URL_PREFIX = (
    "https://raw.githubusercontent.com/Jamison-Chen/KM-software/master/img/"
)


def normalize_img_links(path: str) -> None:
    for sub_item in os.listdir(path):
        full_path = os.path.join(path, sub_item)
        if os.path.isdir(full_path) and (sub_item not in DIRECTORIES_TO_IGNORE):
            normalize_img_links(full_path)
        elif (
            os.path.isfile(full_path)
            and (full_path not in FILES_TO_IGNORE)
            and sub_item.endswith(".md")
        ):
            with open(full_path, "r") as file:
                content = file.read()

            match_tuples = [(m.start(), m.end()) for m in re.finditer(REGEX, content)]
            breakpoints = [idx for t in match_tuples for idx in t]
            tuple_substring_map = OrderedDict()
            for i, j in zip([0] + breakpoints, breakpoints + [len(content)]):
                tuple_substring_map[(i, j)] = content[i:j]
            for match_tuple in match_tuples:
                original_link = tuple_substring_map[match_tuple][3:-2]
                tuple_substring_map[match_tuple] = (
                    f"![](<{PRODUCTION_IMG_URL_PREFIX}{original_link}>)"
                )

            with open(full_path, "w") as file:
                file.write("".join(tuple_substring_map.values()))


if __name__ == "__main__":
    normalize_img_links(".")
    print("All image links normalized.")
