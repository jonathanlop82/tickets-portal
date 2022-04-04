from flask import Flask, render_template
import tickets

app = Flask(__name__)

@app.route('/')
def index():
    list_tickets_users, all_tickets = tickets.list_tickets()
    return render_template("index.html", tickets=list_tickets_users, all_tickets=all_tickets)



if __name__ == "__main__":
    app.run(debug=True, port=5010)