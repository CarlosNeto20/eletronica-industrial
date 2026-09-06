# -*- coding: utf-8 -*-
"""Procura marcadores de erro do LibreOffice Math (glifos vermelhos) no PDF."""
import os, subprocess, sys, glob
import numpy as np
from PIL import Image

pdf = sys.argv[1]
tmp = os.path.join(os.path.dirname(pdf), "_chk")
os.makedirs(tmp, exist_ok=True)
for f in glob.glob(os.path.join(tmp, "*.png")): os.remove(f)
subprocess.run(["pdftoppm", "-r", "120", "-png", pdf, os.path.join(tmp, "c")], check=True)
ruim = 0
for f in sorted(glob.glob(os.path.join(tmp, "*.png"))):
    a = np.asarray(Image.open(f).convert("RGB")).astype(int)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    vermelho = (r > 90) & (r - g > 55) & (r - b > 55)
    n = int(vermelho.sum())
    if n > 3:
        ys, xs = np.nonzero(vermelho)
        print("VERMELHO em %s: %d px, y=%d..%d x=%d..%d"
              % (os.path.basename(f), n, ys.min(), ys.max(), xs.min(), xs.max()))
        ruim += 1
print("paginas com marcador de erro:", ruim)
