#!/usr/bin/env python3
"""Render synthetic CTI four-stage workflow animation."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
out=Path("assets/cti-v2-workflow.gif")
out.parent.mkdir(parents=True,exist_ok=True)
fontdir=Path("/usr/share/fonts/truetype/dejavu")
def f(size,bold=False):
 p=fontdir/("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf")
 return ImageFont.truetype(str(p),size) if p.exists() else ImageFont.load_default()
steps=[("R1 / INTELLIGENCE","Validate sources, confidence and relevance","Analyst-reviewed intelligence report"),("R2 / DETECTION","Map TTPs to existing SIEM telemetry","Draft queries; test in lab before deployment"),("R3 / AUTOMATION","Prepare Sigma, IOC and hunt artifacts","Human approval required for changes"),("R4 / RESPONSE","Produce SITREP and executive brief","Retain provenance and redacted evidence")]
frames=[]
for i,(title,detail,output) in enumerate(steps):
 im=Image.new("RGB",(1200,440),"#091827");d=ImageDraw.Draw(im)
 d.rounded_rectangle((22,22,1178,418),radius=23,fill="#14344a",outline="#51d8be",width=3)
 d.text((55,55),"CTI AUTOMATION CHAIN 2.0",font=f(29,True),fill="#6ce5d0")
 d.text((55,126),title,font=f(37,True),fill="#fff")
 d.text((55,193),detail,font=f(23),fill="#d7eaf1")
 d.text((55,241),output,font=f(20),fill="#b4d1dc")
 for j,label in enumerate(("R1 INTEL","R2 DETECT","R3 DRAFT","R4 REPORT")):
  x=55+j*280
  d.rounded_rectangle((x,305,x+260,358),radius=11,fill="#48d2b7" if j<=i else "#34576a")
  d.text((x+22,320),label,font=f(19,True),fill="#0a2834" if j<=i else "#e6f4f7")
 d.text((55,385),"SYNTHETIC WORKFLOW • OUTPUTS REQUIRE HUMAN VALIDATION",font=f(16),fill="#a6c4d2")
 frames.append(im)
frames[0].save(out,save_all=True,append_images=frames[1:],duration=1250,loop=0,optimize=True)
assert Image.open(out).n_frames==4
