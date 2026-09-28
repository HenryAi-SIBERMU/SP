import os
from pathlib import Path
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.datamodel.base_models import InputFormat
from docling_core.types.doc import ImageRefMode

pdf_paths = [
    r"c:\Users\yooma\OneDrive\Desktop\duniahub\client\23. Celios8-solarpanel\ref\1-s2.0-S2352938523001441-main.pdf",
    r"c:\Users\yooma\OneDrive\Desktop\duniahub\client\23. Celios8-solarpanel\ref\Paper Teduhi Ruang Kota Kami.pdf"
]

out_dir = Path(r"c:\Users\yooma\OneDrive\Desktop\duniahub\client\23. Celios8-solarpanel\tools\parser_docling\Celios8-References\outputs")
out_dir.mkdir(parents=True, exist_ok=True)

pipeline_options = PdfPipelineOptions()
pipeline_options.do_formula_enrichment = False
pipeline_options.generate_picture_images = False

converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
    }
)

for pdf_path in pdf_paths:
    print(f"Parsing {pdf_path}...")
    try:
        result = converter.convert(pdf_path)
        base_name = Path(pdf_path).stem
        out_path = out_dir / f"{base_name}.md"
        print(f"Saving to {out_path}...")
        result.document.save_as_markdown(out_path, image_mode=ImageRefMode.REFERENCED)
        print(f"Done with {base_name}")
    except Exception as e:
        print(f"Error parsing {pdf_path}: {e}")
