import os
import re
from collections import OrderedDict

from const import DIRECTORIES_TO_IGNORE, FILES_TO_IGNORE

REGEX = r"!\[\[(.*)\]\]"
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

            breakpoints = sum(
                [[match.start(), match.end()] for match in re.finditer(REGEX, content)],
                [],
            )

            idx_substring_map = OrderedDict()
            for i, j in zip([0] + breakpoints, breakpoints + [len(content)]):
                idx_substring_map[(i, j)] = content[i:j]

            matches = [
                (match.start(), match.end()) for match in re.finditer(REGEX, content)
            ]
            for match in matches:
                if original_link := idx_substring_map.get(match):
                    idx_substring_map[match] = (
                        f"![](<{PRODUCTION_IMG_URL_PREFIX}{original_link[3:-2]}>)"
                    )

            content = "".join(idx_substring_map.values())

            with open(full_path, "w") as file:
                file.write(content)


if __name__ == "__main__":
    normalize_img_links(".")
    print("All image links normalized.")
