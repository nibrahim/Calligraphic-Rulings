#!/usr/bin/python

import math
import optparse

from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4, A3
 
page_sizes = {"A4" : A4,
              "A3" : A3}


__VERSION__ = "0.1alpha"

# Utility functions
def compute_endpoint(x0, y0, angle, pagesize, h = False):
    "Computes the endpoint for a given angle"
    if not h:
        h = math.sqrt(sum(x**2 for x in pagesize))
    x = x0 + h * math.cos(math.radians(angle))
    y = y0 + h * math.sin(math.radians(angle))
    return x, y

# Functions to draw different things on the canvas
def draw_linear_width_markers(canvas, nw, pagesize):
    "Draws markers on the right and left indicating pen nib widths"
    for i in range(0, int(300/nw)):
        if i%2 == 0:
            canvas.rect(1*mm, i*nw*mm, 2*mm, nw*mm, stroke = 0, fill = 1)
            canvas.rect(pagesize[0]-4*mm, i*nw*mm, 2*mm, nw*mm, stroke = 0, fill = 1)
        else:
            canvas.rect(3*mm, i*nw*mm ,2*mm, nw*mm, stroke = 0, fill = 1)
            canvas.rect(pagesize[0]-2*mm, i*nw*mm, 2*mm, nw*mm, stroke = 0, fill = 1)

def draw_line_set(canvas, position, nib_width, partitions, pagesize):
    """Draws rulings for a single line of calligraphic text. Returns
    position of last line drawn"""
    offset = position
    canvas.line(1*mm, offset, pagesize[0], offset)
    for i in (float(x) for x in partitions.split(",")):
        offset += i * nib_width * mm
        canvas.line(1*mm, offset, pagesize[0], offset)
    return offset

    
def draw_lines(canvas, nib_width, partitions, gap, nrulings, top_margin, pagesize):
    "Draws lines and separators on the page"
    line_height = sum((float(x) for x in partitions.split(",")),0.0) # Sum of the ascenders, descenders and body
    line_height += gap # Add the gap
    canvas.rect(1*mm, 1*mm, pagesize[0], top_margin * mm * nib_width, stroke = 0, fill = 1)
    for i in range(nrulings):
        position = (top_margin * mm * nib_width) + (i * line_height * nib_width * mm) # Margin + position for the current line
        offset = draw_line_set(canvas, position, nib_width, partitions, pagesize)
        canvas.rect(1*mm, offset, pagesize[0], gap * nib_width * mm, stroke = 0, fill = 1)

# def draw_radial_width_markers(canvas, center, nib_width):
#     for i in range(0, int(300/nw)):
#         if i%2 == 0:
#             canvas.rect(1*mm, i*nw*mm, 2*mm, nw*mm, stroke = 0, fill = 1)
#             canvas.rect(A4[0]-4*mm, i*nw*mm, 2*mm, nw*mm, stroke = 0, fill = 1)
#         else:
#             canvas.rect(3*mm, i*nw*mm ,2*mm, nw*mm, stroke = 0, fill = 1)
#             canvas.rect(A4[0]-2*mm, i*nw*mm, 2*mm, nw*mm, stroke = 0, fill = 1)



def draw_circle_set(canvas, x, y, radius, nib_width, partitions):
    """
    Draws concentric circles of the given radius. 
    """
    offset = radius
    for i in (float(x) for x in partitions.split(",")):
        canvas.circle(x, y, offset, fill = 1)
        offset -= i *nib_width * mm

    return offset

def draw_circles(canvas, nib_width, partitions, gap, nrulings, top_margin, center):
    "Draws circles and separators on the page"
    partition_radius = sum((float(x) for x in partitions.split(",")),0.0) # Sum of the ascenders, descenders and body
    partition_radius += gap # Add the gap

    offset = nrulings * partition_radius * nib_width * mm
    
    for i in range(nrulings, 1, -1):
        # Draw gap
        canvas.setFillColorRGB(0, 0, 0, 1)
        canvas.circle(center[0], center[1], offset, fill = 1, stroke = 1)
        offset -= gap *nib_width * mm
        # Draw partitions
        canvas.setFillColorRGB(1, 1, 1, 1)
        offset = draw_circle_set(canvas, center[0], center[1], offset, nib_width, partitions)

    # Draw initial inner margin
    canvas.setFillColorRGB(0.5, 0.5, 0.5, 1)
    canvas.circle(center[0], center[1], offset, fill = 1, stroke = 1)



def draw_lines_for_angle(canvas, angle, distance, pagesize):
    "Draws a few lines for the given angle"    
    x = pagesize[0]
    y = 0
    move_angle = 90 + angle
    m = math.tan(math.radians(angle))
    while True:
        d = distance*mm
        xr = pagesize[0]
        yr = m * (xr - x) + y
        canvas.line(x, y, xr, yr)
        
        yl = 0
        xl = (yl - y + m*x)/m
        if xl < 0:
            xl = 0
            yl = m * (xl - x) + y
        canvas.line(x, y, xl, yl)
        
        if xr < 0 or yl > pagesize[1]:
            break

        # canvas.circle(x, y, 10, fill = 1, stroke = 1)        
        x, y = compute_endpoint(x, y, move_angle, pagesize, d)



def draw_angle_lines(canvas, angles, distance, pagesize):
    "Draws oblique lines to help with pen positioning and serifs"
    angles = (float(x.strip()) for x in angles.split(","))
    for i in angles:
        draw_lines_for_angle(canvas, i, distance, pagesize)
        
def write_title_and_credits(canvas, text, nib_width, partitions, angles, pagesize, horizontal = False):
    canvas.setFillColorRGB(0, 0, 0, 1)
    if not horizontal:
        canvas.rotate(90)
    t = canvas.beginText()
    if text:
        canvas.setTitle(text)
        t.setTextOrigin(10*mm, 3*mm)
        t.setFont("Times-Italic", 20)
        t.textOut(text)
        t.setFont("Times-Italic", 10)
        t.textOut("  (%smm nib, Partitions:%s, angles:%s)"%(nib_width, partitions, angles))

    # canvas.setFillColorRGB(0, 0, 0, 0.2)
    # w,l = (float(x)/100 for x in A4)
    # print w,",",l
    if not horizontal:
        t.setTextOrigin(10*mm, -pagesize[0]-5*mm)
    t.setFont("Times-Roman", 10)
    t.textOut(" Generated using ")
    t.setFont("Times-Italic", 10)
    t.textOut("http://noufalibrahim.name/rulings")
    canvas.drawText(t)


def status_message(opts, args):
    "Prints a status message for the user"
    if opts.radial:
        style = "radial"
    else:
        style = "linear"
    return """Ruling.py version %s
------------------------------------------------------------
Creating %s ruling sheet for '%s' (size %s)
Output file                            : %s
Nib width                              : %smm
Partitions per line (in nib widths)    : %s
Gap between lines (in nib widths)      : %s
Top margin : (in nib widths)           : %s
Angle markings for angles (in degrees) : %s
------------------------------------------------------------"""%(__VERSION__, style, opts.title or "untitled", opts.pagesize, args[1], opts.nib_width,
opts.partitions, opts.gap, opts.top_margin, opts.angles or "No angle markings")

def main(opts, args):
    pagesize = page_sizes[opts.pagesize]
    c = canvas.Canvas(args[1], bottomup = 1, pagesize = pagesize, cropMarks = True)
    c.setAuthor("ruling.py version %s"%__VERSION__)
    c.setFillColorRGB(0.1, 0.1, 0.1, 0.5)
    if not opts.radial:
        draw_linear_width_markers(c, opts.nib_width, pagesize)
        draw_lines(c, opts.nib_width, opts.partitions, opts.gap, opts.rulings, opts.top_margin, pagesize)
        if opts.angles:
            draw_angle_lines(c, opts.angles, opts.distance, pagesize)
    else:
        x, y = pagesize
        center = (x/2.0, y/2.0)
        # draw_radial_width_markers(c, center, opts.nib_width)
        draw_circles(c, opts.nib_width, opts.partitions, opts.gap, opts.rulings, opts.top_margin, center)

    write_title_and_credits(c, opts.title, opts.nib_width, opts.partitions, opts.angles, pagesize, opts.radial)

    c.showPage()
    c.save()

def parse_options(args):
    parser = optparse.OptionParser(usage = "%s [options] output_file"%args[0])
    parser.add_option("-w", "--nib-width", dest = "nib_width", type=float,
                      help = "Width of the nib specified in millimeters. All other measurements are multiples of this.")
    parser.add_option("-p", "--partitions", dest = "partitions", type="string",
                      help = "Comma separated list of partitions in each line (specified in nib widths)")
    parser.add_option("-g", "--gap", dest = "gap", type=float, help = "gap between lines (specified in nib widths)")
    parser.add_option("--top-margin", dest = "top_margin", default = 2, type = int,
                      help = "Top margin (specified in nib widths). Default is 2")
    parser.add_option("-n", "--rulings", dest = "rulings", default = 10, type=int,
                      help = "How many rulings to draw. Default is 10")
    parser.add_option("-a", "--angle", dest = "angles", type = "string",
                      help = "Comma separated list of angles (in degrees) for which to draw lines on the page (for pen angle, serifs etc.)")
    parser.add_option("-d", "--distance", dest = "distance", type = int,
                      help = "Distance (in mm) between angle guides")
    parser.add_option("-t", "--title", dest = "title", type = "string",
                      help = "A title for this ruling (usually the font name)")
    parser.add_option("-r", "--radial", dest = 'radial', action="store_true", default = False,
                      help = "Draw circles instead of straight lines")
    parser.add_option("-s", "--pagesize", dest = 'pagesize', default = "A4",
                      help = "Size of sheet")

    opts,args =  parser.parse_args(args)
    if len(args) != 2:
        parser.error("The output filename is required")
    return (opts,args)

if __name__ == "__main__":
    import sys
    opts = parse_options(sys.argv)
    main(*opts)

    
