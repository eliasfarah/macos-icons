import subprocess

def test_logo(filepath):
    # Test with black background
    cmd_black = f"magick '{filepath}' -background black -flatten -colorspace gray -format '%[fx:mean]' info: 2>/dev/null"
    res_b = subprocess.run(cmd_black, shell=True, capture_output=True, text=True)
    try:
        mean_b = float(res_b.stdout.strip())
    except:
        mean_b = 1.0
        
    print(f"{filepath}: mean_black_bg = {mean_b}")
    if mean_b < 0.1:
        print("   -> DETECTED AS DARK LOGO (needs invert)")

test_logo('apps/scalable/github-desktop.svg')
test_logo('apps/scalable/git.svg')
test_logo('apps/scalable/org.gnome.SystemMonitor.png')
test_logo('apps/scalable/org.gnome.Calculator.png')
