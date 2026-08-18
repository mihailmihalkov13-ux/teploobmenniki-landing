import os
from PIL import Image, ImageOps

SRC = r"C:\Users\floyu\Downloads"
DST = r"C:\Users\floyu\сайт тепло\img"

os.makedirs(DST, exist_ok=True)

# name -> (source file, crop box or None, max_dim)
JOBS = {
    # hero / about
    "hero-production.jpg":    ("5462933014942784254.jpg", None, 1400),
    "about-warehouse.jpg":    ("5462933014942784250.jpg", (0, 0, 650, 960), 1200),

    # gallery / production line
    "gallery-lineup.jpg":     ("5462933014942784255.jpg", None, 1400),
    "gallery-unit-tall.jpg":  ("5462933014942784253.jpg", None, 1200),
    "gallery-unit-red.jpg":   ("5462933014942784252.jpg", None, 1200),
    "gallery-three-units.jpg":("5462933014942784251.jpg", (40, 0, 1240, 960), 1400),
    "gallery-packing.jpg":    ("5462933014942784248.jpg", None, 1200),
    "gallery-four-units.jpg": ("5462933014942784249.jpg", None, 1200),

    # before / after service
    "before-plate-hand.jpg":  ("5462933014942784237.jpg", None, 1200),
    "after-plate-flat.jpg":   ("5462933014942784234.jpg", (30, 100, 700, 1260), 1100),
    "before-plates-two.jpg":  ("5462933014942784245.jpg", (0, 180, 960, 1280), 1200),
    "after-plate-bucket.jpg": ("5462933014942784243.jpg", (0, 150, 960, 1280), 1200),
    "before-after-single.jpg":("5462933014942784238.jpg", (0, 90, 960, 1280), 1200),
    "before-installed.jpg":   ("5462933014942784242.jpg", (0, 70, 960, 1280), 1200),
}

for out_name, (src_name, box, max_dim) in JOBS.items():
    src_path = os.path.join(SRC, src_name)
    im = Image.open(src_path)
    im = ImageOps.exif_transpose(im)
    if box:
        im = im.crop(box)
    w, h = im.size
    scale = max_dim / max(w, h)
    if scale < 1:
        im = im.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
    out_path = os.path.join(DST, out_name)
    im.convert("RGB").save(out_path, "JPEG", quality=82, optimize=True)
    print(out_name, im.size, os.path.getsize(out_path) // 1024, "KB")
