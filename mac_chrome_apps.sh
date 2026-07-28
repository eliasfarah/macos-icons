#!/bin/bash
# Apply macOS squircle mask to all Chrome PWA icons

find ~/.local/share/icons -name "chrome-*.png" | while read -r icon; do
    # Create a temporary file
    tmp_icon="${icon}.tmp.png"
    
    # Apply squircle mask
    magick "$icon" \
      \( +clone -alpha transparent -background none -fill white -stroke none \
         -draw "roundrectangle 0,0 %[fx:w-1],%[fx:h-1] %[fx:w*0.22],%[fx:h*0.22]" \) \
      -compose DstIn -composite "$tmp_icon"
      
    # Replace original
    mv "$tmp_icon" "$icon"
    echo "Squircled: $icon"
done
