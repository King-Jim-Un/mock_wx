"""Call list comparison models"""

from dataclasses import dataclass, field
from difflib import SequenceMatcher
import logging
from typing import Any, List, Optional, NewType
from unittest.mock import _Call, Mock
import wx

from calldiff.constants import LineType

# Constants:
LOG = logging.getLogger(__name__)
_ = wx.GetTranslation


@dataclass(eq=False)
class SubCall:
    comparable: Any
    printable: str

    def __hash__(self) -> int:
        return hash(self.comparable)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, SubCall) and self.comparable == other.comparable


@dataclass
class TextChunk:
    chunk_type: LineType
    text: str


@dataclass
class LineChunks:
    chunks: List[TextChunk] = field(default_factory=list)


@dataclass(repr=False, eq=False)
class HashableCall:
    the_call: _Call
    line_number: int = 0
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
        args = [repr(arg) for arg in self.args] + [f"{key}={repr(value)}" for key, value in self.kwargs]
        return f"call.{self.name}({', '.join(args)})"

    def to_list(self) -> List[SubCall]:
        return_value = [SubCall("call.", "call."), SubCall(self.name, self.name), SubCall("(", "(")]
        subsequent = False
        for arg in self.args:
            if subsequent:
                return_value.append(SubCall(", ", ", "))
            subsequent = True
            return_value.append(SubCall(arg, repr(arg)))
        for kwarg in self.kwargs:
            if subsequent:
                return_value.append(SubCall(", ", ", "))
            subsequent = True
            return_value.append(SubCall(kwarg, f"{kwarg[0]}={repr(kwarg[1])}"))
        return return_value + [SubCall(")", ")")]

    def compare(self, other: "HashableCall") -> "ComparisonLine":
        s_list = self.to_list()
        o_list = other.to_list()
        sequence = SequenceMatcher(a=s_list, b=o_list)
        chunks: List[TextChunk] = []
        for op in sequence.get_opcodes():
            if op[0] == "equal":
                for index in range(op[1], op[2]):
                    chunks.append(TextChunk(LineType.EQUAL, s_list[index].printable))
            elif op[0] == "replace":
                for index in range(op[1], op[2]):
                    chunks.append(TextChunk(LineType.DELETE, s_list[index].printable))
                for index in range(op[3], op[4]):
                    chunks.append(TextChunk(LineType.INSERT, o_list[index].printable))
            elif op[0] == "insert":
                for index in range(op[3], op[4]):
                    chunks.append(TextChunk(LineType.INSERT, o_list[index].printable))
            elif op[0] == "delete":
                for index in range(op[1], op[2]):
                    chunks.append(TextChunk(LineType.DELETE, s_list[index].printable))
            else:
                assert False
        return ComparisonLine(LineType.REPLACE, self, other, LineChunks(chunks))


@dataclass
class ComparisonLine:
    line_type: LineType
    expect: Optional[HashableCall] = None
    mock: Optional[HashableCall] = None
    line_analysis: LineChunks = field(default_factory=LineChunks)

    def __str__(self):
        if self.line_type == LineType.REPLACE:
            return str(self.line_analysis)
        else:
            return str(self.expect) if self.expect else str(self.mock)


CallList = NewType("CallList", List[HashableCall])


@dataclass
class HashableComparison:
    expect: List[_Call] = field(default_factory=list)
    mock: _Call = field(default_factory=Mock)
    comparison_lines: List[ComparisonLine] = field(default_factory=list)

    def compare(self) -> None:
        """Compare the mock against the expectation"""
        hash_expect = CallList([HashableCall(item, index + 1) for index, item in enumerate(self.expect)])
        hash_mock = CallList([HashableCall(item) for item in self.mock.mock_calls])

        sequence = SequenceMatcher(a=hash_expect, b=hash_mock)
        for op in sequence.get_opcodes():
            if op[0] == "equal":
                for index in range(op[2] - op[1]):
                    self.comparison_lines.append(
                        ComparisonLine(LineType.EQUAL, hash_expect[op[1] + index], hash_mock[op[3] + index])
                    )
            elif op[0] == "replace":
                self.sub_compare(hash_expect, hash_mock, *op[1:])
            elif op[0] == "insert":
                for index in range(op[3], op[4]):
                    self.comparison_lines.append(ComparisonLine(LineType.INSERT, mock=hash_mock[index]))
            elif op[0] == "delete":
                for index in range(op[1], op[2]):
                    self.comparison_lines.append(ComparisonLine(LineType.DELETE, hash_expect[index]))
            else:
                assert False

    def sub_compare(
        self, hash_expect: CallList, hash_mock: CallList, e_start: int, e_end: int, m_start: int, m_end: int
    ) -> None:
        """Compare a replacement range within an earlier comparison"""
        e_names = [hashable.name for hashable in hash_expect[e_start:e_end]]
        m_names = [hashable.name for hashable in hash_mock[m_start:m_end]]
        sequence = SequenceMatcher(a=e_names, b=m_names)
        for op in sequence.get_opcodes():
            adj_op = (op[0], op[1] + e_start, op[2] + e_start, op[3] + m_start, op[4] + m_start)
            if adj_op[0] == "equal":
                for index in range(adj_op[2] - adj_op[1]):
                    self.comparison_lines.append(hash_expect[adj_op[1] + index].compare(hash_mock[adj_op[3] + index]))
            elif adj_op[0] == "replace":
                for index in range(adj_op[1], adj_op[2]):
                    self.comparison_lines.append(ComparisonLine(LineType.DELETE, hash_expect[index]))
                for index in range(adj_op[3], adj_op[4]):
                    self.comparison_lines.append(ComparisonLine(LineType.INSERT, mock=hash_mock[index]))
            elif adj_op[0] == "insert":
                for index in range(adj_op[3], adj_op[4]):
                    self.comparison_lines.append(ComparisonLine(LineType.INSERT, mock=hash_mock[index]))
            elif adj_op[0] == "delete":
                for index in range(adj_op[1], adj_op[2]):
                    self.comparison_lines.append(ComparisonLine(LineType.DELETE, hash_expect[index]))
            else:
                assert False

    def __len__(self):
        return len(self.comparison_lines)

    def last_line_num(self) -> int:
        return len(self.expect)
