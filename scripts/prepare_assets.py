from pathlib import Path
import shutil
from PIL import Image, ImageOps
ROOT = Path(__file__).resolve().parents[1]
SOURCE_PORTRAIT = Path('/mnt/data/Buck-Kevin.jpg')
SOURCE_DOCUMENTS = {
    Path('/mnt/data/Kevin_Buck_cv(1).pdf'): 'Kevin_Buck_CV.pdf',
    Path('/mnt/data/Kevin_Buck_Research_Statement.pdf'): 'Kevin_Buck_Research_Statement.pdf',
    Path('/mnt/data/Kevin_Buck_Publication_List.pdf'): 'Kevin_Buck_Publication_List.pdf',
}
def prepare_portrait():
    output = ROOT / "assets/images/kevin-buck-portrait.webp"
    output.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(SOURCE_PORTRAIT) as source:
        image = ImageOps.exif_transpose(source).convert("RGB")
        # Fixed 5:6 head-and-shoulders crop; trims the wall outlet at frame right.
        crop_width = min(image.width, 1400)
        crop_height = round(crop_width * 6 / 5)
        left = max(0, min(20, image.width - crop_width))
        top = max(0, min(170, image.height - crop_height))
        image = image.crop((left, top, left + crop_width, top + crop_height))
        image = image.resize((900, 1080), Image.Resampling.LANCZOS)
        image.save(output, "WEBP", quality=82, method=6)
def prepare_documents():
    out=ROOT/'assets/documents'; out.mkdir(parents=True,exist_ok=True)
    for source, filename in SOURCE_DOCUMENTS.items():
        if not source.exists(): raise FileNotFoundError(source)
        shutil.copy2(source,out/filename)
def main():
    if not SOURCE_PORTRAIT.exists(): raise FileNotFoundError(SOURCE_PORTRAIT)
    prepare_portrait(); prepare_documents()
if __name__=='__main__': main()
