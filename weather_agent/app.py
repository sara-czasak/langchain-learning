from flask import Flask, render_template


app = Flask(__name__)

@app.route('/')
def index():
    return render_template("chat.html")


@app.route('/send', methods=['POST'])
def another():
    return "Pika bo"


app.run(debug=True)