def normalize(ranges):
    if not ranges:
        return ranges
    old_ranges = sorted(ranges)
    new_ranges = [old_ranges.pop(0)]
    for r in old_ranges:
        if r.intersects(new_ranges[-1]):
            r = r + new_ranges.pop()
        new_ranges.append(r)
    return new_ranges


class RangeList:
    def __init__(self, ranges=None):
        if ranges is None:
            ranges = []
        self.ranges = [Range(b, e) for b, e in ranges]

    def __getitem__(self, index):
        return self.ranges[index]

    def __repr__(self):
        return repr(self.ranges)

    def intersects(self, other):
        if isinstance(other, Range):
            other = RangeList([other])
        return any(any(o.intersects(r) for r in self.ranges) for o in other.ranges)

    def __contains__(self, other):
        if isinstance(other, Range):
            other = RangeList([other])
        return all(any(o in r for r in self.ranges) for o in other.ranges)

    def __add__(self, other):
        if isinstance(other, Range):
            other = RangeList([other])
        return normalize(self.ranges + other.ranges)


class Range(tuple):
    """Tuple subclass for representating a range

    It accepts either two int values, or a iterable containing two int values.

    The first value is begin and the second value is end."""
    def __new__(cls, *args):
        if len(args) == 1:
            args = tuple(args[0])
        if len(args) != 2:
            raise TypeError("Range() requires either a two int values, or an iterable containing two int values")
        if not all(isinstance(arg, int) for arg in args):
            raise TypeError("Range() requires either a two int values, or an iterable containing two int values")
        args = sorted(args)
        return super().__new__(cls, args)

    @property
    def begin(self):
        return self[0]

    @property
    def end(self):
        return self[1]

    def intersects(self, other):
        return other.begin <= self.end and other.end >= self.begin

    def __contains__(self, other):
        if isinstance(other, int):
            other = Range(other, other)
        return other.begin >= self.begin and other.end <= self.end

    def __add__(self, other):
        if not self.intersects(other):
            raise ValueError("Cannot combine non-overlapping Ranges")
        return Range(min(self.begin, other.begin), max(self.end, other.end))
