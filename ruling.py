#!/usr/bin/python

import optparse

from reportlab.pdfgen import canvas, textobject, pdfimages
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4



def draw_ruling(canvas, nw):
    for i in range(0, int(300/nw)):
        if i%2 == 0:
            canvas.rect(1*mm, i*nw*mm, 2*mm, nw*mm, stroke = 0, fill = 1)
        else:
            canvas.rect(3*mm, i*nw*mm ,2*mm, nw*mm, stroke = 0, fill = 1)
        

def main(opts, args):
    c = canvas.Canvas(args[1], bottomup = 1, pagesize = A4, cropMarks = True)
    draw_ruling(c, opts.nib_width)
    c.showPage()
    c.save()

def parse_options(args):
    parser = optparse.OptionParser()
    parser.add_option("-n","--nib-width", dest = "nib_width", type=float,
                      help = "Width of the nib specified in millimeters. All other measurements are multiples of this.")
    return parser.parse_args(args)

if __name__ == "__main__":
    import sys
    opts = parse_options(sys.argv)
    main(*opts)

    
