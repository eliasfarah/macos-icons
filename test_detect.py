import subprocess
import os

def is_flat_icon(filepath):
    # Render SVG to a 64x64 PNG in memory and get the alpha value at (32, 2) and (32, 62)
    # If both are fully transparent (alpha=0), it's highly likely a flat icon without a full background.
    # If they are opaque, it has a background.
    cmd = [
        "convert",
        "-background", "none",
        "-resize", "64x64!",
        filepath,
        "-format", "%[fx:u.p{32,2}.a] %[fx:u.p{32,62}.a]",
        "info:"
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        alphas = result.stdout.strip().split()
        if len(alphas) == 2:
            a1, a2 = float(alphas[0]), float(alphas[1])
            # if alpha is 0, it's transparent
            if a1 < 0.1 and a2 < 0.1:
                return True
            else:
                return False
    except Exception as e:
        pass
    return True # default to flat if error

print("Test fonts.svg (should be flat or square depending on theme):", is_flat_icon("apps/scalable/fonts.svg"))
print("Test hwloc.svg (has background):", is_flat_icon("apps/scalable/hwloc.svg"))
