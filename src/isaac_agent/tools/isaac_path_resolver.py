"""
Auto-detect The Binding of Isaac: Repentance paths on the user's machine.

Finds:
- Mods folder: ".../steamapps/common/The Binding of Isaac Rebirth/mods"
- Log file:    ".../Documents/My Games/Binding of Isaac Repentance/log.txt"

Supports Windows, Linux (native + Steam Deck / Proton), and macOS.
"""

import os
import sys
from pathlib import Path
from typing import Optional, Tuple

from loguru import logger


def _find_steam_root() -> Optional[Path]:
    """Locate the Steam installation root directory."""
    system = sys.platform

    if system == "win32":
        candidates = [
            Path("C:/Program Files (x86)/Steam"),
            Path("C:/Program Files/Steam"),
            Path("D:/Steam"),
            Path("E:/Steam"),
        ]
        for c in candidates:
            if c.exists():
                return c

    elif system == "darwin":
        c = Path.home() / "Library/Application Support/Steam"
        if c.exists():
            return c

    else:  # Linux / Steam Deck
        for c in [
            Path.home() / ".steam/steam",
            Path.home() / ".local/share/Steam",
            Path.home() / ".var/app/com.valvesoftware.Steam/.steam/steam",  # Flatpak
        ]:
            if c.exists():
                return c

    return None


def _find_steam_libraries(steam_root: Path) -> list[Path]:
    """Parse libraryfolders.vdf to find all Steam library directories."""
    libraries = [steam_root]
    vdf_path = steam_root / "steamapps/libraryfolders.vdf"
    if not vdf_path.exists():
        return libraries

    try:
        content = vdf_path.read_text(encoding="utf-8", errors="replace")
        import re
        for match in re.finditer(r'"path"\s+"([^"]+)"', content):
            lib_path = Path(match.group(1))
            if lib_path.exists():
                libraries.append(lib_path)
    except Exception:
        pass

    return libraries


_ISAAC_MODS_SUFFIX = "steamapps/common/The Binding of Isaac Rebirth/mods"


def find_isaac_mods_dir() -> Optional[Path]:
    """Auto-detect the Isaac mods folder.

    Returns the first matching path, or None.
    """
    # 1. Check ISAAC_MOD_DIR env var / config override
    from isaac_agent.config import settings
    env_path = os.environ.get("ISAAC_MOD_DIR", settings.isaac_mod_dir)
    if env_path and env_path != "./mods":
        p = Path(env_path)
        if p.exists():
            logger.info(f"Using ISAAC_MOD_DIR from config: {p}")
            return p

    # 2. Try common absolute paths directly (fast path for Windows)
    candidates: list[Path] = []
    system = sys.platform

    if system == "win32":
        # Common Windows Steam library locations
        for drive in "CDEFGH":
            for lib in [
                f"{drive}:/SteamLibrary",
                f"{drive}:/Steam",
                f"{drive}:/Program Files (x86)/Steam",
                f"{drive}:/Program Files/Steam",
            ]:
                p = Path(lib) / _ISAAC_MODS_SUFFIX
                candidates.append(p)
    elif system == "darwin":
        candidates.append(
            Path.home() / "Library/Application Support/Steam" / _ISAAC_MODS_SUFFIX
        )
    else:
        candidates.extend([
            Path.home() / ".steam/steam" / _ISAAC_MODS_SUFFIX,
            Path.home() / ".local/share/Steam" / _ISAAC_MODS_SUFFIX,
        ])

    for p in candidates:
        if p.exists():
            logger.info(f"Found Isaac mods dir: {p}")
            return p

    # 3. Search through Steam library folders
    steam_root = _find_steam_root()
    if steam_root:
        for lib in _find_steam_libraries(steam_root):
            p = lib / _ISAAC_MODS_SUFFIX
            if p.exists():
                logger.info(f"Found Isaac mods dir via Steam lib: {p}")
                return p

    # 4. Broad search in common locations (last resort)
    broad_candidates: list[Path] = []
    if system == "win32":
        for drive in "CDEFGH":
            broad_candidates.append(Path(f"{drive}:/"))
        broad_candidates.append(Path.home())
    else:
        broad_candidates.append(Path.home())

    needle = "The Binding of Isaac Rebirth"
    for root in broad_candidates:
        if not root.exists():
            continue
        try:
            for found in root.rglob(needle):
                if found.is_dir():
                    mods = found / "mods"
                    if mods.exists():
                        logger.info(f"Found Isaac mods dir via search: {mods}")
                        return mods
        except (PermissionError, OSError):
            continue

    logger.warning("Could not auto-detect Isaac mods folder")
    return None


# Common log file paths per platform
_LOG_CANDIDATES: dict[str, list[Path]] = {
    "win32": [
        Path.home() / "Documents/My Games/Binding of Isaac Repentance/log.txt",
        Path.home() / "Documents/My Games/The Binding of Isaac Repentance/log.txt",
        Path.home() / "Documents/My Games/Binding of Isaac Rebirth/log.txt",
    ],
    "darwin": [
        Path.home() / "Library/Application Support/Binding of Isaac Repentance/log.txt",
        Path.home() / "Library/Application Support/The Binding of Isaac Repentance/log.txt",
    ],
    "linux": [
        Path.home() / ".local/share/binding of isaac repentance/log.txt",
        Path.home() / ".local/share/Steam/steamapps/compatdata/250900/pfx/drive_c/users/steamuser/Documents/My Games/Binding of Isaac Repentance/log.txt",
        Path.home() / ".steam/steam/steamapps/compatdata/250900/pfx/drive_c/users/steamuser/Documents/My Games/Binding of Isaac Repentance/log.txt",
    ],
}


def find_isaac_log_file() -> Optional[Path]:
    """Auto-detect the Isaac log.txt file.

    Returns the first matching path, or None.
    """
    candidates = _LOG_CANDIDATES.get(sys.platform, _LOG_CANDIDATES["linux"])

    for p in candidates:
        if p.exists():
            logger.info(f"Found Isaac log file: {p}")
            return p

    # Try broad search under Documents / home
    home = Path.home()
    needle = "Binding of Isaac Repentance"
    try:
        for found in home.rglob(needle):
            if found.is_dir():
                log_file = found / "log.txt"
                if log_file.exists():
                    logger.info(f"Found Isaac log file via search: {log_file}")
                    return log_file
    except (PermissionError, OSError):
        pass

    logger.warning("Could not auto-detect Isaac log.txt")
    return None


def resolve_all_paths() -> dict:
    """Resolve both mods dir and log file. Returns dict with keys 'mods_dir' and 'log_file'."""
    return {
        "mods_dir": str(find_isaac_mods_dir()) if find_isaac_mods_dir() else None,
        "log_file": str(find_isaac_log_file()) if find_isaac_log_file() else None,
    }
