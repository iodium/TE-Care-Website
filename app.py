from flask import Flask, render_template, request, flash, redirect, url_for, session


app = Flask(__name__)
app.secret_key = "key"

@app.route('/')
def home():
    pass

if __name__ == '__main__':
    app.run(debug=True)