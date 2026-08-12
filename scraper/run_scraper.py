"""
Script executável: lê uma lista de URLs de perfumes, faz scraping e
insere os dados no banco. Rodar com: python -m scraper.run_scraper
"""
from scraper.fetch import fetch_perfume_page
from scraper.parse import parse_perfume
from db.connection import get_connection
from db.insert import insert_perfume

# lista de URLs de teste — trocar por uma lista maior depois de validar
URLS = [
    "https://www.fragrantica.com.br/perfume/EXEMPLO-1.html",
    "https://www.fragrantica.com.br/perfume/EXEMPLO-2.html",
]


def run(urls: list[str]):
    conn = get_connection()
    try:
        for url in urls:
            print(f"Buscando: {url}")
            soup = fetch_perfume_page(url)
            data = parse_perfume(soup, url)
            insert_perfume(conn, data)
            print(f"  -> inserido: {data['brand']} - {data['name']}")
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Erro durante o scraping, rollback aplicado: {e}")
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    run(URLS)