# macos-icons

Um tema de ícones estilo **macOS 3D Glassmorphism** elegante para Linux, com suporte a sombras suaves estilo Apple, relevos de vidro em 3D, gradientes pastéis/neutros e suporte a PWAs (como ChatGPT e Google Gemini).

## 📌 Créditos e Repositórios Originais

Este tema é baseado e inspirado nos seguintes projetos originais de código aberto:

* **[WhiteSur Icon Theme](https://github.com/vinceliuice/WhiteSur-icon-theme)** por [vinceliuice](https://github.com/vinceliuice) - Tema de ícones estilo macOS para Linux.
* **macos-icons** - Coleção e adaptações de ícones 3D com motor de glassmorfismo automatizado.

---

## 🎨 Destaques do Tema
* **Glassmorphism Engine (`mac_glass_engine.py`)**: Aplica automaticamente sombras e efeito de vidro 3D nos ícones de aplicativos (`apps/scalable`).
* **Dark Mode Engine (`mac_dark_engine.py`)**: Gera o tema escuro (`apps-dark/scalable`) a partir do tema claro.
* **Suporte a PWAs e Web Apps**: Script automatizado (`mac_chrome_apps.sh`) para aplicar o tema em ícones do Chrome/Brave/Edge.
* **Ícones Oficiais Customizados**:
  * **ChatGPT**: Logotipo oficial em preto sobre cartão **Branco Glassmórfico** 3D.
  * **Google Gemini**: Estrela/Sparkle oficial em gradiente azul/roxo sobre vidro escuro.
  * **Apple Finder**: Design oficial 100% autêntico.
  * **Calendário Dinâmico**: Mostra o mês e dia correntes (`update_calendar_date.py`).

---

## 🌙 Modo Escuro

O tema escuro **não** é o tema claro escurecido. Cada ícone é reconstruído
seguindo as regras que a Apple usa nas variantes escuras do macOS/iOS:

* **O cartão escurece, a logo não.** O fundo branco ou colorido vira um bloco
  quase preto tingido com a própria cor do ícone; a arte em cima mantém as
  cores da marca em força total.
* **Nunca inverter a arte.** Inversão transforma o Wilber marrom do GIMP em
  azul e o pássaro azul do Thunderbird em creme — a identidade da marca é
  intocável.
* **Nunca escurecer/dessaturar tudo por igual.** Isso deixa o ícone sujo, não
  desenhado.
* **Resgatar a arte que sumiria.** Uma logo preta em bloco preto é invisível,
  então só a *luminosidade* dela é invertida — matiz e saturação ficam.
* **Ícones que já são escuros** (terminais, IDEs, OBS, Antigravity,
  bb-launcher) são detectados e passam intactos.
* **Quando o cartão *é* a arte, desenhamos à mão** (`dark_handdrawn.py`).
  Recortar o cartão do rosto do Finder ou do "A" da App Store deixa um buraco
  irregular, então essas variantes são desenhadas: Chrome, App Store,
  visualizador de imagens, Tour, engrenagem de ajustes, peça de extensões,
  reprodutor de vídeo, Mapas, Câmera, além do calendário e do bloco de notas.
  O registro é por nome do arquivo claro, mas a busca é pelo *hash da arte* —
  assim todo apelido que embute o mesmo desenho é atendido junto.
* **Finder passa intacto**: a Apple entrega um único ícone do Finder.

```bash
# requer: python3 (numpy, pillow) e rsvg-convert
python3 mac_dark_engine.py                    # reconstrói apps-dark/scalable
python3 mac_dark_engine.py --only firefox,gimp --out /tmp/preview   # prévia
```

Para instalar as duas versões lado a lado, o diretório `macos-icons-dark/`
expõe `apps-dark` como um tema separado (`macos-icons-dark`).

---

## 🚀 Instalação Local

Para instalar na sua máquina local:

```bash
mkdir -p ~/.local/share/icons
ln -s $(pwd) ~/.local/share/icons/macos-icons
touch ~/.local/share/icons/macos-icons/.icon-theme.cache
```

Depois, selecione o tema **macos-icons** no seu gerenciador de aparência (GNOME Tweaks, KDE System Settings, XFCE Appearance, etc.).

---

## 📄 Licença
Distribuído sob os termos da licença GPL-3.0 / MIT em conformidade com os repositórios originais.
