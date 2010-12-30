#!/usr/bin/python

import optparse

from reportlab.pdfgen import canvas, textobject, pdfimages
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4



def draw_width_markers(canvas, nw):
    for i in range(0, int(300/nw)):
        if i%2 == 0:
            canvas.rect(1*mm, i*nw*mm, 2*mm, nw*mm, stroke = 0, fill = 1)
            canvas.rect(A4[0]-4*mm, i*nw*mm, 2*mm, nw*mm, stroke = 0, fill = 1)
        else:
            canvas.rect(3*mm, i*nw*mm ,2*mm, nw*mm, stroke = 0, fill = 1)
            canvas.rect(A4[0]-2*mm, i*nw*mm, 2*mm, nw*mm, stroke = 0, fill = 1)

def draw_single_line(canvas, position, nib_width, partitions):
    "Draws rulings for a single line of calligraphic text"
    print "Drawing at %s"%position
    offset = position
    canvas.line(1*mm, offset, A4[0], offset)
    for i in (float(x) for x in partitions.split(",")):
        offset += i * nib_width * mm
        canvas.line(1*mm, offset, A4[0], offset)
        print i,"   ",offset
    print 20*"-"


def draw_ruling(canvas, nib_width, partitions, gap, nrulings, top_margin):
    "Draws lines and separators on the page"
    line_height = sum((float(x) for x in partitions.split(",")),0.0) # Sum of the ascenders, descenders and body
    line_height += gap # Add the gap
    print "Line height ", line_height
    print nrulings
    for i in range(nrulings):
        position = (top_margin * mm * nib_width) + (i * line_height * nib_width * mm) # Margin + position for the current line
        draw_single_line(canvas, position, nib_width, partitions)
    # idx = 0
    # segments = [float(x) for x in partitions.split(",")]
    # segments.append(gap)
    # for i in range(0, 5): #int(300/nw)):
    #     for j in segments:
    #         canvas.line(1*mm, segno + i*j*nw*mm, A4[0], segno + i*j*nw*mm)
    #         segno += i*j*mm*nw
        

def main(opts, args):
    c = canvas.Canvas(args[1], bottomup = 1, pagesize = A4, cropMarks = True)
    draw_width_markers(c, opts.nib_width)
    draw_ruling(c, opts.nib_width, opts.partitions, opts.gap, opts.rulings, opts.tmargin)
    c.showPage()
    c.save()

def parse_options(args):
    parser = optparse.OptionParser()
    parser.add_option("-n", "--nib-width", dest = "nib_width", type=float,
                      help = "Width of the nib specified in millimeters. All other measurements are multiples of this.")
    parser.add_option("-p", "--partitions", dest = "partitions", type="string",
                      help = "comma separated list of partitions in each line (specified in nib widths)")
    parser.add_option("-g", "--gap", dest = "gap", type=float, help = "gap between lines (specified in nib widths)")
    parser.add_option("-r", "--rulings", dest = "rulings", default = 10, type=int,
                      help = "How many rulings to draw")
    parser.add_option("-t","--top-margin", dest = "tmargin", default = 2, type = int,
                      help = "Top margin (specified in nib widths)")
    return parser.parse_args(args)

if __name__ == "__main__":
    import sys
    opts = parse_options(sys.argv)
    main(*opts)

    
