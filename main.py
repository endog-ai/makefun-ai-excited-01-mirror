import os, zlib, struct, math
W=H=512
buf=bytearray(W*H*3)

def p(x,y,r,g,b):
 i=(y*W+x)*3; buf[i:i+3]=bytes([r,g,b])

def rect(x0,y0,x1,y1,col):
 for y in range(y0,y1):
  for x in range(x0,x1):
   p(x,y,*col)

def circle(cx,cy,r,col):
 for dy in range(-r,r+1):
  y=cy+dy
  if 0<=y<H:
   dx=int((r*r-dy*dy)**0.5)
   for x in range(cx-dx,cx+dx+1):
    if 0<=x<W:
     p(x,y,*col)
# Sky gradient top half
for y in range(H//2):
  t=y/(H//2-1)
  r=int(70*(1-t)+200*t)
  g=int(30*(1-t)+100*t)
  b=int(120*(1-t)+30*t)
  for x in range(W): p(x,y,r,g,b)
# Sun
circle(W//2, H//2-30, 40, (255,180,80))
# Stars
for i in range(30):
  x=math.floor(math.sin(i*12.9898)*10000)%W
  y=math.floor(math.cos(i*78.233)*10000)% (H//2)
  p(x,y,255,255,255)
# Dune bottom quarter
rect(0, H*3//4, W, H, (180,120,30))
# Flowers
for i in range(200):
  x=math.floor(math.sin(i*5.4321)*10000)%W
  y=H*3//4 + math.floor(math.cos(i*3.1415)*30)% (H//4)
  col=(200,50,150) if i%3==0 else (255,255,255) if i%3==1 else (120,0,180)
  p(x,y,*col)
# Mirror frame
mx0, my0, mx1, my1 = W//2-100, H//2-150, W//2+100, H//2+150
rect(mx0, my0, mx1, my1, (212,175,55))
# Mirror interior gradient
for y in range(my0+5, my1-5):
  t=(y-my0)/(my1-my0)
  r=int(0*(1-t)+80*t)
  g=int(100*(1-t)+0*t)
  b=int(150*(1-t)+200*t)
  for x in range(mx0+5, mx1-5): p(x,y,r,g,b)
# Islands
islands=[(mx0+30, my0+60, 30),(mx0+80, my0+30,20),(mx0+130, my0+80,25)]
for ix,iy,r in islands:
  circle(ix,iy,r,(34,139,34))
  circle(ix,iy+5,r,(80,50,30))
# Waterfalls upward (simple lines)
for ix,iy,r in islands:
  for dy in range(5,30,5):
    x=ix; y=iy-dy
    if 0<=y<H:
      p(x,y,200,255,255)
# Lanterns
for i in range(5):
  x=mx0+10+i*30; y=my0+20
  circle(x,y,6,(255,240,180))
  for dy in range(-2,3):
    for dx in range(-2,3):
      if 0<=x+dx<W and 0<=y+dy<H:
        p(x+dx,y+dy,255,255,200)
# Person silhouette
px, py = mx0+70, my1-10
for dy in range(0,15): p(px, py-dy, 0,0,0)
for dx in range(-3,4): p(px+dx, py-15, 0,0,0)
# Encoder

def png_bytes():
 data=b'\x89PNG\r\n\x1a\n'
 ihdr=struct.pack('>IIBBBBB',W,H,8,2,0,0,0)
 data+=struct.pack('>I',len(ihdr))+b'IHDR'+ihdr+struct.pack('>I',zlib.crc32(b'IHDR'+ihdr)&0xffffffff)
 raw=bytearray()
 for y in range(H):
  raw.append(0)
  start=y*W*3
  raw+=buf[start:start+W*3]
 comp=zlib.compress(bytes(raw))
 data+=struct.pack('>I',len(comp))+b'IDAT'+comp+struct.pack('>I',zlib.crc32(b'IDAT'+comp)&0xffffffff)
 data+=struct.pack('>I',0)+b'IEND'+b''+struct.pack('>I',zlib.crc32(b'IEND')&0xffffffff)
 return data
out=os.environ.get('MAKEFUN_OUTPUT_DIR','/output')
os.makedirs(out,exist_ok=True)
with open(os.path.join(out,'entry.png'),'wb') as f: f.write(png_bytes())
