from flask import Blueprint, render_template as view

main = Blueprint('main', __name__, static_folder='static', template_folder='templates')


@main.route('/')
def index():
    """
    Show an index template
    :return:
    """

    return view('user/home.html')
