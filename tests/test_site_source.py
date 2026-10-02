from pathlib import Path

import yaml

ROOT = Path('.')


def test_navigation_omits_software_page():
    config = yaml.safe_load((ROOT / '_quarto.yml').read_text(encoding='utf-8'))
    left_nav = config['website']['navbar']['left']
    labels = {item['text'] for item in left_nav}
    hrefs = {item['href'] for item in left_nav}
    assert 'Software' not in labels
    assert 'software.qmd' not in hrefs
    assert not (ROOT / 'software.qmd').exists()


def test_brown_email_is_used_everywhere_in_public_source():
    public_files = [
        ROOT / 'index.qmd',
        ROOT / 'contact.qmd',
        ROOT / 'cv.qmd',
        ROOT / '_quarto.yml',
    ]
    combined = '\n'.join(path.read_text(encoding='utf-8') for path in public_files)
    assert 'kevin_buck@brown.edu' in combined
    assert 'kevmbuck@gmail.com' not in combined


def test_teaching_page_has_concise_philosophy_curriculum_and_mentoring_sections():
    text = (ROOT / 'teaching.qmd').read_text(encoding='utf-8')
    assert 'comfortable asking questions' in text
    assert 'make mistakes' in text
    assert 'Linear Algebra for Data Science' in text
    assert 'Transition to Calculus' in text
    assert 'LEMMA' in text
    assert '13 students' not in text
    assert 'Woojeong Kim' not in text
    assert 'Dorothea Gallos' not in text
    assert 'Christiana Gallos' not in text
    assert 'Jessica Babyak' not in text
    assert len(text.split()) < 550


def test_homepage_combines_research_into_three_highlights():
    text = (ROOT / 'index.qmd').read_text(encoding='utf-8')
    assert '## Research highlights' in text
    assert '## Featured projects' not in text
    assert text.count('::: {.research-card}') == 3
    for topic in (
        'Scientific machine learning',
        'Singularity formation',
        'Spectral theory',
    ):
        assert topic in text
    assert '::: {.hero}' in text
    assert '::: {.research-grid}' in text


def test_public_copy_avoids_third_person_self_labels():
    public_files = [
        ROOT / 'index.qmd',
        ROOT / 'research.qmd',
        ROOT / 'publications.qmd',
        ROOT / 'teaching.qmd',
        ROOT / 'cv.qmd',
        ROOT / 'contact.qmd',
        ROOT / '_quarto.yml',
    ]
    combined = '\n'.join(path.read_text(encoding='utf-8') for path in public_files)
    for phrase in (
        'Portrait of Kevin Buck',
        'by Kevin Buck',
        'Kevin Buck is a',
    ):
        assert phrase not in combined


def test_homepage_hides_duplicate_navbar_brand_and_uses_compact_position_line():
    styles = (ROOT / 'styles.scss').read_text(encoding='utf-8')
    home = (ROOT / 'index.qmd').read_text(encoding='utf-8')
    assert '.navbar-brand { display:none; }' in styles
    assert 'Postdoctoral Researcher, Brown University' in home
    assert 'Postdoctoral Researcher in Mathematics  \nBrown University' not in home


def test_homepage_spacing_is_compact():
    styles = (ROOT / 'styles.scss').read_text(encoding='utf-8')
    assert 'min-height:min(34rem,calc(100vh - 5rem))' not in styles
    assert 'padding:clamp(1rem,3vw,2rem) 0' in styles
    assert '.home-section { padding:clamp(2rem,4.5vw,3.5rem) 0;' in styles
    assert 'max-width:17rem; height:auto' in styles
    assert 'aspect-ratio:5/6' not in styles
