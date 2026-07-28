#!/usr/bin/env python3
import datetime
import subprocess
from pathlib import Path

def generate_calendar_svg(weekday_str, day_str):
    return f"""<svg width="64" height="64" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- Apple Drop Shadow -->
    <filter id="glass-shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="2.5" stdDeviation="2.5" flood-color="#000000" flood-opacity="0.22" />
    </filter>

    <!-- 3D Bevel/Glass Highlights -->
    <linearGradient id="inner-bevel" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.75" />
      <stop offset="30%" stop-color="#ffffff" stop-opacity="0.0" />
      <stop offset="70%" stop-color="#000000" stop-opacity="0.0" />
      <stop offset="100%" stop-color="#000000" stop-opacity="0.2" />
    </linearGradient>

    <!-- White Card Base Gradient -->
    <linearGradient id="bg-grad-white" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" />
      <stop offset="100%" stop-color="#f1f5f9" />
    </linearGradient>

    <!-- Squircle Clip -->
    <clipPath id="squircle-clip">
      <rect width="56" height="56" x="4" y="4" rx="14" ry="14" />
    </clipPath>
  </defs>

  <!-- Background Base with Shadow -->
  <g filter="url(#glass-shadow)">
    <g clip-path="url(#squircle-clip)">
      <!-- White Base Card -->
      <rect width="56" height="56" x="4" y="4" fill="url(#bg-grad-white)" />
      
      <!-- Red Weekday Text (e.g. Mon / Wed / SEG) -->
      <text x="32" y="21.5" font-family="-apple-system, BlinkMacSystemFont, SF Pro Text, Inter, Roboto, sans-serif" font-weight="600" font-size="11.5" fill="#ff3b30" text-anchor="middle">{weekday_str}</text>
      
      <!-- Date Number (e.g. 27 / 4) -->
      <text x="32" y="49" font-family="-apple-system, BlinkMacSystemFont, SF Pro Display, Inter, Roboto, sans-serif" font-weight="600" font-size="28" fill="#1c1c1e" text-anchor="middle">{day_str}</text>
    </g>
  </g>

  <!-- Glass Bevel Overlay -->
  <rect width="56" height="56" x="4" y="4" rx="14" ry="14" fill="none" stroke="url(#inner-bevel)" stroke-width="1.5" />
</svg>"""

def main():
    now = datetime.datetime.now()
    weekday_str = now.strftime("%a") # e.g. "Mon" or "Wed"
    day_str = str(now.day)          # e.g. "27"
    
    svg_content = generate_calendar_svg(weekday_str, day_str)
    
    repo_dir = Path(__file__).parent.resolve()
    apps_dir = repo_dir / "apps/scalable"
    
    calendar_names = [
        "calendar.svg", "org.gnome.Calendar.svg", "org.gnome.calendar.svg",
        "gnome-calendar.svg", "google-calendar.svg", "web-google-calendar.svg",
        "unity-webapps-google-calendar.svg", "office-calendar.svg", "stock_calendar.svg",
        "vcalendar.svg", "x-office-calendar.svg", "xfcalendar.svg", "dde-calendar.svg",
        "deepin-calendar.svg", "evolution-calendar.svg", "io.elementary.calendar.svg",
        "org.deepin.flatdeb.deepin-calendar.svg", "org.kde.plasma.calendar.svg",
        "preferences-calendar-and-tasks.svg", "solstice-microsoft-outlook-calendar.svg",
        "starcal2.svg", "ximian-evolution-calendar.svg", "calendar-blue-31.svg",
        "calendar-red-31.svg"
    ]
    
    for name in calendar_names:
        target = apps_dir / name
        target.write_text(svg_content, encoding="utf-8")
        
    print(f"Ícones de calendário atualizados para o estilo exato do macOS Sequoia: {weekday_str} {day_str}")
    subprocess.run("touch .icon-theme.cache 2>/dev/null", shell=True, cwd=repo_dir)

if __name__ == "__main__":
    main()
