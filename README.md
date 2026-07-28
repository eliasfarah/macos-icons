# macOS 3D Prime Icons for Linux (AZ-OS-3D)

Um tema de ícones estilo **macOS 3D Glassmorphism** elegante para Linux, com suporte a sombras suaves estilo Apple, relevos de vidro em 3D, gradientes pastéis/neutros e suporte a PWAs (como ChatGPT e Google Gemini).

## 📌 Créditos e Repositórios Originais

Este tema é baseado e inspirado nos seguintes projetos originais de código aberto:

* **[WhiteSur Icon Theme](https://github.com/vinceliuice/WhiteSur-icon-theme)** por [vinceliuice](https://github.com/vinceliuice) - Tema de ícones estilo macOS para Linux.
* **AZ-OS-3D-Prime-Icons** - Coleção e adaptações de ícones 3D com motor de glassmorfismo automatizado.

---

## 🎨 Destaques do Tema
* **Glassmorphism Engine (`mac_glass_engine.py`)**: Aplica automaticamente sombras e efeito de vidro 3D nos ícones de aplicativos (`apps/scalable`).
* **Suporte a PWAs e Web Apps**: Script automatizado (`mac_chrome_apps.sh`) para aplicar o tema em ícones do Chrome/Brave/Edge.
* **Ícones Oficiais Customizados**:
  * **ChatGPT**: Logotipo oficial em preto sobre cartão **Branco Glassmórfico** 3D.
  * **Google Gemini**: Estrela/Sparkle oficial em gradiente azul/roxo sobre vidro escuro.
  * **Apple Finder**: Design fiel de duas metades ciano/azul com relevo 3D.
  * **Calendário Dinâmico**: Mostra o mês e dia correntes (`update_calendar_date.py`).

---

## 🚀 Instalação Local

Para instalar na sua máquina local:

```bash
mkdir -p ~/.local/share/icons
ln -s $(pwd) ~/.local/share/icons/AZ-OS-3D-Prime-Icons
touch ~/.local/share/icons/AZ-OS-3D-Prime-Icons/.icon-theme.cache
```

Depois, selecione o tema **AZ-OS-3D** no seu gerenciador de aparência (GNOME Tweaks, KDE System Settings, XFCE Appearance, etc.).

---

## 📄 Licença
Distribuído sob os termos da licença GPL-3.0 / MIT em conformidade com os repositórios originais.
