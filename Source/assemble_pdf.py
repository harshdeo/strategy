"""Assemble high-resolution rendered slides with a searchable native-text layer.

The visible page is the Artifact Tool render of the final PPTX. The invisible text
layer comes only from that same PPTX, for search/accessibility; no screenshot OCR,
text substitution or screenshot fabrication. PPTX remains the editable master.
"""
import sys,re
from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
import fitz
source,images,out=map(Path,sys.argv[1:]);ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main'}
font='/Users/harsh/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/poppler/fonts/DejaVuSans.ttf'
doc=fitz.open()
with ZipFile(source) as z:
    dim=E.fromstring(z.read('ppt/presentation.xml')).find('p:sldSz',ns)
    width,height=[int(dim.get(k))/12700 for k in ['cx','cy']]
    for i,image in enumerate(sorted(images.glob('*.png')),1):
        page=doc.new_page(width=width,height=height);page.insert_image(page.rect,filename=str(image))
        page.insert_font(fontname='anvest',fontfile=font)
        tree=E.fromstring(z.read(f'ppt/slides/slide{i}.xml'))
        for shape in tree.xpath('//p:sp',namespaces=ns):
            text=' '.join(shape.xpath('.//a:t/text()',namespaces=ns))
            if not text:continue
            xform=shape.find('.//a:xfrm',ns)
            if xform is None:continue
            off=xform.find('a:off',ns);ext=xform.find('a:ext',ns)
            if off is None or ext is None:continue
            x,y,cx,cy=[int(obj.get(k))/12700 for obj,k in [(off,'x'),(off,'y'),(ext,'cx'),(ext,'cy')]]
            rect=fitz.Rect(max(0,x),max(0,y),min(width,x+cx),min(height,y+max(cy,5)))
            for size in [8,6,4,2,1]:
                spare=page.insert_textbox(rect,text,fontname='anvest',fontsize=size,render_mode=3,overlay=True)
                if spare>=0:break
            else:raise RuntimeError(f'Text layer does not fit slide {i}')
        # Native tables are searchable in row order, at their own slide location.
        for frame in tree.xpath('//p:graphicFrame',namespaces=ns):
            tables=frame.xpath('.//a:tbl',namespaces=ns)
            if not tables:continue
            off=frame.find('p:xfrm/a:off',ns);ext=frame.find('p:xfrm/a:ext',ns)
            if off is None or ext is None:continue
            x,y,cx,cy=[int(obj.get(k))/12700 for obj,k in [(off,'x'),(off,'y'),(ext,'cx'),(ext,'cy')]]
            text='\n'.join(' '.join(row.xpath('.//a:t/text()',namespaces=ns)) for row in tables[0].findall('a:tr',ns))
            page.insert_textbox(fitz.Rect(x,y,x+cx,y+cy),text,fontname='anvest',fontsize=5,render_mode=3)
        page.insert_text((42,height-10),'Anvest · Confidential · 20 Oct 2026',fontname='anvest',fontsize=5,render_mode=3)
    doc.set_metadata({'title':source.stem.replace('_',' '),'author':'Anvest','subject':'Investor materials, 20 October 2026','creator':'Rendered from editable PPTX; original product screenshots preserved'})
    doc.save(out,garbage=4,deflate=True)
print(out)
