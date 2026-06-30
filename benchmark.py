from collections.abc import Iterator
from dataclasses import dataclass, field
from io import BufferedRandom
from socket import socket
from timeit import timeit
from typing import Any

from pynicotine.slskmessages import FileAttributes

Incomplete = Any


class BasicTransfer:
    """This class holds information about a single transfer."""

    __slots__ = (
        "sock",
        "username",
        "virtual_path",
        "folder_path",
        "token",
        "size",
        "file_handle",
        "start_time",
        "current_byte_offset",
        "last_byte_offset",
        "transferred_bytes_total",
        "speed",
        "avg_speed",
        "time_elapsed",
        "time_left",
        "modifier",
        "queue_position",
        "file_attributes",
        "iterator",
        "status",
        "legacy_attempt",
        "retry_attempt",
        "size_changed",
        "is_backslash_path",
        "is_lowercase_path",
        "request_timer_id",
    )

    def __init__(
        self,
        username: str,
        virtual_path: str | None = None,
        folder_path: str | None = None,
        size: int = 0,
        file_attributes: FileAttributes | None = None,
        status: str | None = None,
        current_byte_offset: None = None,
    ):
        self.username: str = username
        self.virtual_path: str | None = virtual_path
        self.folder_path: str | None = folder_path
        self.size: int = size
        self.status: str | None = status
        self.current_byte_offset: int | None = current_byte_offset
        self.file_attributes: FileAttributes | None = file_attributes

        self.sock: socket | None = None
        self.file_handle: BufferedRandom | None = None
        self.token: int | None = None
        self.queue_position: int = 0
        self.modifier: None = None
        self.request_timer_id: int | None = None
        self.start_time: float | None = None
        self.last_byte_offset: int | None = None
        self.transferred_bytes_total: int = 0
        self.speed: float = 0
        self.avg_speed: int = 0
        self.time_elapsed: float = 0
        self.time_left: int = 0
        # Can be a "Gtk.TreeIterator", not sure how the GTK side of things work though
        self.iterator: int | None | Iterator[Incomplete] = None
        self.legacy_attempt: bool = False
        self.retry_attempt: bool = False
        self.size_changed: bool = False
        self.is_backslash_path: bool = False
        self.is_lowercase_path: bool = False

        if file_attributes is None:
            self.file_attributes = FileAttributes()


@dataclass()
class DataclassTransfer:
    """This class holds information about a single transfer."""

    username: str
    virtual_path: str | None = None
    folder_path: str | None = None
    size: int = 0
    status: str | None = None
    current_byte_offset: int | None = None
    file_attributes: FileAttributes | None = field(default_factory=FileAttributes)

    sock: socket | None = field(default=None, init=False)
    file_handle: BufferedRandom | None = field(default=None, init=False)
    token: int | None = field(default=None, init=False)
    queue_position: int = field(default=0, init=False)
    modifier: None = field(default=None, init=False)
    request_timer_id: int | None = field(default=None, init=False)
    start_time: float | None = field(default=None, init=False)
    last_byte_offset: int | None = field(default=None, init=False)
    transferred_bytes_total: int = field(default=0, init=False)
    speed: float = field(default=0, init=False)
    avg_speed: int = field(default=0, init=False)
    time_elapsed: float = field(default=0, init=False)
    time_left: int = field(default=0, init=False)
    # Can be a "Gtk.TreeIterator". Not sure how the GTK side of things work though
    iterator: int | None | Iterator[Incomplete] = field(default=None, init=False)
    legacy_attempt: bool = field(default=False, init=False)
    retry_attempt: bool = field(default=False, init=False)
    size_changed: bool = field(default=False, init=False)
    is_backslash_path: bool = field(default=False, init=False)
    is_lowercase_path: bool = field(default=False, init=False)


globals = {
    "username": "LoremIpsum",
    "virtual_path": r"@@dolor\Sit\Amet Consectetur\Adipiscing Elit\04 Vivamus Metus nibh Ornare.mp3",
    "folder_path": "/neque/vulputate/.fringilla/imperdiet/felis/neque",
    "size": 9597175,
    "status": "Finished",
    "current_byte_offset": 9597175,
    "file_attributes": None,
}

ITERATIONS = 100_000_000
OLD_CONSTRUCTOR = "BasicTransfer(" + ", ".join(globals.keys()) + ")"
NEW_CONSTRUCTOR = "DataclassTransfer(" + ", ".join(globals.keys()) + ")"
OLD_GLOBALS = {**globals, "BasicTransfer": BasicTransfer}
NEW_GLOBALS = {**globals, "DataclassTransfer": DataclassTransfer}

old_time = timeit(OLD_CONSTRUCTOR, number=ITERATIONS, globals=OLD_GLOBALS)
new_time = timeit(NEW_CONSTRUCTOR, number=ITERATIONS, globals=NEW_GLOBALS)

print("Constructor duration:", f"{old_time=}", f"{new_time=}", sep="\n\t")

new_time = timeit(
    "it.file_attributes = None",
    setup=f"it = {NEW_CONSTRUCTOR}",
    number=ITERATIONS,
    globals=NEW_GLOBALS,
)
old_time = timeit(
    "it.file_attributes = None",
    setup=f"it = {OLD_CONSTRUCTOR}",
    number=ITERATIONS,
    globals=OLD_GLOBALS,
)
print("Setting attributes:", f"{old_time=}", f"{new_time=}", sep="\n\t")
