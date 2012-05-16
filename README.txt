Used to create calligraphic rulings for western calligraphy::

Usage: ruling.py [options] output_file

Options:
  -h, --help            show this help message and exit
  -w NIB_WIDTH, --nib-width=NIB_WIDTH
                        Width of the nib specified in millimeters. All other
                        measurements are multiples of this.
  -p PARTITIONS, --partitions=PARTITIONS
                        Comma separated list of partitions in each line
                        (specified in nib widths)
  -g GAP, --gap=GAP     gap between lines (specified in nib widths)
  --top-margin=TOP_MARGIN
                        Top margin (specified in nib widths). Default is 2
  -n RULINGS, --rulings=RULINGS
                        How many rulings to draw. Default is 10
  -a ANGLES, --angle=ANGLES
                        Comma separated list of angles (in degrees) for which
                        to draw lines on the page (for pen angle, serifs etc.)
  -t TITLE, --title=TITLE
                        A title for this ruling (usually the font name)
  -r, --radial          Draw circles instead of straight lines


Some more specifics at [http://nibrahim.net.in/2010/12/30/calligraphic_rulings.html](http://nibrahim.net.in/2010/12/30/calligraphic_rulings.html).
