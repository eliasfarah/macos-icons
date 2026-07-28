#!/bin/bash
# Apply macOS 3D Glassmorphism mask to all Chrome PWA icons

find ~/.local/share/icons -name "chrome-*.png" 2>/dev/null | while read -r icon; do
    tmp_icon="${icon}.tmp.png"
    
    # Apply squircle mask
    magick "$icon" \
      \( +clone -alpha transparent -background none -fill white -stroke none \
         -draw "roundrectangle 0,0 %[fx:w-1],%[fx:h-1] %[fx:w*0.22],%[fx:h*0.22]" \) \
      -compose DstIn -composite "$tmp_icon"
      
    mv "$tmp_icon" "$icon"
    echo "Glassmorphic Chrome PWA: $icon"
done
