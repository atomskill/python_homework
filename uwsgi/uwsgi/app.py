from bottle import Bottle
app = Bottle()
@app.get('/')
def root():
    return "FUCK!!!"
