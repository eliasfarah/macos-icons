import subprocess

def get_brightness(filepath):
    # This command drops the alpha channel and assumes a black background, which might distort.
    # A better way is to calculate mean only where alpha > 0.
    # ImageMagick 7 fx can do this but we might be on ImageMagick 6.
    # A reliable way: convert to grayscale, set transparent to black, calculate mean. Wait, if it's black and transparent is black, it's all black.
    # Actually, a simple resize to 1x1 and get pixel color could work, but let's use a simpler heuristic.
    # Let's just use the previous simple command and see if it's good enough for github-desktop and system-monitor.
    cmd = f"magick '{filepath}' -colorspace gray -format '%[fx:mean]' info: 2>/dev/null"
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    try:
        return float(res.stdout.strip())
    except:
        return 1.0

print("SystemMonitor:", get_brightness('apps/scalable/org.gnome.SystemMonitor.png'))
print("Github Desktop:", get_brightness('apps/scalable/github-desktop.svg'))
print("Git:", get_brightness('apps/scalable/git.svg'))
