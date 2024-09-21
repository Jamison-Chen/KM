import os
import re
from collections import OrderedDict, deque
from pathlib import Path, PurePosixPath

from const import DIRECTORIES_TO_IGNORE, FILES_TO_IGNORE

LINK_REGEX = r"(?<!!)\[\[.*?\]\]"
SEPARATOR_REGEX = r"(?:\\\||\|)"


def normalize_internal_links(path: str) -> None:
    for sub_item in os.listdir(path):
        full_path = os.path.join(path, sub_item)
        if os.path.isdir(full_path) and (sub_item not in DIRECTORIES_TO_IGNORE):
            normalize_internal_links(full_path)
        elif (
            os.path.isfile(full_path)
            and (full_path not in FILES_TO_IGNORE)
            and sub_item.endswith(".md")
        ):
            with open(full_path, "r") as file:
                content = file.read()
            match_tuples = [
                (m.start(), m.end()) for m in re.finditer(LINK_REGEX, content)
            ]
            breakpoints = [idx for t in match_tuples for idx in t]
            tuple_substring_map: dict[tuple, str] = OrderedDict()
            for i, j in zip([0] + breakpoints, breakpoints + [len(content)]):
                tuple_substring_map[(i, j)] = content[i:j]
            for match_tuple in match_tuples:
                original_link = tuple_substring_map[match_tuple][2:-2].strip()
                match = re.search(SEPARATOR_REGEX, original_link)
                link_text = (
                    original_link[match.end() :] if match else original_link
                ).strip()
                linked_file = (
                    original_link[: match.start()] if match else original_link
                ).strip()
                hash = ""
                if "#" in linked_file:
                    idx = linked_file.find("#")
                    hash = linked_file[idx:]
                    linked_file = linked_file[:idx]
                if link_address := find_link_address(full_path, linked_file):
                    tuple_substring_map[match_tuple] = (
                        f"[{link_text}](</{link_address}{hash}>)"
                    )
            with open(full_path, "w") as file:
                file.write("".join(tuple_substring_map.values()))


def find_link_address(current_path_str: str, linked_file_name: str) -> str | None:
    if linked_file_name == "":
        return current_path_str
    current_path = Path(current_path_str)
    linked_file_name = (
        linked_file_name
        if (
            (suffix := PurePosixPath(linked_file_name).suffix)
            and " " not in suffix
            and suffix != ".draft"
        )
        else linked_file_name + ".md"
    )
    queue = deque([current_path])
    visited: set[Path] = set()
    root_path_strs = (".", "/")
    while queue:
        visiting_path = queue.popleft()
        if os.path.isfile(visiting_path) and visiting_path.match(linked_file_name):
            return visiting_path.as_posix()
        if (
            visiting_path.as_posix() not in root_path_strs
            and (parent_path := visiting_path.parent) not in visited
        ):
            queue.append(parent_path)
        if os.path.isdir(visiting_path):
            for child_path_str in os.listdir(visiting_path):
                if child_path_str not in (DIRECTORIES_TO_IGNORE | FILES_TO_IGNORE):
                    queue.append(visiting_path / child_path_str)
        visited.add(visiting_path)
    return None


if __name__ == "__main__":
    normalize_internal_links(".")
    print("All internal links normalized.")
