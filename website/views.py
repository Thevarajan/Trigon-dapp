from flask import Blueprint, render_template, redirect

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return redirect("/home")

@views.route('/dash')
def dash():
    return redirect("/dashboard")

@views.route('/main1')
def main1():
    return redirect("/main")

@views.route('/hello')
def hello():
    return redirect("/ai")