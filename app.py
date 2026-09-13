import json
import re
from pathlib import Path

from flask import Flask, render_template, request, flash, redirect, url_for, session


app = Flask(__name__)
app.secret_key = "key"

# Folder holding one JSON file of text per page (content/home.json, etc.)
CONTENT_DIR = Path(__file__).parent / "content"

# Sensitive names in the JSON are wrapped like [[this]] so they're easy to
# find with a search. The brackets are stripped before rendering, so the
# site shows just the text inside them.
FLAG = re.compile(r"\[\[(.*?)\]\]")


def strip_flags(value):
    """Remove [[ ]] markers from every string, recursing into lists and dicts."""
    if isinstance(value, str):
        return FLAG.sub(r"\1", value)
    if isinstance(value, list):
        return [strip_flags(v) for v in value]
    if isinstance(value, dict):
        return {k: strip_flags(v) for k, v in value.items()}
    return value


def load_content(page):
    """Read content/<page>.json, strip [[ ]] flags, return a dict.

    Read on every request (not cached) so edits to the JSON show up on
    browser reload without restarting Flask.
    """
    with open(CONTENT_DIR / f"{page}.json", encoding="utf-8") as f:
        return strip_flags(json.load(f))


@app.route('/')
def home():
    return render_template("home.html", c=load_content("home"))

@app.route('/about')
def about():
    return render_template("about.html", c=load_content("about"))

@app.route('/impact')
def impact():
    return render_template("impact.html", c=load_content("impact"))

@app.route('/calendar')
def calendar():
    return render_template("calendar.html")

if __name__ == '__main__':
    app.run(debug=True)
