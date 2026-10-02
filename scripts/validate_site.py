from __future__ import annotations
from pathlib import Path
from urllib.parse import unquote, urlparse
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]; SITE=ROOT/'_site'
STALE_PHRASES=('Postdoctoral Researcher in Mathematics at Indiana University','Indiana University, 2026–present')
def local_target(page:Path, href:str):
    parsed=urlparse(href)
    if parsed.scheme or href.startswith(('mailto:','tel:','#')): return None
    path=unquote(parsed.path)
    if not path: return None
    target=SITE/path.lstrip('/') if path.startswith('/') else page.parent/path
    if target.is_dir(): target=target/'index.html'
    return target.resolve()
def validate():
    errors=[]
    if not SITE.exists(): return ['Rendered site directory _site/ does not exist. Run `quarto render`.']
    for page in sorted(SITE.rglob('*.html')):
        soup=BeautifulSoup(page.read_text(encoding='utf-8'),'html.parser'); text=soup.get_text(' ',strip=True)
        for phrase in STALE_PHRASES:
            if phrase in text: errors.append(f'{page}: stale affiliation phrase: {phrase}')
        for image in soup.select('main img'):
            src=image.get('src',''); alt=image.get('alt')
            decorative = alt == '' and 'presentation' == image.get('role')
            if not decorative and (alt is None or not alt.strip()): errors.append(f'{page}: image has missing or empty alt text: {src}')
            target=local_target(page,src)
            if target is not None and not target.exists(): errors.append(f'{page}: missing image target: {src}')
        for anchor in soup.select('a[href]'):
            href=anchor.get('href',''); target=local_target(page,href)
            if target is not None and not target.exists(): errors.append(f'{page}: broken internal link: {href}')
    return errors
def main():
    errors=validate()
    if errors:
        print('Site validation failed:'); [print(f'- {e}') for e in errors]; return 1
    print('Site validation passed.'); return 0
if __name__=='__main__': raise SystemExit(main())
