from flask import Blueprint, render_template, redirect, request, session
from website.models import voice

auth = Blueprint('auth', __name__)

@auth.route('/home', methods=['GET', 'POST'])
def home():
    return render_template("home.html")

@auth.route('/dashboard', methods=['GET', 'POST'])
def dash1():
    error = None
    if request.method == 'POST':
        address = request.form.get('address')
        p_key= request.form.get('privatekey')
        voice(p_key,address)
    return render_template("dash.html",error=error)




