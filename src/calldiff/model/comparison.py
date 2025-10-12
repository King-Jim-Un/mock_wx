"""Call list comparison models"""

from dataclasses import dataclass, field
from difflib import SequenceMatcher
import logging
from typing import Any, List, Optional, NewType, Tuple
import wx

from mock_wx._test_case import CallDifference

from calldiff.constants import LineType

# Constants:
LOG = logging.getLogger(__name__)
_ = wx.GetTranslation


@dataclass
class TextChunk:
    chunk_type: LineType
    text: str


@dataclass
class LineChunks:
    chunks: List[TextChunk] = field(default_factory=list)


@dataclass(repr=False, eq=False)
class HashableCall:
    line_number: int = 0
    name: str = ""
    args: Tuple[str, ...] = ()
    kwargs: Tuple[Tuple[str, str], ...] = field(default_factory=list)
    sorted_kwargs: tuple = field(init=False)

    @staticmethod
    def hashable(obj):
        try:
            hash(obj)
            return obj
        except TypeError:
            return str(obj)

    def __post_init__(self) -> None:
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
        args = list(self.args) + [f"{key}={value}" for key, value in self.kwargs]
        return f"call.{self.name}({', '.join(args)})"

    def to_list(self) -> List[str]:
        return_value = ["call.", self.name, "("]
        subsequent = False
        for arg in self.args:
            if subsequent:
                return_value.append(", ")
            subsequent = True
            return_value.append(arg)
        for kwarg in self.kwargs:
            if subsequent:
                return_value.append(", ")
            subsequent = True
            return_value.append(f"{kwarg[0]}={kwarg[1]}")
        return return_value + [")"]

    def compare(self, other: "HashableCall") -> "ComparisonLine":
        s_list = self.to_list()
        o_list = other.to_list()
        sequence = SequenceMatcher(a=s_list, b=o_list)
        chunks: List[TextChunk] = []
        for op in sequence.get_opcodes():
            if op[0] == "equal":
                for index in range(op[1], op[2]):
                    chunks.append(TextChunk(LineType.EQUAL, s_list[index]))
            elif op[0] == "replace":
                for index in range(op[1], op[2]):
                    chunks.append(TextChunk(LineType.DELETE, s_list[index]))
                for index in range(op[3], op[4]):
                    chunks.append(TextChunk(LineType.INSERT, o_list[index]))
            elif op[0] == "insert":
                for index in range(op[3], op[4]):
                    chunks.append(TextChunk(LineType.INSERT, o_list[index]))
            elif op[0] == "delete":
                for index in range(op[1], op[2]):
                    chunks.append(TextChunk(LineType.DELETE, s_list[index]))
            else:
                assert False
        return ComparisonLine(LineType.REPLACE, self, other, LineChunks(chunks))


@dataclass
class ComparisonLine:
    line_type: LineType
    expect: Optional[HashableCall] = None
    actual: Optional[HashableCall] = None
    line_analysis: LineChunks = field(default_factory=LineChunks)

    def __str__(self):
        if self.line_type == LineType.REPLACE:
            return str(self.line_analysis)
        else:
            return str(self.expect) if self.expect else str(self.actual)


CallList = NewType("CallList", List[HashableCall])


@dataclass
class HashableComparison:
    expect: List[HashableCall] = field(default_factory=list)
    actual: List[HashableCall] = field(default_factory=list)
    comparison_lines: List[ComparisonLine] = field(default_factory=list)

    @classmethod
    def from_exception(cls, error: CallDifference) -> "HashableComparison":
        return_value = cls()
        for index, (name, args, kwargs) in enumerate(error.expect):
            return_value.expect.append(HashableCall(index + 1, name, tuple(args), tuple(kwargs)))
        for index, (name, args, kwargs) in enumerate(error.actual):
            return_value.actual.append(HashableCall(index + 1, name, tuple(args), tuple(kwargs)))
        return return_value

    def compare(self) -> None:
        """Compare the mock against the expectation"""
        sequence = SequenceMatcher(a=self.expect, b=self.actual)
        for op in sequence.get_opcodes():
            if op[0] == "equal":
                for index in range(op[2] - op[1]):
                    self.comparison_lines.append(
                        ComparisonLine(LineType.EQUAL, self.expect[op[1] + index], self.actual[op[3] + index])
                    )
            elif op[0] == "replace":
                self.sub_compare(*op[1:])
            elif op[0] == "insert":
                for index in range(op[3], op[4]):
                    self.comparison_lines.append(ComparisonLine(LineType.INSERT, actual=self.actual[index]))
            elif op[0] == "delete":
                for index in range(op[1], op[2]):
                    self.comparison_lines.append(ComparisonLine(LineType.DELETE, self.expect[index]))
            else:
                assert False

    def sub_compare(self, e_start: int, e_end: int, m_start: int, m_end: int) -> None:
        """Compare a replacement range within an earlier comparison"""
        e_names = [hashable.name for hashable in self.expect[e_start:e_end]]
        a_names = [hashable.name for hashable in self.actual[m_start:m_end]]
        sequence = SequenceMatcher(a=e_names, b=a_names)
        for op in sequence.get_opcodes():
            adj_op = (op[0], op[1] + e_start, op[2] + e_start, op[3] + m_start, op[4] + m_start)
            if adj_op[0] == "equal":
                for index in range(adj_op[2] - adj_op[1]):
                    self.comparison_lines.append(self.expect[adj_op[1] + index].compare(self.actual[adj_op[3] + index]))
            elif adj_op[0] == "replace":
                for index in range(adj_op[1], adj_op[2]):
                    self.comparison_lines.append(ComparisonLine(LineType.DELETE, self.expect[index]))
                for index in range(adj_op[3], adj_op[4]):
                    self.comparison_lines.append(ComparisonLine(LineType.INSERT, actual=self.actual[index]))
            elif adj_op[0] == "insert":
                for index in range(adj_op[3], adj_op[4]):
                    self.comparison_lines.append(ComparisonLine(LineType.INSERT, actual=self.actual[index]))
            elif adj_op[0] == "delete":
                for index in range(adj_op[1], adj_op[2]):
                    self.comparison_lines.append(ComparisonLine(LineType.DELETE, self.expect[index]))
            else:
                assert False

    def __len__(self):
        return len(self.comparison_lines)

    def last_line_num(self) -> int:
        return len(self.expect)
