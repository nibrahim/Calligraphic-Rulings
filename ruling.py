#!/usr/bin/python

import math
import optparse

from reportlab.pdfgen import canvas, textobject, pdfimages
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4

__VERSION__ = "0.1alpha"

# Utility functions
def compute_endpoint(x0, y0, angle):
    "Computes the endpoing for a given angle"
    h = math.sqrt(sum(x**2 for x in A4))
    x = x0 + h * math.cos(math.radians(angle))
    y = y0 + h * math.sin(math.radians(angle))
    return x, y
    

# Functions to draw different things on the canvas
def draw_width_markers(canvas, nw):
    "Draws markers on the right and left indicating pen nib widths"
    for i in range(0, int(300/nw)):
        if i%2 == 0:
            canvas.rect(1*mm, i*nw*mm, 2*mm, nw*mm, stroke = 0, fill = 1)
            canvas.rect(A4[0]-4*mm, i*nw*mm, 2*mm, nw*mm, stroke = 0, fill = 1)
        else:
            canvas.rect(3*mm, i*nw*mm ,2*mm, nw*mm, stroke = 0, fill = 1)
            canvas.rect(A4[0]-2*mm, i*nw*mm, 2*mm, nw*mm, stroke = 0, fill = 1)

def draw_single_line(canvas, position, nib_width, partitions):
    """Draws rulings for a single line of calligraphic text. Returns
    position of last line drawn"""
    offset = position
    canvas.line(1*mm, offset, A4[0], offset)
    for i in (float(x) for x in partitions.split(",")):
        offset += i * nib_width * mm
        canvas.line(1*mm, offset, A4[0], offset)
    return offset


def draw_ruling(canvas, nib_width, partitions, gap, nrulings, top_margin):
    "Draws lines and separators on the page"
    line_height = sum((float(x) for x in partitions.split(",")),0.0) # Sum of the ascenders, descenders and body
    line_height += gap # Add the gap
    canvas.rect(1*mm, 1*mm, A4[0], top_margin * mm * nib_width, stroke = 0, fill = 1)
    for i in range(nrulings):
        position = (top_margin * mm * nib_width) + (i * line_height * nib_width * mm) # Margin + position for the current line
        offset = draw_single_line(canvas, position, nib_width, partitions)
        canvas.rect(1*mm, offset, A4[0], gap * nib_width * mm, stroke = 0, fill = 1)

def draw_lines_for_angle(canvas, angle):
    "Draws a few lines for the given angle"
    for i in range(-200, 500, 20):
        x0, y0 = 0, i*mm
        x1, y1 = compute_endpoint(x0, y0, angle)
        canvas.line(x0, y0, x1, y1)

def draw_angle_lines(canvas, angles):
    "Draws oblique lines to help with pen positioning and serifs"
    angles = (float(x.strip()) for x in angles.split(","))
    for i in angles:
        draw_lines_for_angle(canvas, i)
        
def write_title(canvas, text, partitions):
    canvas.setFillColorRGB(0.7,0.7,0.7)
    canvas.setFont("Times-Italic", 30)
    canvas.setTitle(text)
    canvas.rotate(90)
    canvas.drawString(20*mm, 0 ,"%s (%s)"%(text,partitions))

def status_message(opts, args):
    "Prints a status message for the user"
    return """Ruling.py version %s
------------------------------------------------------------
Creating ruling sheet for '%s'
Output file                            : %s
Nib width                              : %smm
Partitions per line (in nib widths)    : %s
Gap between lines (in nib widths)      : %s
Top margin : (in nib widths)           : %s
Angle markings for angles (in degrees) : %s
------------------------------------------------------------"""%(__VERSION__, opts.title or "untitled", args[1], opts.nib_width,
opts.partitions, opts.gap, opts.top_margin, opts.angles or "No angle markings")

def main(opts, args):
    print status_message(opts, args)
    c = canvas.Canvas(args[1], bottomup = 1, pagesize = A4, cropMarks = True)
    c.setAuthor("ruling.py version %s"%__VERSION__)
    draw_width_markers(c, opts.nib_width)
    draw_ruling(c, opts.nib_width, opts.partitions, opts.gap, opts.rulings, opts.top_margin)
    if opts.angles:
        draw_angle_lines(c, opts.angles)
    if opts.title:
        write_title(c, opts.title, opts.partitions)
    c.showPage()
    c.save()

def parse_options(args):
    parser = optparse.OptionParser()
    parser.add_option("-n", "--nib-width", dest = "nib_width", type=float,
                      help = "Width of the nib specified in millimeters. All other measurements are multiples of this.")
    parser.add_option("-p", "--partitions", dest = "partitions", type="string",
                      help = "Comma separated list of partitions in each line (specified in nib widths)")
    parser.add_option("-g", "--gap", dest = "gap", type=float, help = "gap between lines (specified in nib widths)")
    parser.add_option("--top-margin", dest = "top_margin", default = 2, type = int,
                      help = "Top margin (specified in nib widths). Default is 2")
    parser.add_option("-r", "--rulings", dest = "rulings", default = 10, type=int,
                      help = "How many rulings to draw. Default is 10")
    parser.add_option("-a", "--angle", dest = "angles", type = "string",
                      help = "Comma separated list of angles (in degrees) for which to draw lines on the page (for pen angle, serifs etc.)")
    parser.add_option("-t", "--title", dest = "title", type = "string",
                      help = "A title for this ruling (usually the font name)")

    return parser.parse_args(args)

if __name__ == "__main__":
    import sys
    opts = parse_options(sys.argv)
    main(*opts)

    
