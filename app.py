from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    """Return homepage."""
    return render_template('home.html', msg='Contractor Project!')

if __name__ == '__main__':
    app.run(debug=True)


# Create an app that can track donations and impact for a user
# CREATE - http verb POST - create a new donation
# READ - http verb GET - see donations and forms for changes
    #INDEX - show all of the donations
    #SHOW - show a single donation
    #NEW - form to create a new donation
    #EDIT - form to update an existing donation
# UPDATE - http verb PUT PATCH - update a donation
# DESTROY - http verb DELETE - delete a donation