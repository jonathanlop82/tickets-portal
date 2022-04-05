from flask import Flask, render_template
import tickets

app = Flask(__name__)

@app.route('/')
def index():
    list_tickets_users, all_tickets = tickets.list_tickets()
    tickets_delayed = tickets.get_tickets_delayed()
    return render_template("index.html", tickets=list_tickets_users, all_tickets=all_tickets, tickets_delayed=tickets_delayed)



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)