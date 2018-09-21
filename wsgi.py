from flask import Flask, render_template
import random
application = Flask(__name__)

@application.route("/")
def hello():
    return render_template('home.html')

@application.route("/array")
def arrayTest():
    things = ["1","2","3","4","5","6","7"]
    placeHolder = random.randint(0,len(things)-1);
    return things[placeHolder]

if __name__ == "__main__":
    application.run()
