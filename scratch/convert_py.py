from pathlib import Path
import re
import sys

# Constants:
MOCK_PATH = Path(__file__).resolve().parents[1] / "src" / "mock_wx" / "wx"
PYI_PATH = Path(__file__).resolve().parents[1] / "test" / "test_cd" / "stubs" / "wx"
SEARCH_QUOTES = re.compile(r'^ *"""[^"]+"""\n', re.M)
SEARCH_INDENTED = re.compile(r"^ .*\n", re.M)
SEARCH_UNDERSCORE = re.compile(r"^_.*\n", re.M)
SEARCH_BLANK = re.compile(r"^\s*\n", re.M)
SEARCH_COMMENT = re.compile("#.*")
SEARCH_IMPORT = re.compile(r"^.*\bimport\b.*", re.M)
SEARCH_DEF = re.compile(r"^def (\w+).*", re.M)
SEARCH_BASE_CLASS = re.compile(r"^(class \w+):\s*$", re.M)
SEARCH_CLASS = re.compile(r"^(class .*)", re.M)
SEARCH_CONST = re.compile(r"^(\w+).*", re.M)


def main(parts) -> None:
    mock_path = MOCK_PATH
    pyi_path = PYI_PATH
    for part in parts[:-1]:
        mock_path = mock_path / part
        pyi_path = pyi_path / part
    mock_path = mock_path / f"{parts[-1]}.py"
    pyi_path = pyi_path / f"{parts[-1]}.pyi"
    with pyi_path.open("rt", encoding="utf-8") as file_obj:
        text = file_obj.read()
    text = SEARCH_QUOTES.sub("", text)
    text = SEARCH_INDENTED.sub("", text)
    text = SEARCH_UNDERSCORE.sub("", text)
    text = SEARCH_COMMENT.sub("", text)
    text = SEARCH_IMPORT.sub("", text)
    text = SEARCH_BLANK.sub("", text)
    for match in SEARCH_CONST.finditer(text):
        if match.group(1) not in ["def", "class"]:
            text = re.sub(f"^{match.group(1)}\\W.*", f'{match.group(1)} = {{"{match.group(1)}"}}', text, flags=re.M)
    text = SEARCH_DEF.sub(r"\1 = MOCK.\1", text)
    text = SEARCH_BASE_CLASS.sub(r"\1 ...", text)
    text = SEARCH_CLASS.sub(r"\1(BaseClass):", text)
    print(text)
    with mock_path.open("wt", encoding="utf-8") as file_obj:
        file_obj.write(text)


if __name__ == "__main__":
    main(sys.argv[1:])
