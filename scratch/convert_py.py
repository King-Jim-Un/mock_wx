from dataclasses import dataclass, field
import logging
from pathlib import Path
import re
from typing import List, Set, Dict

# Constants:
LOG = logging.getLogger(__name__)
MOCK_PATH = Path(__file__).resolve().parents[1] / "src" / "mock_wx" / "wx"
PYI_PATH = Path(__file__).resolve().parents[1] / "test" / "test_cd" / "stubs" / "wx"
SEARCH_QUOTES = re.compile(r'^ *"""[^"]+"""\n', re.M)
SEARCH_DEF = re.compile(r"^def (\w+)")
SEARCH_BASE_CLASS = re.compile(r"^class\s+(\w+)\s*:")
SEARCH_CLASS = re.compile(r"^class\s+(\w+)\s*\((.*)\)\s*:")
SEARCH_CONST = re.compile(r"^\s*(\w+)")


@dataclass
class Class:
    name: str
    parents: List[str] = field(default_factory=list)
    consts: List[str] = field(default_factory=list)


@dataclass
class Converter:
    class_map: Dict[str, str] = field(init=False)

    def __post_init__(self):
        self.class_map = {
            "ExpandoTextCtrl": "wx.lib.expando",
            "GenStaticText": "wx.lib.stattext",
            "GenButton": "wx.lib.buttons",
            "MaskedEditMixin": "wx.lib.masked.maskededit",
            "MaskedEditAccessorsMixin": "wx.lib.masked.maskededit",
            "BaseMaskedTextCtrl": "wx.lib.masked.textctrl",
            "BaseClass": "wx.base_class",
        }

    def convert_file(self, dir_path, pyi_path, mock_path) -> None:
        consts: List[str] = []
        funcs: List[str] = []
        classes: Dict[str, Class] = {}
        imports: Dict[str, Set[str]] = {}

        if dir_path == "wx.propgrid":
            classes["PropertyGridIteratorBase"] = Class("PropertyGridIteratorBase")

        # Open source
        with pyi_path.open("rt", encoding="utf-8") as file_obj:
            text = file_obj.read()

        # Remove most docstrings
        text = SEARCH_QUOTES.sub("", text)

        # Loop through lines
        last_class = None
        for line in text.splitlines():
            # Types
            if line.startswith("_"):
                continue

            # Functions
            match = SEARCH_DEF.search(line)
            if match:
                name = match.group(1)
                funcs.append(name)
                if name not in self.class_map:
                    self.class_map[name] = dir_path
                if "base_class" not in imports:
                    imports["wx.base_class"] = set()
                imports["wx.base_class"].add("G_MOCK")
                last_class = None
                continue

            # Classes
            match = SEARCH_BASE_CLASS.search(line)
            if match:
                last_class = Class(match.group(1), ["BaseClass"])
                classes[last_class.name] = last_class
                if last_class.name not in self.class_map:
                    self.class_map[last_class.name] = dir_path
                continue
            match = SEARCH_CLASS.search(line)
            if match:
                last_class = Class(match.group(1), [parent.strip() for parent in match.group(2).split(",")])
                if last_class.name == "DragImage":
                    last_class.parents = ["Object"]
                elif last_class.name == "ComboBox":
                    last_class.parents = ["Control", "ItemContainer", "TextEntry"]
                elif last_class.name == "TextCtrl":
                    last_class.parents = ["Control", "TextEntry"]
                elif last_class.name == "Scrolled":
                    last_class.parents = []
                classes[last_class.name] = last_class
                if last_class.name not in self.class_map:
                    self.class_map[last_class.name] = dir_path
                continue

            # Constants
            match = SEARCH_CONST.search(line)
            if match:
                if match.group(1) in ["type", "def", "from", "import", "tuple"]:
                    continue
                if line.startswith(" "):
                    if last_class:
                        last_class.consts.append(match.group(1))
                else:
                    name = match.group(1)
                    consts.append(name)
                    if name not in self.class_map:
                        self.class_map[name] = dir_path

        # Do we need any imports?
        names: Set[str] = set()
        parents: Set[str] = set()
        for name, item in classes.items():
            names.add(name)
            for parent in item.parents:
                parents.add(parent)
        unknown_classes = parents - names
        for missing_class in unknown_classes:
            if missing_class in ["Enum", "Flag"]:
                path = "enum"
            elif missing_class == "ContextManager":
                path = "typing"
            else:
                path = self.class_map[missing_class]
            if path not in imports:
                imports[path] = set()
            imports[path].add(missing_class)

        # Write destination
        with mock_path.open("wt", encoding="utf-8") as file_obj:
            # Imports
            for path, class_names in imports.items():
                file_obj.write("from %s import %s\n" % (path, ", ".join(class_names)))

            # Constants
            for const in sorted(consts):
                file_obj.write('%s = {"%s"}\n' % (const, const))

            # Functions
            for func in sorted(funcs):
                file_obj.write(f"{func} = G_MOCK.{func}\n")

            # Classes
            included: Set[str] = unknown_classes
            sorted_classes = list(classes.values())
            sorted_classes.sort(key=lambda cls: cls.name)
            while sorted_classes:
                for index, item in enumerate(sorted_classes):
                    if all(parent in included for parent in item.parents):
                        included.add(item.name)
                        if item.parents:
                            file_obj.write(
                                "class %s(%s):%s\n"
                                % (item.name, ", ".join(item.parents), "" if item.consts else " ...")
                            )
                        else:
                            file_obj.write("class %s:%s\n" % (item.name, "" if item.consts else " ..."))
                        for const in item.consts:
                            file_obj.write('    %s = {"%s"}\n' % (const, const))
                        del sorted_classes[index]
                        break
                else:
                    print(sorted_classes)
                    print(unknown_classes)
                    1 / 0

    def convert_dir(self, parts) -> None:
        # Create paths
        pyi_dir = PYI_PATH
        mock_dir = MOCK_PATH
        for part in parts:
            pyi_dir = pyi_dir / part
            mock_dir = mock_dir / part
        if not mock_dir.exists():
            mock_dir.mkdir()
        pyi_path = pyi_dir / "__init__.pyi"
        mock_path = mock_dir / "__init__.py"
        LOG.info("Converting %s into %s", pyi_path, mock_path)

        if pyi_path.exists():
            self.convert_file(".".join(["wx"] + parts), pyi_path, mock_path)
        else:
            mock_path.open("wt").close()

        # Scan children
        for path in pyi_dir.glob("*"):
            if path.is_dir():
                self.convert_dir(parts + [path.name])


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    Converter().convert_dir([])
