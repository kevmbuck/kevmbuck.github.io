from pathlib import Path
import yaml
DATA=Path('data')
def load_yaml(filename): return yaml.safe_load((DATA/filename).read_text(encoding='utf-8'))
def test_publications_have_unique_ids_and_required_fields():
    pubs=load_yaml('publications.yml'); assert len(pubs)>=5
    ids=[p['id'] for p in pubs]; assert len(ids)==len(set(ids))
    for p in pubs:
        assert p['title']; assert 'Kevin Buck' in p['authors']; assert p['status'] in {'published','accepted','submitted','preprint'}; assert p['year']>=2022; assert p.get('links',{}).get('arxiv','').startswith('https://')
def test_featured_publications_include_two_accepted_pinn_papers():
    featured={p['id'] for p in load_yaml('publications.yml') if p.get('featured')}; assert {'pinns-nsch','aa-pinn-phase-transitions'}.issubset(featured)
def test_projects_reference_existing_publications():
    pub_ids={p['id'] for p in load_yaml('publications.yml')}; projects=load_yaml('projects.yml'); assert len(projects)>=4
    for project in projects:
        assert project['id'] and project['title'] and project['summary']; assert set(project.get('publication_ids',[])).issubset(pub_ids)
def test_news_starts_with_brown_postdoc_appointment():
    news=load_yaml('news.yml'); assert str(news[0]['date'])=='2026-08'; assert 'Brown University' in news[0]['text']; assert 'Postdoctoral Researcher' in news[0]['text']
