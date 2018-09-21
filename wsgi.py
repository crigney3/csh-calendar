from flask import Flask
application = Flask(__name__)

@application.route("/")
def hello():
    return "Hello!"

<html>
    <head>
        <title>Bet This wont work</title>
    </head>
    <body>
        <h1>Hello!</h1>
    </body>
</html>

if __name__ == "__main__":
    application.run()
