"""Local shim for `pydantic_extra_types.ulid.ULID` used in tests.

Provides a zero-argument constructor that generates a new ULID using
the `python-ulid` package and stringifies cleanly for use in models/JSON.
"""

from __future__ import annotations

from ulid import ULID as _CoreULID  # type: ignore


class ULID:  # noqa: N801 (match expected name)
    def __init__(self, ulid: str | _CoreULID | "ULID" | None = None) -> None:
        if ulid is None:
            self._u = _CoreULID()
        elif isinstance(ulid, ULID):
            self._u = ulid._u
        elif isinstance(ulid, _CoreULID):
            self._u = ulid
        else:
            # Accept string-like inputs
            self._u = _CoreULID.from_str(str(ulid))

    def __str__(self) -> str:  # 26-char Crockford base32
        return str(self._u)

    def __repr__(self) -> str:
        return f"ULID('{self}')"

    # Expose underlying if needed
    @property
    def value(self) -> _CoreULID:
        return self._u

