from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

client = MongoClient()
db = client.Donations
donations = db.donations

app = Flask(__name__)


# Mock donations
# donations = [
#     {'organization': 'Save the turtles', 'amount_usd': 400, 'donor': 'Joe Schmo'},
#     {'organization': 'Save the seagulls', 'amount_usd': 100, 'donor': 'Terry Hairy'}
# ]

# READ - http verb GET - see donations and forms for changes
    #INDEX - show all of the donations
@app.route('/')
def donations_index():
    '''Show all donations.'''
    return render_template('donations_index.html', donations=donations.find())

# READ - http verb GET - see donations and forms for changes
    # NEW - form to create a new donation
@app.route('/donations/new')
def donations_new():
    '''Create a new donation.'''
    return render_template('donations_new.html')

@app.route('/donations', methods=['POST'])
def donations_submit(): 
    '''Submit a new donation.'''
    donation = {
        'organization': request.form.get('organization'),
        'amount_usd': request.form.get('amount_usd'),
        'note': request.form.get('note')
    }
    donations.insert_one(donation)
    return redirect(url_for('donations_index'))

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