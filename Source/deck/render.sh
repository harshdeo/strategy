#!/bin/zsh
# usage: render.sh name   -> exports name.pptx through Keynote and writes r_name/pNN.png
cd "$(dirname "$0")"
open -a Keynote; sleep 3
osascript export_pdf.applescript "$PWD/$1.pptx" "$PWD/$1.pdf" || exit 1
/opt/homebrew/bin/python3 - "$1" <<'PY'
import fitz,os,sys
n=sys.argv[1]; d=fitz.open(f'{n}.pdf'); os.makedirs(f'r_{n}',exist_ok=True)
for i,p in enumerate(d,1): p.get_pixmap(dpi=100).save(f'r_{n}/p{i:02d}.png')
print(d.page_count,'pages',sorted(set(f[3].split('+')[-1] for p in d for f in p.get_fonts())))
for i,p in enumerate(d,1):
    for f in p.get_fonts():
        if any(k in f[3] for k in ('Times','Lucida','Arial','Courier')): print(' page',i,f[3])
PY
