
import sys
from PIL import Image
import argparse
import webbrowser

parser = argparse.ArgumentParser(description='Image -> Ascii Art')
parser.add_argument('-f','--filename', default=None,
    help='file to convert')
parser.add_argument('-l','--maxlength', default=100.0, type=float,
    help='Maximum length')
parser.add_argument('-c','--color', action='store_true',
    help='Color')
parser.add_argument('-s','--fontsize', default=7, type=int,
    help='file to convert')
parser.add_argument('-o','--output', default='output.html',
    help='file to output')
parser.add_argument('-b','--browser', action='store_true',
    help='open browser to view upon execution')
args = vars(parser.parse_args())
    
imgname = args['filename']
maxLen = args['maxlength']
clr = args['color']
fontSize = args['fontsize']



try:
    img = Image.open(imgname)
except IOError:
    exit("File not found: " + imgname)

# resize to: the max of the img is maxLen

width, height = img.size
rate = maxLen / max(width, height)
width = int(rate * width)  # cast to int
height = int(rate * height)
img = img.resize((width, height))

# img = img.convert('L')

# get pixels
pixel = img.load()

# grayscale
color = "MNHQ$OC?7>!:-;. "

string = ""

for h in xrange(height):  # first go through the height,  otherwise will roate
    for w in xrange(width):
        rgb = pixel[w, h]
        if clr:
            string += "<span style=\"color:rgb" + str(rgb) + \
                ";\"></span>"
        else:
            string += color[int(sum(rgb) / 3.0 / 256.0 * 16)]
    string += "\n"

# wrappe with html

template = """<!DOCTYPE HTML>
<html>
<head>
  <meta http-equiv="content-type" content="text/html; charset=utf-8" />
  <style type="text/css" media="all">
    pre {
      white-space: pre-wrap;       /* css-3 */
      white-space: -moz-pre-wrap;  /* Mozilla, since 1999 */
      white-space: -pre-wrap;      /* Opera 4-6 */
      white-space: -o-pre-wrap;    /* Opera 7 */
      word-wrap: break-word;       /* Internet Explorer 5.5+ */
      font-family: 'Inconsolata', 'Consolas'!important;
      line-height: 1.0;
      font-size: %dpx;
    }
  </style>
</head>
<body>
  <pre>%s</pre>
</body>
</html>
"""

html = template % (fontSize, string)
with open(args['output'], 'w') as f:
    f.write(html)

if args['browser']:
    webbrowser.open(args['output'])
