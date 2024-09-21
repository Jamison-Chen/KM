import os

from const import DIRECTORIES_TO_IGNORE, FILES_TO_IGNORE, SUMMARY_FILE_NAME

UNIT_INDENT = "  "
BULLET_POINT = "- "


def generate_summary(path: str, indent: str = "") -> int:
    basename = os.path.basename(path) if os.path.basename(path) != "." else "Software"
    with open(SUMMARY_FILE_NAME, "a") as file:
        file.write(f"{indent}{BULLET_POINT}{basename}\n")
    children_count = 0
    for sub_item in os.listdir(path):
        full_path = os.path.join(path, sub_item)
        if os.path.isdir(full_path) and (sub_item not in DIRECTORIES_TO_IGNORE):
            children_count += generate_summary(full_path, f"{indent}{UNIT_INDENT}")
        elif (
            os.path.isfile(full_path)
            and sub_item.endswith(".md")
            and not sub_item.endswith(".draft.md")
            and full_path not in FILES_TO_IGNORE
        ):
            with open(SUMMARY_FILE_NAME, "a") as file:
                file.write(
                    f"{indent}{UNIT_INDENT}{BULLET_POINT}[{os.path.splitext(sub_item)[0]}](<./{full_path}>)\n"
                )
            children_count += 1
    if not children_count:
        _delete_last_line()
        return 0
    return 1


def _delete_last_line():
    with open(SUMMARY_FILE_NAME, "r") as file:
        lines = file.readlines()
    with open(SUMMARY_FILE_NAME, "w") as file:
        file.writelines(lines[:-1])


def main() -> None:
    with open(SUMMARY_FILE_NAME, "w") as file:
        file.write("# Summary\n\n")
    generate_summary(".")
    print(f"GitBook summary file ({SUMMARY_FILE_NAME}) generated.")


if __name__ == "__main__":
    main()
