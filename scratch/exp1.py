from dataclasses import dataclass, field
from difflib import SequenceMatcher
from typing import List, Any
from unittest.mock import Mock, call, mock_open, _Call


@dataclass(eq=False)
class SubCall:
    comparable: Any
    printable: str

    def __hash__(self) -> int:
        return hash(self.comparable)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, SubCall) and self.comparable == other.comparable


@dataclass(repr=False, eq=False)
class HashableCall:
    the_call: _Call
    name: str = field(init=False)
    args: tuple = field(init=False)
    kwargs: tuple = field(init=False)
    sorted_kwargs: tuple = field(init=False)

    @staticmethod
    def hashable(obj):
        try:
            hash(obj)
            return obj
        except TypeError:
            return str(obj)

    def __post_init__(self) -> None:
        self.name, args, kwargs = self.the_call
        self.args = tuple(self.hashable(arg) for arg in args)
        self.kwargs = tuple((self.hashable(key), self.hashable(value)) for key, value in kwargs.items())
        self.sorted_kwargs = tuple(sorted(self.kwargs, key=lambda obj: obj[0]))

    def __hash__(self) -> int:
        return hash((self.name, self.args, self.sorted_kwargs))

    def __eq__(self, other: Any) -> bool:
        return (
            isinstance(other, HashableCall)
            and self.name == other.name
            and self.args == other.args
            and self.sorted_kwargs == other.sorted_kwargs
        )

    def __repr__(self) -> str:
        args = [str(arg) for arg in self.args] + [f"{key}={value}" for key, value in self.kwargs]
        return f"call.{self.name}({', '.join(args)})"

    def to_list(self) -> List[SubCall]:
        return_value = [SubCall("call.", "call."), SubCall(self.name, self.name), SubCall("(", "(")]
        subsequent = False
        for arg in self.args:
            if subsequent:
                return_value.append(SubCall(", ", ", "))
            subsequent = True
            return_value.append(SubCall(arg, str(arg)))
        for kwarg in self.kwargs:
            if subsequent:
                return_value.append(SubCall(", ", ", "))
            subsequent = True
            return_value.append(SubCall(kwarg, f"{kwarg[0]}={kwarg[1]}"))
        return return_value + [SubCall(")", ")")]

    def compare(self, other: "HashableCall"):
        s_list = self.to_list()
        o_list = other.to_list()
        sequence = SequenceMatcher(a=s_list, b=o_list)
        text = ""
        for op in sequence.get_opcodes():
            if op[0] == "equal":
                for index in range(op[1], op[2]):
                    text += s_list[index].printable
            elif op[0] == "replace":
                for index in range(op[1], op[2]):
                    text += f"<-{s_list[index].printable}>"
                for index in range(op[3], op[4]):
                    text += f"<+{o_list[index].printable}>"
            elif op[0] == "insert":
                for index in range(op[3], op[4]):
                    text += f"<+{o_list[index].printable}>"
            elif op[0] == "delete":
                for index in range(op[1], op[2]):
                    text += f"<-{s_list[index].printable}>"
            else:
                assert False
        print(f"   {text}")

@dataclass
class HashableComparison:
    expect: List[_Call]
    mock: _Call
    hash_expect: List[HashableCall] = field(init=False)
    hash_mock: List[HashableCall] = field(init=False)

    def __post_init__(self) -> None:
        self.hash_expect = [HashableCall(item) for item in self.expect]
        self.hash_mock = [HashableCall(item) for item in self.mock.mock_calls]

    def compare(self):
        sequence = SequenceMatcher(a=self.hash_expect, b=self.hash_mock)
        for op in sequence.get_opcodes():
            if op[0] == "equal":
                for index in range(op[1], op[2]):
                    print(f"=  {self.hash_expect[index]}")
            elif op[0] == "replace":
                self.sub_compare(*op[1:])
            elif op[0] == "insert":
                for index in range(op[3], op[4]):
                    print(f"+  {self.hash_mock[index]}")
            elif op[0] == "delete":
                for index in range(op[1], op[2]):
                    print(f"-  {self.hash_expect[index]}")
            else:
                assert False

    def sub_compare(self, e_start, e_end, m_start, m_end):
        e_names = [hashable.name for hashable in self.hash_expect[e_start:e_end]]
        m_names = [hashable.name for hashable in self.hash_mock[m_start:m_end]]
        sequence = SequenceMatcher(a=e_names, b=m_names)
        for op in sequence.get_opcodes():
            adj_op = (op[0], op[1] + e_start, op[2] + e_start, op[3] + m_start, op[4] + m_start)
            if adj_op[0] == "equal":
                for index in range(adj_op[2] - adj_op[1]):
                    self.hash_expect[adj_op[1] + index].compare(self.hash_mock[adj_op[3] + index])
            elif adj_op[0] == "replace":
                for index in range(adj_op[1], adj_op[2]):
                    print(f" - {self.hash_expect[index]}")
                for index in range(adj_op[3], adj_op[4]):
                    print(f" + {self.hash_mock[index]}")
            elif adj_op[0] == "insert":
                for index in range(adj_op[3], adj_op[4]):
                    print(f" + {self.hash_mock[index]}")
            elif adj_op[0] == "delete":
                for index in range(adj_op[1], adj_op[2]):
                    print(f" - {self.hash_expect[index]}")
            else:
                assert False


def main():
    mock = Mock()
    mock_open(mock.open, "some read data")
    mock.one()
    mock.two.three().four()
    mock.five(6, 7, 8, 9, 10, eleven=12, thirteen=14).thirteen("fourteen")
    with mock.open("test", "rt") as file_obj:
        mock.write(file_obj.read())
    expect = [
        call.one(),
        call.two.three(),
        call.two.three().four(),
        call.five(6, 7, 8, 9, 10, thirteen=14, eleven=12),
        call.five().thirteen("fourteen"),
        call.open("tst", "rt"),
        call.open("tet", "rt"),
        call.open().__enter__(),
        call.open().read(),
        call.write("some read data"),
        call.open().__exit__(None, None, None),
        call.open().close(),
    ]
    HashableComparison(expect, mock).compare()

"""
HashableComparison(
expect=[call.one(), call.two.three(), call.two.three().four(), call.five(6, 7, 8, 9, 10, thirteen=14, eleven=12), call.five().thirteen('fourteen'), call.open('tst', 'rt'), call.open('tet', 'rt'), call.open().__enter__(), call.open().read(), call.write('some read data'), call.open().__exit__(None, None, None), call.open().close()], 
mock=<Mock id='2679956694960'>, 
comparison_lines=[
ComparisonLine(line_type=<LineType.EQUAL: 1>, expect=call.one(), mock=call.one(), line_analysis=[]), 
ComparisonLine(line_type=<LineType.EQUAL: 1>, expect=call.two.three(), mock=call.two.three(), line_analysis=[]), 
ComparisonLine(line_type=<LineType.EQUAL: 1>, expect=call.two.three().four(), mock=call.two.three().four(), line_analysis=[]), 
ComparisonLine(line_type=<LineType.EQUAL: 1>, expect=call.five(6, 7, 8, 9, 10, thirteen=14, eleven=12), mock=call.five(6, 7, 8, 9, 10, eleven=12, thirteen=14), line_analysis=[]), 
ComparisonLine(line_type=<LineType.EQUAL: 1>, expect=call.five().thirteen(fourteen), mock=call.five().thirteen(fourteen), line_analysis=[]), 
ComparisonLine(line_type=<LineType.REPLACE: 4>, expect=call.open(tst, rt), mock=call.open(test, rt), line_analysis=[
TextChunk(chunk_type=<LineType.EQUAL: 1>, text='call.'), 
TextChunk(chunk_type=<LineType.EQUAL: 1>, text='open'), 
TextChunk(chunk_type=<LineType.EQUAL: 1>, text='('), 
TextChunk(chunk_type=<LineType.DELETE: 3>, text="'tst'"), 
TextChunk(chunk_type=<LineType.INSERT: 2>, text="'test'"), 
TextChunk(chunk_type=<LineType.EQUAL: 1>, text=', '), 
TextChunk(chunk_type=<LineType.EQUAL: 1>, text="'rt'"), 
TextChunk(chunk_type=<LineType.EQUAL: 1>, text=')')
]), 
ComparisonLine(line_type=<LineType.DELETE: 3>, expect=call.open(tet, rt), mock=None, line_analysis=[]), 
ComparisonLine(line_type=<LineType.EQUAL: 1>, expect=call.open().__enter__(), mock=call.open().__enter__(), line_analysis=[]), 
ComparisonLine(line_type=<LineType.EQUAL: 1>, expect=call.open().read(), mock=call.open().read(), line_analysis=[]), 
ComparisonLine(line_type=<LineType.EQUAL: 1>, expect=call.write(some read data), mock=call.write(some read data), line_analysis=[]), 
ComparisonLine(line_type=<LineType.EQUAL: 1>, expect=call.open().__exit__(None, None, None), mock=call.open().__exit__(None, None, None), line_analysis=[]), 
ComparisonLine(line_type=<LineType.EQUAL: 1>, expect=call.open().close(), mock=call.open().close(), line_analysis=[])
])
"""

if __name__ == "__main__":
    main()
