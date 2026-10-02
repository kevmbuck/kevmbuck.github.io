from pathlib import Path
from bs4 import BeautifulSoup

SITE=Path('_site')
EXPECTED_PAGES={'index.html':'Kevin Buck','research.html':'Research','publications.html':'Publications','teaching.html':'Teaching','cv.html':'CV','contact.html':'Contact'}

def test_expected_pages_exist():
    for name in EXPECTED_PAGES:
        assert (SITE/name).exists()
    assert not (SITE/'software.html').exists()

def test_navigation_labels():
    soup=BeautifulSoup((SITE/'index.html').read_text(encoding='utf-8'),'html.parser')
    labels={a.get_text(' ',strip=True) for a in soup.select('nav a')}
    expected={'Research','Publications','Teaching','CV','Contact'}
    assert expected.issubset(labels)
    assert 'Software' not in labels

def test_homepage_hero_and_links():
    soup=BeautifulSoup((SITE/'index.html').read_text(encoding='utf-8'),'html.parser')
    hero=soup.select_one('.hero'); assert hero
    assert len(soup.select('main h1')) == 1
    assert soup.select_one('main h1').get_text(strip=True) == 'Kevin Buck'
    text=hero.get_text(' ',strip=True); assert 'Kevin Buck' in text and 'Postdoctoral Researcher, Brown University' in text
    hrefs={a.get('href') for a in hero.select('a[href]')}; assert 'assets/documents/Kevin_Buck_CV.pdf' in hrefs; assert 'https://github.com/kevmbuck' in hrefs; assert any(h and 'scholar.google.com' in h for h in hrefs); assert 'mailto:kevin_buck@brown.edu' in hrefs

def test_portrait_is_decorative_without_third_person_alt_text():
    image=BeautifulSoup((SITE/'index.html').read_text(encoding='utf-8'),'html.parser').select_one('.hero img')
    assert image
    assert image.get('alt','') == ''

def test_homepage_publications_match_catalog_metadata():
    import yaml
    publications = yaml.safe_load(Path('data/publications.yml').read_text(encoding='utf-8'))
    expected_ids = ['defocusing-nls-blowup', 'magnetic-double-wells', 'aa-pinn-phase-transitions', 'pinns-nsch']
    by_id = {publication['id']: publication for publication in publications}
    soup = BeautifulSoup((SITE/'index.html').read_text(encoding='utf-8'), 'html.parser')
    highlights = soup.select('article.publication-item')
    assert len(highlights) == len(expected_ids)
    for highlight, publication_id in zip(highlights, expected_ids):
        publication = by_id[publication_id]
        assert highlight.select_one('h3').get_text(strip=True) == publication['title']
        assert highlight.select_one('h3 a')['href'] == publication['links'].get('journal', publication['links']['arxiv'])
        assert highlight.select_one('.status-badge').get_text(strip=True) == publication['status']
        assert highlight.select_one('.publication-authors').get_text(strip=True) == ', '.join(publication['authors'])
