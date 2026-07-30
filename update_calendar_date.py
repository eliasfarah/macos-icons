#!/usr/bin/env python3
"""Keep every Calendar alias in the light and dark themes on today's date."""

from __future__ import annotations

import argparse
import datetime as dt
import os
import subprocess
from pathlib import Path


CALENDAR_NAMES = (
    "calendar.svg",
    "org.gnome.Calendar.svg",
    "org.gnome.calendar.svg",
    "gnome-calendar.svg",
    "google-calendar.svg",
    "web-google-calendar.svg",
    "unity-webapps-google-calendar.svg",
    "office-calendar.svg",
    "stock_calendar.svg",
    "vcalendar.svg",
    "x-office-calendar.svg",
    "xfcalendar.svg",
    "dde-calendar.svg",
    "deepin-calendar.svg",
    "evolution-calendar.svg",
    "io.elementary.calendar.svg",
    "org.deepin.flatdeb.deepin-calendar.svg",
    "org.kde.plasma.calendar.svg",
    "preferences-calendar-and-tasks.svg",
    "solstice-microsoft-outlook-calendar.svg",
    "starcal2.svg",
    "ximian-evolution-calendar.svg",
    "calendar-blue-31.svg",
    "calendar-red-31.svg",
)

PT_WEEKDAYS = ("SEG", "TER", "QUA", "QUI", "SEX", "SÁB", "DOM")


def weekday_label(now: dt.datetime) -> str:
    """Use the desktop language without depending on an installed Python locale."""
    language = ""
    for variable in ("LC_ALL", "LC_TIME", "LANGUAGE", "LANG"):
        candidate = os.environ.get(variable, "").lower()
        if not candidate or candidate in {"c", "c.utf-8", "posix"}:
            continue
        language = candidate
        break
    if language.startswith("pt"):
        return PT_WEEKDAYS[now.weekday()]
    return now.strftime("%a").upper().rstrip(".")


def light_calendar_svg(weekday: str, day: str) -> str:
    return f"""<svg width="64" height="64" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <filter id="shadow" x="-25%" y="-25%" width="150%" height="155%">
      <feDropShadow dx="0" dy="2.6" stdDeviation="2.7" flood-color="#26303d" flood-opacity="0.24"/>
      <feDropShadow dx="0" dy="0.8" stdDeviation="0.7" flood-color="#ffffff" flood-opacity="0.38"/>
    </filter>
    <linearGradient id="paper" x1="8%" y1="0%" x2="90%" y2="100%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="62%" stop-color="#fbfbfc"/>
      <stop offset="100%" stop-color="#edf0f4"/>
    </linearGradient>
    <linearGradient id="rim" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.98"/>
      <stop offset="50%" stop-color="#ffffff" stop-opacity="0.28"/>
      <stop offset="100%" stop-color="#7f8997" stop-opacity="0.34"/>
    </linearGradient>
    <clipPath id="clip"><rect x="4" y="4" width="56" height="56" rx="14"/></clipPath>
  </defs>
  <g filter="url(#shadow)"><rect x="4" y="4" width="56" height="56" rx="14" fill="url(#paper)"/></g>
  <g clip-path="url(#clip)">
    <path d="M4 4H60V25H4Z" fill="#ffffff" opacity="0.44"/>
    <text x="32" y="21.5" font-family="-apple-system, BlinkMacSystemFont, 'SF Pro Text', Inter, Roboto, sans-serif" font-weight="650" font-size="11.5" fill="#ff3b30" text-anchor="middle">{weekday}</text>
    <text x="32" y="49" font-family="-apple-system, BlinkMacSystemFont, 'SF Pro Display', Inter, Roboto, sans-serif" font-weight="600" font-size="28" fill="#1c1c1e" text-anchor="middle">{day}</text>
    <path d="M4 52C20 56 44 54 60 45V60H4Z" fill="#768293" opacity="0.04"/>
  </g>
  <rect x="4.5" y="4.5" width="55" height="55" rx="13.5" fill="none" stroke="url(#rim)" stroke-width="1"/>
</svg>
"""


def dark_calendar_svg(weekday: str, day: str) -> str:
    return f"""<svg width="64" height="64" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <filter id="shadow" x="-25%" y="-25%" width="150%" height="155%">
      <feDropShadow dx="0" dy="2.6" stdDeviation="2.8" flood-color="#000000" flood-opacity="0.46"/>
    </filter>
    <linearGradient id="tile" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#303034"/>
      <stop offset="100%" stop-color="#111114"/>
    </linearGradient>
    <radialGradient id="glow" cx="50%" cy="16%" r="70%">
      <stop offset="0%" stop-color="#ff453a" stop-opacity="0.075"/>
      <stop offset="100%" stop-color="#ff453a" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="rim" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.34"/>
      <stop offset="36%" stop-color="#ffffff" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0.025"/>
    </linearGradient>
    <clipPath id="clip"><rect x="4" y="4" width="56" height="56" rx="14"/></clipPath>
  </defs>
  <g filter="url(#shadow)"><rect x="4" y="4" width="56" height="56" rx="14" fill="url(#tile)"/></g>
  <g clip-path="url(#clip)">
    <rect x="4" y="4" width="56" height="56" fill="url(#glow)"/>
    <path d="M4 4H60V20C43 17 22 17 4 21Z" fill="#ffffff" opacity="0.035"/>
    <text x="32" y="21.5" font-family="-apple-system, BlinkMacSystemFont, 'SF Pro Text', Inter, Roboto, sans-serif" font-weight="650" font-size="11.5" fill="#ff453a" text-anchor="middle">{weekday}</text>
    <text x="32" y="49" font-family="-apple-system, BlinkMacSystemFont, 'SF Pro Display', Inter, Roboto, sans-serif" font-weight="600" font-size="28" fill="#f2f2f7" text-anchor="middle">{day}</text>
  </g>
  <rect x="4.25" y="4.25" width="55.5" height="55.5" rx="13.75" fill="none" stroke="#000000" stroke-opacity="0.34" stroke-width="0.5"/>
  <rect x="4.75" y="4.75" width="54.5" height="54.5" rx="13.25" fill="none" stroke="url(#rim)" stroke-width="0.75"/>
</svg>
"""


def write_theme_calendars(theme_dir: Path, content: str) -> int:
    """Update regular files; symlinks continue pointing at the canonical icon."""
    updated = 0
    for name in CALENDAR_NAMES:
        target = theme_dir / name
        if target.is_symlink() or not target.exists():
            continue
        if target.read_text(encoding="utf-8") != content:
            target.write_text(content, encoding="utf-8")
        updated += 1
    return updated


def refresh_caches(repo: Path) -> None:
    cache_tool = "gtk-update-icon-cache"
    for theme in (repo, repo / "macos-icons-dark"):
        if not (theme / "index.theme").exists():
            continue
        subprocess.run(
            [cache_tool, "-f", "-t", str(theme)],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    for marker in (repo / ".icon-theme.cache", repo / "macos-icons-dark/.icon-theme.cache"):
        marker.touch(exist_ok=True)


def install_timer(script: Path) -> None:
    unit_dir = Path.home() / ".config/systemd/user"
    unit_dir.mkdir(parents=True, exist_ok=True)
    service = unit_dir / "macos-icons-calendar.service"
    timer = unit_dir / "macos-icons-calendar.timer"
    service.write_text(
        f"""[Unit]
Description=Atualiza a data do calendário do macos-icons

[Service]
Type=oneshot
ExecStart=/usr/bin/python3 {script}
""",
        encoding="utf-8",
    )
    timer.write_text(
        """[Unit]
Description=Atualização diária do calendário do macos-icons

[Timer]
OnCalendar=*-*-* 00:01:00
Persistent=true
AccuracySec=30s
Unit=macos-icons-calendar.service

[Install]
WantedBy=timers.target
""",
        encoding="utf-8",
    )
    subprocess.run(["systemctl", "--user", "daemon-reload"], check=True)
    subprocess.run(
        ["systemctl", "--user", "enable", "--now", "macos-icons-calendar.timer"],
        check=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--install-timer",
        action="store_true",
        help="instala e ativa a atualização diária no systemd do usuário",
    )
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="não atualiza os caches dos temas",
    )
    args = parser.parse_args()

    repo = Path(__file__).resolve().parent
    now = dt.datetime.now().astimezone()
    weekday = weekday_label(now)
    day = str(now.day)

    light_count = write_theme_calendars(
        repo / "apps/scalable", light_calendar_svg(weekday, day)
    )
    dark_count = write_theme_calendars(
        repo / "apps-dark/scalable", dark_calendar_svg(weekday, day)
    )
    if not args.no_cache:
        refresh_caches(repo)
    if args.install_timer:
        install_timer(Path(__file__).resolve())

    print(
        f"Calendário atualizado para {weekday} {day}: "
        f"{light_count} arquivos claros e {dark_count} escuros."
    )


if __name__ == "__main__":
    main()
