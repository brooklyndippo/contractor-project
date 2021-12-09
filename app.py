from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

# uncomment this when running on heroku
uri = os.environ.get('mongodb://localhost:27017/Charity-Labs', 'MONGODB_URI')
client = MongoClient(uri)
db = client.get_default_database()
# or
# db = client.get_database('CharityLabs')

#comment this out when running on heroku
# client = MongoClient()

db = client.Donations
donations = db.donations
users = db.users

app = Flask(__name__)

#HOME PAGE/Sign Up
@app.route('/')
def home():
    '''Show home page'''
    return render_template('home.html')




# ADMIN VIEW
# INDEX - show all of the users
@app.route('/admin')
def users_index():
    '''Show all users.'''
    return render_template('users_index.html', users=users.find())




# ======== USER RESOURCE ======== USER RESOURCE ======== USER RESOURCE ======== 

#NEW USER form to create a new user
@app.route('/users/new')
def users_new():
    '''Create a new user'''
    user={}
    return render_template('users_new.html', user=user, title='New User')

# CREATE USER- http verb POST - create a new donation
@app.route('/users', methods=['POST'])
def users_submit(): 
    '''Submit a new user.'''
    user = {
        'firstName': request.form.get('firstName'),
        'lastName': request.form.get('lastName'),
        'income': int(request.form.get('income')),
        'impact': int(request.form.get('impact')),
    }
    users.insert_one(user)
    return render_template('users_dashboard.html', user=user, title='New User')

# SHOW A SINGLE USER
@app.route('/users/<user_id>')
def users_show(user_id):
    '''Show a single user.'''
    print(user_id)
    user = users.find_one({'_id': ObjectId(user_id)})
    user_donations = donations.find({'user_id': ObjectId(user_id)})
    return render_template('users_dashboard.html', user=user, donations=user_donations)

# EDIT A USERS SETTINGS (get a form)
@app.route('/users/<user_id>/edit')
def users_edit(user_id):
    '''Show the edit form for a donation'''
    user = users.find_one({'_id': ObjectId(user_id)})
    return render_template('users_edit.html', user=user, title='Edit User')


# UPDATE A USERS SETTINGS
@app.route('/users/<user_id>', methods=['POST'])
def users_update(user_id):
    """Submit an updated donation."""
    # create our updated donation
    updated_user = {
        'firstName': request.form.get('firstName'),
        'lastName': request.form.get('lastName'),
        'income': request.form.get('income'),
        'impact': request.form.get('impact')
    }
    # set the former donation to the new one we just updated/edited
    users.update_one(
        {'_id': ObjectId(user_id)},
        {'$set': updated_user})
    # take us back to the donation's show page
    return redirect(url_for('users_show', user_id=user_id))

# DESTROY A USER
@app.route('/users/<user_id>/delete', methods=['POST'])
def users_delete(user_id):
    """Delete one donation."""
    users.delete_one({'_id': ObjectId(user_id)})
    return redirect(url_for('users_index'))


# ======== DONATION RESOURCE ======== DONATION RESOURCE ======== DONATION RESOURCE ======== 

# CREATE A DONATION FOR A USER
@app.route('/users/donations', methods=['POST'])
def donations_new():
    '''Submit a new donation.'''
    donation = {
        'user_id': ObjectId(request.form.get('user_id')),
        'organization': request.form.get('organization'),
        'cause': request.form.get('cause'),
        'amount_usd': request.form.get('amount_usd'),
        'note': request.form.get('note')
    }
    donations.insert_one(donation)
    print (donation['user_id'])
    print(donation['note'])
    user_id=request.form.get('user_id')
    return redirect(url_for('users_show', user_id=user_id))

# ======== DONATION RESOURCE ======== DONATION RESOURCE ======== DONATION RESOURCE ======== 

# READ - http verb GET - see donations and forms for changes
    #INDEX - show all of the donations
# @app.route('/')
# def donations_index():
#     '''Show all donations.'''
#     return render_template('donations_index.html', donations=donations.find())


# # READ - http verb GET - see donations and forms for changes
#     # NEW - form to create a new donation
# @app.route('/donations/new')
# def donations_new():
#     '''Create a new donation.'''
#     donation = {}
#     return render_template('donations_new.html', donation=donation, title='New Donation')


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






# # READ - http verb GET - see donations and forms for changes
#     # NEW - form to create a new donation
# @app.route('/donations/new')
# def donations_new():
#     '''Create a new donation.'''
#     donation = {}
#     return render_template('donations_new.html', donation=donation, title='New Donation')


# # CREATE - http verb POST - create a new donation
# @app.route('/donations', methods=['POST'])
# def donations_submit(): 
#     '''Submit a new donation.'''
#     donation = {
#         'organization': request.form.get('organization'),
#         'amount_usd': request.form.get('amount_usd'),
#         'note': request.form.get('note')
#     }
#     donations.insert_one(donation)
#     return redirect(url_for('donations_index'))


# # READ - http verb GET - see donations and forms for changes
#     # SHOW - show a single donation
# @app.route('/donations/<donation_id>')
# def donations_show(donation_id):
#     '''Show a single donation'''
#     donation = donations.find_one({'_id': ObjectId(donation_id)})
#     return render_template('donations_show.html', donation=donation)



# # READ - http verb GET - see donations and forms for changes
#     #EDIT - form to update an existing donation
# @app.route('/donations/<donation_id>/edit')
# def donations_edit(donation_id):
#     '''Show the edit form for a donation'''
#     donation = donations.find_one({'_id': ObjectId(donation_id)})
#     return render_template('donations_edit.html', donation=donation, title='Edit Donation')



# # UPDATE - http verb PUT PATCH - update a donation
# @app.route('/donations/<donation_id>', methods=['POST'])
# def donations_update(donation_id):
#     """Submit an updated donation."""
#     # create our updated donation
#     updated_donation = {
#         'organization': request.form.get('organization'),
#         'amount_usd': request.form.get('amount_usd'),
#         'note': request.form.get('note')
#     }
#     # set the former donation to the new one we just updated/edited
#     donations.update_one(
#         {'_id': ObjectId(donation_id)},
#         {'$set': updated_donation})
#     # take us back to the donation's show page
#     return redirect(url_for('donations_show', donation_id=donation_id))

# # DESTROY - http verb DELETE - delete a donation
# @app.route('/donations/<donation_id>/delete', methods=['POST'])
# def donations_delete(donation_id):
#     """Delete one donation."""
#     donations.delete_one({'_id': ObjectId(donation_id)})
#     return redirect(url_for('donations_index'))




if __name__ == '__main__':
    app.run(debug=True)