from flask import Flask
from flask import render_template
app=Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")
@app.route('/unlock')
def unlock():
    return render_template("unlock.html")
@app.route('/lock')
def lock():
    return render_template("lock.html")

if __name__=="__main__":
    app.run(debug=True,host='0.0.0.0')
