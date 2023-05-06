import os

from const import DIRECTORIES_TO_IGNORE, FILES_TO_IGNORE, SUMMARY_FILE_NAME

UNIT_INDENT = "  "
BULLET_POINT = "- "


def generate_summary(path: str, indent: str = "") -> None:
    # Avoid generating the root layer
    if (basename := os.path.basename(path)) != ".":
        with open(SUMMARY_FILE_NAME, "a") as file:
            file.write(f"{indent}{BULLET_POINT}{basename}\n")

    for sub_item in os.listdir(path):
        full_path = os.path.join(path, sub_item)
        if os.path.isdir(full_path) and (sub_item not in DIRECTORIES_TO_IGNORE):
            generate_summary(full_path, "" if path == "." else f"{indent}{UNIT_INDENT}")
        elif (
            os.path.isfile(full_path)
            and sub_item.endswith(".md")
            and (full_path not in FILES_TO_IGNORE)
        ):
            with open(SUMMARY_FILE_NAME, "a") as file:
                file.write(
                    f"{indent}{UNIT_INDENT}{BULLET_POINT}[{os.path.splitext(sub_item)[0]}](<./{full_path}>)\n"
                )


def main() -> None:
    with open(SUMMARY_FILE_NAME, "w") as file:
        file.write("# Summary\n\n")

    generate_summary(".")
    print(f"GitBook summary file ({SUMMARY_FILE_NAME}) generated.")


if __name__ == "__main__":
    main()
