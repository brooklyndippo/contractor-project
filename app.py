from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

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
    donation = {}
    return render_template('donations_new.html', donation=donation, title='New Donation')


# CREATE - http verb POST - create a new donation
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


# READ - http verb GET - see donations and forms for changes
    # SHOW - show a single donation
@app.route('/donations/<donation_id>')
def donations_show(donation_id):
    '''Show a single donation'''
    donation = donations.find_one({'_id': ObjectId(donation_id)})
    return render_template('donations_show.html', donation=donation)



# READ - http verb GET - see donations and forms for changes
    #EDIT - form to update an existing donation
@app.route('/donations/<donation_id>/edit')
def donations_edit(donation_id):
    '''Show the edit form for a donation'''
    donation = donations.find_one({'_id': ObjectId(donation_id)})
    return render_template('donations_edit.html', donation=donation, title='Edit Donation')



# UPDATE - http verb PUT PATCH - update a donation
@app.route('/donations/<donation_id>', methods=['POST'])
def donations_update(donation_id):
    """Submit an updated donation."""
    # create our updated donation
    updated_donation = {
        'organization': request.form.get('organization'),
        'amount_usd': request.form.get('amount_usd'),
        'note': request.form.get('note')
    }
    # set the former donation to the new one we just updated/edited
    donations.update_one(
        {'_id': ObjectId(donation_id)},
        {'$set': updated_donation})
    # take us back to the donation's show page
    return redirect(url_for('donations_show', donation_id=donation_id))

# DESTROY - http verb DELETE - delete a donation
@app.route('/donations/<donation_id>/delete', methods=['POST'])
def donations_delete(donation_id):
    """Delete one donation."""
    donations.delete_one({'_id': ObjectId(donation_id)})
    return redirect(url_for('donations_index'))

if __name__ == '__main__':
    app.run(debug=True)