#!/usr/bin/python

import optparse

from reportlab.pdfgen import canvas, textobject, pdfimages
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4



def draw_ruling(canvas):
    for i in range(0,150,2):
        canvas.rect(1*mm, i*2*mm, 3*mm, 2*mm, stroke = 1, fill = 1)
        canvas.rect(4*mm, (i+1)*2*mm, 3*mm, 2*mm, stroke = 1, fill = 1)
        
        

def main(opts, args):
    c = canvas.Canvas(args[0], bottomup = 1, pagesize = A4, cropMarks = True)
    draw_ruling(c)
    c.showPage()
    c.save()

def parse_options(args):
    parser = optparse.OptionParser()
    parser.add_option("-n","--nib-width", dest = "nib_width",
                      help = "Width of the nib specified in millimeters. All other measurements are multiples of this.")
    return parser.parse_args(args)

if __name__ == "__main__":
    import sys
    opts = parse_options(sys.argv)
    main(*opts)

    
