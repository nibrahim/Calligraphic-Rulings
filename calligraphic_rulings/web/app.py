import StringIO

from ruling import main

from flask import Flask, request, render_template, send_file, make_response


app = Flask(__name__)
app.config.from_object(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template('index.html')
    elif request.method == "POST":
        cfg = lambda :0 # Dummy object which can have attributes
        for i,typ in [('nib_width', float),
                      ('partitions', str),
                      ('gap',float),
                      ('top_margin',int),
                      ('angles', str),
                      ('title', str),
                      ('radial', bool),
                      ('rulings', int)]:
            setattr(cfg, i, typ(request.form.get(i,'')))
        fname = request.form.get('title','rulings').replace(" ","_").lower() + ".pdf"
        s = StringIO.StringIO()
        main(cfg, [None, s])

        resp = make_response(s.getvalue())
        resp.headers['Content-Type'] = 'application/pdf'
        resp.headers['Content-Disposition'] = 'attachment; filename=%s'%fname
        return resp
    
                    
