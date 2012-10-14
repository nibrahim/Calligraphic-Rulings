import StringIO

from ruling import main
from .revproxy import ReverseProxied

from flask import Flask, request, render_template, send_file, make_response

APPLICATION_ROOT="/rulings"


app = Flask(__name__)
app.wsgi_app = ReverseProxied(app.wsgi_app)
app.config.from_object(__name__)
app.config.debug = True


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/download")
def pdf():
    cfg = lambda :0 # Dummy object which can have attributes
    for i,typ in [('nib_width', float),
                  ('partitions', str),
                  ('gap',float),
                  ('top_margin',int),
                  ('angles', str),
                  ('title', str),
                  ('radial', bool),
                  ('rulings', int),
                  ('distance', int)]:
        print i, "   ", request.args.get(i,'')
        setattr(cfg, i, typ(request.args.get(i,'')))
    fname = request.args.get('title','rulings').replace(" ","_").lower() + ".pdf"
    s = StringIO.StringIO()
    main(cfg, [None, s])

    resp = make_response(s.getvalue())
    resp.headers['Content-Type'] = 'application/pdf'
    resp.headers['Content-Disposition'] = 'attachment; filename=%s'%fname
    return resp


