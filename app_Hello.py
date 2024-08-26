from flask import Flask
# from flask import render_template
app=Flask(__name__)

@app.route('/')
def index():
    return "Hello World! SP Good Friday Cool Cool"

if __name__=="__main__":
    app.run(debug=True,host='127.0.0.1') #0.0.0.0 => accessible to any device on the network
    
