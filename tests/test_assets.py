from pathlib import Path
from PIL import Image
DOCUMENTS=Path('assets/documents'); IMAGES=Path('assets/images')
def test_public_documents_exist_with_clean_names():
    expected={'Kevin_Buck_CV.pdf','Kevin_Buck_Research_Statement.pdf','Kevin_Buck_Publication_List.pdf'}
    assert expected=={p.name for p in DOCUMENTS.glob('*.pdf')}
    for filename in expected: assert (DOCUMENTS/filename).stat().st_size>10_000
def test_portrait_is_web_optimized():
    portrait=IMAGES/'kevin-buck-portrait.webp'; assert portrait.exists()
    with Image.open(portrait) as image:
        assert image.format=='WEBP'; assert image.width==900; assert image.height==1080
    assert portrait.stat().st_size<350_000
