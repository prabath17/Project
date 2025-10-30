from flask import Flask, render_template, request, redirect, session, flash
from supabase import create_client, Client
from datetime import datetime


app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Replace with your actual Supabase project credentials
SUPABASE_URL = "https://lvgvmiybckdkyusfpabk.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imx2Z3ZtaXliY2tka3l1c2ZwYWJrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDY3MDM5NjQsImV4cCI6MjA2MjI3OTk2NH0.aN5H5cP2ketyWO5WA74X8lf49OdbC_RtBZ_qfOT7GW0"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/admin/signup', methods=['GET', 'POST'])
def admin_signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        gym_name = request.form['gym_name']
        gym_address = request.form['gym_address']

        existing = supabase.table('admin_users').select("*").eq("username", username).execute()
        if existing.data:
            flash("Username already exists", "error")
        else:
            supabase.table('admin_users').insert({
                'username': username,
                'password': password,
                'gym_name': gym_name,
                'gym_address': gym_address
            }).execute()
            flash("Signup successful! Please log in.", "success")
            return redirect('/admin/login')

    return render_template('admin/signup.html')


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check for superadmin credentials
        if username == 'superadmin' and password == 'superadmin@123':
            session['superadmin_logged_in'] = True
            return redirect('/superadmin/dashboard')

        result = supabase.table('admin_users').select("*").eq("username", username).eq("password", password).execute()

        if result.data:
            session['admin_logged_in'] = True
            session['admin_username'] = username
            return redirect('/admin/dashboard')
        else:
            flash("Check your username and password", "error")

    return render_template('admin/login.html')





@app.route('/admin/logout')
def admin_logout():
    session.clear()
    return redirect('/')


@app.route('/superadmin/dashboard')
def superadmin_dashboard():
    if not session.get('superadmin_logged_in'):
        return redirect('/admin/login')

    admins = supabase.table('admin_users').select('*').execute()
    members = supabase.table('members').select('*').execute()
    return render_template('superadmin/dashboard.html', admins=admins.data, members=members.data)

# Show the add member page
@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect('/admin/login')

    members = supabase.table('members').select('*').execute().data

    total = len(members)
    today = datetime.today().date()
    active = sum(1 for m in members if m.get("subscription_end") and datetime.strptime(m["subscription_end"], "%Y-%m-%d").date() >= today)
    expired = total - active

    return render_template('admin/dashboard.html', members=members, total_members=total, active_members=active, expired_members=expired)


@app.route('/admin/add-member', methods=['GET', 'POST'])
def add_member():
    if not session.get('admin_logged_in'):
        return redirect('/admin/login')

    if request.method == 'POST':
        supabase.table('members').insert({
            'name': request.form['name'],
            'age': request.form['age'],
            'contact': request.form['contact'],
            'membership_plan': request.form['membership_plan'],
            'diet_plan': request.form['diet_plan'],
            'workout_plan': request.form['workout_plan'],
            'subscription_start': request.form['subscription_start'],
            'subscription_end': request.form['subscription_end']
        }).execute()
        return redirect('/admin/dashboard')

    return render_template('admin/add_member.html')


@app.route('/admin/edit-member/<int:member_id>', methods=['GET', 'POST'])
def edit_member(member_id):
    if request.method == 'GET':
        # Fetch existing member data
        member_data = supabase.table("members").select("*").eq("id", member_id).single().execute()
        member = member_data.data
        return render_template('edit_member.html', member=member)

    elif request.method == 'POST':
        # Update the member with new data
        updated_data = {
            "name": request.form["name"],
            "age": request.form["age"],
            "contact": request.form["contact"],
            "membership_plan": request.form["membership_plan"],
            "diet_plan": request.form["diet_plan"],
            "workout_plan": request.form["workout_plan"],
            "subscription_start": request.form["subscription_start"],
            "subscription_end": request.form["subscription_end"]
        }

        supabase.table("members").update(updated_data).eq("id", member_id).execute()
        return redirect('/admin/dashboard')

@app.route('/admin/delete-member/<int:member_id>', methods=['GET'])
def delete_member(member_id):
    supabase.table("members").delete().eq("id", member_id).execute()
    return redirect('/admin/dashboard')





if __name__ == '__main__':
    app.run(debug=True)
