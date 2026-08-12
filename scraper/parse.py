from bs4 import BeautifulSoup # type: ignore

def parse_perfume(soup: BeautifulSoup, url: str) -> dict:
    """Extrai nome, marca, notas e acordes de uma página de perfume."""
    name = soup.find("h1").get_text(strip=True)
    brand = soup.find("span", itemprop="brand").get_text(strip=True)

    return {
        "name": name,
        "brand": brand,
        "url": url,
        "accords": parse_accords(soup),
        "notes": parse_pyramid(soup),
    }


def parse_accords(soup: BeautifulSoup) -> list[dict]:
    """
    Extrai os acordes principais do perfume.
    Cada acorde é uma <div class="... rounded-br-lg ...">
    com style="...background: rgb(...); width: X%;"
    e um <span class="truncate"> com o nome.
    """
    accords = []
    for bar in soup.select("div.rounded-br-lg"):
        name_span = bar.select_one("span.truncate")
        if not name_span:
            continue
        accords.append({
            "name": name_span.get_text(strip=True),
            "strength": _extract_width_percentage(bar.get("style", ""))
        })
    return accords


def _extract_width_percentage(style: str) -> float:
    """style='...width: 100%;' -> 1.0"""
    try:
        pct = float(style.split("width:")[1].split("%")[0].strip())
        return pct / 100
    except (IndexError, ValueError):
        return 1.0


def parse_pyramid(soup: BeautifulSoup) -> dict:
    """
    Percorre os containers de nível da pirâmide olfativa e associa
    cada nota à sua posição (top/middle/base).
    """
    result = {"top": [], "middle": [], "base": []}
    containers = soup.select("div.pyramid-level-container")

    for container in containers:
        position = _detect_pyramid_position(container)
        for link in container.select("a.pyramid-note-link"):
            label = link.select_one("span.pyramid-note-label")
            if not label:
                continue
            result[position].append({
                "name": label.get_text(strip=True),
                "prominence": _extract_opacity(link.get("style", ""))
            })
    return result


def _extract_opacity(style: str) -> float:
    """style='opacity: 0.83;' -> 0.83"""
    try:
        val = style.split("opacity:")[1].split(";")[0].strip()
        return float(val)
    except (IndexError, ValueError):
        return 1.0


def _detect_pyramid_position(container) -> str:
    """
    O heading fica em uma <div class="relative"> irmã anterior ao container,
    estrutura: h4.text-center.relative > span.inline-block...uppercase
    com o texto 'Notas de Topo' / 'Notas de Coração' / 'Notas de Fundo' (ou 'Base').
    """
    heading = container.find_previous("h4")
    if not heading:
        return "middle"  # fallback conservador

    label_span = heading.select_one("span.inline-block")
    text = label_span.get_text(strip=True).lower() if label_span else heading.get_text(strip=True).lower()

    if "topo" in text:
        return "top"
    if "coração" in text:
        return "middle"
    if "fundo" in text or "base" in text:
        return "base"

    return "middle"  # fallback se o texto não bater com nenhum padrão esperado