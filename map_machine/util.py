#!/usr/bin/env python3
#
#  util.py
"""
Utility file.
"""
#
#  Copyright © 2021 Sergey Vartanov <me@enzet.ru>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# stdlib
from dataclasses import dataclass
from typing import Any

__all__ = ["MinMax"]


@dataclass
class MinMax:
	"""Minimum and maximum."""

	min_: Any = None
	max_: Any = None

	def update(self, value: Any) -> None:
		"""Update minimum and maximum with new value."""
		self.min_ = value if not self.min_ or value < self.min_ else self.min_
		self.max_ = value if not self.max_ or value > self.max_ else self.max_

	def delta(self) -> Any:
		"""Difference between maximum and minimum."""
		return self.max_ - self.min_

	def center(self) -> Any:
		"""Get middle point between minimum and maximum."""
		return (self.min_ + self.max_) / 2.0

	def is_empty(self) -> bool:
		"""Check if interval is empty."""
		return self.min_ == self.max_

	def __repr__(self) -> str:
		return f"{self.min_}:{self.max_}"
