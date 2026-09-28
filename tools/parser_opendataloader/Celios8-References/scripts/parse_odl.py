import os
import sys
import opendataloader_pdf

pdf_paths = [
    r"c:\Users\yooma\OneDrive\Desktop\duniahub\client\23. Celios8-solarpanel\ref\1-s2.0-S2352938523001441-main.pdf",
    r"c:\Users\yooma\OneDrive\Desktop\duniahub\client\23. Celios8-solarpanel\ref\Paper Teduhi Ruang Kota Kami.pdf"
]

out_dir = r"c:\Users\yooma\OneDrive\Desktop\duniahub\client\23. Celios8-solarpanel\tools\parser_opendataloader\Celios8-References\outputs"
os.makedirs(out_dir, exist_ok=True)

print(f"Parsing using OpenDataLoader to {out_dir}...")
try:
    opendataloader_pdf.convert(
        input_path=pdf_paths,
        output_dir=out_dir,
        format="markdown,json,html"
    )
    print("Parsing successful!")
except Exception as e:
    print(f"Error during OpenDataLoader parsing: {e}")
