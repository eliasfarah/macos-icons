import subprocess
import glob

def process_dark_logo(filepath):
    cmd = f"magick '{filepath}' -colorspace gray -format '%[fx:mean]' info: 2>/dev/null"
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        out = res.stdout.strip()
        if out:
            mean_brightness = float(out)
            print(f"{filepath}: Brightness = {mean_brightness}")
            if mean_brightness < 0.4:
                print("  -> Would invert or lighten this logo")
    except Exception as e:
        print(f"Error: {e}")

for f in glob.glob("apps/scalable/*.png")[:5] + glob.glob("apps/scalable/*.svg")[:5]:
    process_dark_logo(f)
