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
  * **Calendário Dinâmico**: Mostra o dia da semana e a data correntes nos
    modos claro e escuro (`update_calendar_date.py`).

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
  irregular, então essas variantes são redesenhadas: Finder, Conexões, Chrome, App Store,
  visualizador de imagens, Tour, engrenagem de ajustes, peça de extensões,
  reprodutor de vídeo, Mapas, Câmera, além do calendário e do bloco de notas.
  O registro é por nome do arquivo claro, mas a busca é pelo *hash da arte* —
  assim todo apelido que embute o mesmo desenho é atendido junto.
* **Placeholders vazios são reparados por nome.** Alguns arquivos claros
  trazem apenas um cartão sem marca e, pior, aplicativos diferentes compartilham
  exatamente o mesmo placeholder. O modo escuro fornece desenhos próprios para
  Celeste, Inscryption, Papers Please, OpenRA D2K, OneShot, Stardew Valley,
  Terraria, Undertale, SimpleX Chat, Clapgrep, Roblox e Ricochlime.
* **Finder tem variante escura própria**: rosto azul escultural deslocado
  sobre cartão grafite Liquid Glass, com olhos assimétricos e sorriso bicolor.
* **Conexões é um par claro/escuro próprio**: globo técnico, rota ativa e
  cursor escultural, com contraste e materiais calibrados para cada aparência.

```bash
# requer: python3 (numpy, pillow) e rsvg-convert
python3 mac_dark_engine.py                    # reconstrói apps-dark/scalable
python3 mac_dark_engine.py --only firefox,gimp --out /tmp/preview   # prévia
```

Para instalar as duas versões lado a lado, o diretório `macos-icons-dark/`
expõe `apps-dark` como um tema separado (`macos-icons-dark`).

### Calendário dinâmico

Para atualizar imediatamente e ativar a atualização diária às 00:01:

```bash
./update_calendar_date.py --install-timer
```

O timer é instalado somente para o usuário atual, é persistente (também
atualiza depois de uma máquina desligada no horário programado) e preserva os
aliases dos ícones. Para uma atualização manual, basta executar
`./update_calendar_date.py`.

### Voltar ao design anterior

O design anterior está preservado no commit `35d02af`. Para comparar antes de
trocar os arquivos instalados, sempre gere uma prévia com `--out /tmp/preview`.
Se preferir integralmente a versão anterior:

```bash
git restore --source=35d02af -- mac_dark_engine.py dark_handdrawn.py apps-dark/scalable
touch macos-icons-dark/.icon-theme.cache
```

---

## 🚀 Instalação Local

Para instalar na sua máquina local:

```bash
mkdir -p ~/.local/share/icons
ln -s $(pwd) ~/.local/share/icons/macos-icons
touch ~/.local/share/icons/macos-icons/.icon-theme.cache
```

Depois, selecione o tema **macos-icons** no seu gerenciador de aparência (GNOME Tweaks, KDE System Settings, XFCE Appearance, etc.).

No GNOME, o painel **Aplicativos** pede por padrão um ícone simbólico preto.
Para fazê-lo usar a arte colorida do tema:

```bash
install -Dm644 desktop-overrides/gnome-applications-panel.desktop \
  ~/.local/share/applications/gnome-applications-panel.desktop
update-desktop-database ~/.local/share/applications
```

---

## 📄 Licença
Distribuído sob os termos da licença GPL-3.0 / MIT em conformidade com os repositórios originais.
