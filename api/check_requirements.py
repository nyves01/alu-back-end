#!/usr/bin/python3
"""Local validator for ALU API project requirements."""

import ast
import os
import subprocess
import sys


TARGET_FILES = [
    "0-gather_data_from_an_API.py",
    "1-export_to_CSV.py",
    "2-export_to_JSON.py",
    "3-dictionary_of_list_of_dictionaries.py"
]

EXPECTED_SHEBANG = "#!/usr/bin/python3"


def read_text(path):
    """Read text file as UTF-8."""
    with open(path, "r", encoding="utf-8") as file_obj:
        return file_obj.read()


def check_shebang(path, content):
    """Validate file shebang."""
    first_line = content.splitlines()[0] if content.splitlines() else ""
    return first_line == EXPECTED_SHEBANG


def check_trailing_newline(content):
    """Validate trailing newline."""
    return content.endswith("\n")


def check_module_docstring(path):
    """Validate module docstring presence."""
    tree = ast.parse(read_text(path))
    return ast.get_docstring(tree) is not None


def check_main_guard(content):
    """Validate __main__ guard."""
    return 'if __name__ == "__main__":' in content


def check_get_usage(content):
    """Validate dict get usage."""
    return ".get(" in content


def extract_top_import_block(content):
    """Extract top-level import lines in import section."""
    lines = content.splitlines()
    index = 0

    if index < len(lines) and lines[index].startswith("#!"):
        index += 1

    while index < len(lines) and not lines[index].strip():
        index += 1

    if index < len(lines) and (
        lines[index].startswith('"""') or lines[index].startswith("'''")
    ):
        quote = lines[index][:3]
        index += 1
        while index < len(lines):
            if lines[index].endswith(quote):
                index += 1
                break
            index += 1

    while index < len(lines) and not lines[index].strip():
        index += 1

    import_lines = []
    while index < len(lines):
        stripped = lines[index].strip()
        if not stripped:
            import_lines.append(lines[index])
            index += 1
            continue
        if stripped.startswith("import ") or stripped.startswith("from "):
            import_lines.append(stripped)
            index += 1
            continue
        break

    return [line for line in import_lines if line.strip()]


def check_import_order(content):
    """Validate alphabetical import order."""
    imports = extract_top_import_block(content)
    return imports == sorted(imports, key=lambda value: value.lower())


def get_git_mode(path):
    """Return git index mode for a file, or None if unavailable."""
    try:
        output = subprocess.check_output(
            ["git", "ls-files", "--stage", "--", path],
            stderr=subprocess.STDOUT
        ).decode("utf-8").strip()
    except Exception:
        return None

    if not output:
        return None
    return output.split()[0]


def check_executable(path):
    """Validate git executable bit (100755)."""
    mode = get_git_mode(path)
    return mode == "100755"


def print_result(file_name, label, passed):
    """Print a single check result."""
    mark = "OK" if passed else "FAIL"
    print("[{}] {} - {}".format(mark, file_name, label))


def validate_file(file_name):
    """Run all checks for one file."""
    results = []
    path = os.path.join(os.path.dirname(__file__), file_name)
    content = read_text(path)

    results.append(("shebang", check_shebang(path, content)))
    results.append(("trailing newline", check_trailing_newline(content)))
    results.append(("module docstring", check_module_docstring(path)))
    results.append(("__main__ guard", check_main_guard(content)))
    results.append(("dict get usage", check_get_usage(content)))
    results.append(("alphabetical imports", check_import_order(content)))
    results.append(("git executable mode", check_executable(path)))

    for label, passed in results:
        print_result(file_name, label, passed)

    return all(passed for _, passed in results)


def main():
    """Program entry point."""
    project_dir = os.path.dirname(__file__)
    readme_ok = os.path.isfile(os.path.join(project_dir, "README.md"))

    print_result("README.md", "exists", readme_ok)

    all_ok = readme_ok
    for file_name in TARGET_FILES:
        file_ok = validate_file(file_name)
        all_ok = all_ok and file_ok

    if all_ok:
        print("\nAll checks passed.")
        return 0

    print("\nOne or more checks failed.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
