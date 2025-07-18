from collections.abc import Iterable, Mapping
from re import Pattern
from typing import Any, BinaryIO, TypeVar, overload
from typing_extensions import Self

from django.contrib.auth.models import _AnyUser
from django.contrib.sessions.backends.base import SessionBase
from django.contrib.sites.models import Site
from django.core.files import uploadedfile, uploadhandler
from django.urls import ResolverMatch
from django.utils.datastructures import (
    CaseInsensitiveMapping,
    ImmutableList,
    MultiValueDict,
)

RAISE_ERROR: object = ...
host_validation_re: Pattern[str] = ...

class UnreadablePostError(OSError): ...
class RawPostDataException(Exception): ...

UploadHandlerList = (
    list[uploadhandler.FileUploadHandler]
    | ImmutableList[uploadhandler.FileUploadHandler]
)

T = TypeVar("T")

class HttpHeaders(CaseInsensitiveMapping[str]):
    HTTP_PREFIX: str = ...
    UNPREFIXED_HEADERS: set[str] = ...
    def __init__(self, environ: Mapping[str, Any]) -> None: ...
    @classmethod
    def parse_header_name(cls, header: str) -> str | None: ...
    @classmethod
    def to_wsgi_name(cls, header: str) -> str: ...
    @classmethod
    def to_asgi_name(cls, header: str) -> str: ...
    @classmethod
    def to_wsgi_names(cls, headers: Mapping[str, T]) -> Mapping[str, T]: ...
    @classmethod
    def to_asgi_names(cls, headers: Mapping[str, T]) -> Mapping[str, T]: ...

class MediaType: ...

class HttpRequest:
    GET: QueryDict = ...
    POST: QueryDict = ...
    COOKIES: dict[str, str] = ...
    META: dict[str, Any] = ...
    FILES: MultiValueDict[str, uploadedfile.UploadedFile] = ...
    path: str = ...
    path_info: str = ...
    method: str | None = ...
    resolver_match: ResolverMatch | None = ...
    content_type: str | None = ...
    content_params: dict[str, str] | None = ...
    def __init__(self) -> None: ...
    @property
    def accepted_types(self) -> list[MediaType]: ...
    def get_preferred_type(self, media_types: list[str]) -> str | None: ...
    def accepts(self, media_type: str) -> bool: ...
    def get_host(self) -> str: ...
    def get_port(self) -> str: ...
    def get_full_path(self, force_append_slash: bool = ...) -> str: ...
    def get_full_path_info(self, force_append_slash: bool = ...) -> str: ...
    def get_signed_cookie(
        self,
        key: str,
        default: T = ...,
        salt: str = ...,
        max_age: int | None = ...,
    ) -> str | T: ...
    def get_raw_uri(self) -> str: ...
    def build_absolute_uri(self, location: str | None = ...) -> str: ...
    @property
    def scheme(self) -> str: ...
    def is_secure(self) -> bool: ...
    @property
    def encoding(self) -> str: ...
    @property
    def upload_handlers(self) -> UploadHandlerList: ...
    def is_ajax(self) -> bool: ...
    def parse_file_upload(
        self, META: Mapping[str, Any], post_data: BinaryIO
    ) -> tuple[QueryDict, MultiValueDict[str, uploadedfile.UploadedFile]]: ...
    @property
    def headers(self) -> HttpHeaders: ...
    @property
    def body(self) -> bytes: ...
    def _load_post_and_files(self) -> None: ...
    def close(self) -> None: ...
    def read(self, *args: Any, **kwargs: Any) -> bytes: ...
    def readline(self, *args: Any, **kwargs: Any) -> bytes: ...
    def __iter__(self) -> Iterable[bytes]: ...
    def readlines(self) -> list[bytes]: ...

    # Attributes added by optional parts of Django
    # django.contrib.admin views:
    current_app: str
    # django.contrib.auth.middleware.AuthenticationMiddleware:
    user: _AnyUser
    # django.contrib.sites.middleware.CurrentSiteMiddleware
    site: Site
    # django.contrib.sessions.middleware.SessionMiddleware
    session: SessionBase

class QueryDict(MultiValueDict[str, str]):
    encoding: str = ...
    _mutable: bool = ...
    def __init__(
        self,
        query_string: str | bytes | None = ...,
        mutable: bool = ...,
        encoding: str | None = ...,
    ) -> None: ...
    def setlist(self, key: str, list_: list[str]) -> None: ...
    def setlistdefault(
        self, key: str, default_list: list[str] | None = ...
    ) -> list[str]: ...
    def appendlist(self, key: str, value: str) -> None: ...
    def urlencode(self, safe: str | None = ...) -> str: ...
    @classmethod
    def fromkeys(
        cls,
        iterable: Iterable[bytes | str],
        value: Any = ...,
        mutable: bool = ...,
        encoding: str | None = ...,
    ) -> Self: ...

@overload
def bytes_to_text(s: bytes, encoding: str) -> str: ...
@overload
def bytes_to_text(s: str, encoding: str) -> str: ...
@overload
def bytes_to_text(s: None, encoding: str) -> None: ...
def split_domain_port(host: str) -> tuple[str, str]: ...
def validate_host(host: str, allowed_hosts: Iterable[str]) -> bool: ...
