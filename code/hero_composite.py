from PIL import Image, ImageDraw, ImageFont
import os
PKG=os.path.expanduser("~/workspace/goals/daily-civic-data-brief/hidden_files/nashville-trade-permits-brief-2026-11-07")
src=os.path.join(PKG,"hero_source/media-generation-media-generation-hero-art-trad-0-2df4a62d-dc92-46bb-8c69-0b07c55f54a7.webp")
img=Image.open(src).convert("RGB"); W,H=img.size
# gradient scrim over top 38%
scrim=Image.new("L",(1,int(H*0.42)),0)
for y in range(int(H*0.42)): scrim.putpixel((0,y), int(200*(1-y/(H*0.42))))
scrim=scrim.resize((W,int(H*0.42)))
black=Image.new("RGB",(W,int(H*0.42)),(18,18,18))
img.paste(Image.composite(black, img.crop((0,0,W,int(H*0.42))), scrim), (0,0))
d=ImageDraw.Draw(img)
def font(sz,bold=True):
    p="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    return ImageFont.truetype(p,sz)
x=int(W*0.045)
d.text((x,int(H*0.045)),"87.1%",font=font(int(H*0.115)),fill=(232,163,61))
d.text((x,int(H*0.175)),"of Nashville's dated trade permits were issued",font=font(int(H*0.042)),fill=(245,245,245))
d.text((x,int(H*0.225)),"the same day they were entered",font=font(int(H*0.042)),fill=(245,245,245))
d.text((x,int(H*0.295)),"Nashville Trade Permits - 111,321 entered Oct 2023 to Oct 2026  |  Machine Readable",font=font(int(H*0.021)),fill=(180,220,215))
img.save(os.path.join(PKG,"hero.png"))
open(os.path.join(PKG,"hero-headline.txt"),"w").write("87.1% of Nashville's dated trade permits were issued the same day they were entered (93,345 of 107,210 dated, non-negative gaps)\nSource line: Nashville Trade Permits - 111,321 entered Oct 2023 to Oct 2026 | Machine Readable\n")
print(img.size)
