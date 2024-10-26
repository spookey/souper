from typing import Collection, Final

APP_NAME: Final[str] = "souper"

ASSET: Final[str] = "asset"
FICON: Final[str] = "favicon.ico"
INDEX: Final[str] = "index.html"
LOGIC: Final[str] = "logic.js"
STORE: Final[str] = "store.json"
STYLE: Final[str] = "style.css"

EXTENSIONS: Final[Collection[str]] = (
    ".gif",
    ".jpeg",
    ".jpg",
    ".png",
)

ERROR_ASSETS: Final[int] = 2
ERROR_BASICS: Final[int] = 1
EXIT_SUCCESS: Final[int] = 0
