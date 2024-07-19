from flask import Flask, request, render_template, render_template_string, redirect, url_for
import MySQLdb

app = Flask(__name__)

def get_db_connection():
    return MySQLdb.connect(
        host='localhost',
        user='root',
        password='6411', 
        database='ctf'
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            return render_template_string('''
                <script>alert("Email and password are required.");</script>
                <a href="/login">Go back</a>
            ''')

        connection = get_db_connection()
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE email=%s AND password=%s"
        try:
            cursor.execute(query, (email, password))
            user = cursor.fetchone()
            
        finally:
            connection.close()

        if user:
            return redirect(url_for('success'))
        else:
            return render_template_string('''
                <script>alert("Invalid credentials. Try again.");</script>
                <a href="/">Go back</a>
            ''')

    return render_template('login.html', hint="The secrets of the Royals family are often hidden in plain sight, yet their true meaning remains veiled.")

@app.route('/success')
def success():
    # Fetch encrypted flag from database to display in source code
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT flag FROM secrets WHERE id=1")
    encrypted_flag = cursor.fetchone()[0]
    connection.close()
    return render_template('success.html', hint="The Galactic Federation's encryption methods are rooted in ancient Rome. Perhaps a Caesar could help you decipher the truth.", encrypted_flag=encrypted_flag)

@app.route('/submit_flag', methods=['POST'])
def submit_flag():
    user_flag = request.form.get('flag')
    # Direct comparison to the expected decrypted flag (case-insensitive)
    if user_flag.lower() == "ctf{th1s_1s_my_s3cr3t_fl4g}":  
        return render_template_string('''
            <script>alert("Congratulations! You have captured the flag!");</script>
            <a href="/">Return to Home</a>
        ''') 
    else:
        return render_template_string('''
            <script>alert("Incorrect flag. Keep searching!");</script>
            <a href="/success">Go back</a>
        ''')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
