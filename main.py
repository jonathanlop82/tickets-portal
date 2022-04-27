from flask import Flask, render_template
import tickets

app = Flask(__name__)


@app.route("/")
def index():
    list_tickets_users, all_tickets = tickets.list_tickets()
    tickets_delayed_30, tickets_delayed_10 = tickets.get_tickets_delayed()
    tickets_detail_user = tickets.get_tickets_by_users()
    count_users = len(tickets_detail_user)
    tickets_formats = tickets.get_tickets_by_category(7)
    return render_template(
        "index.html",
        tickets=list_tickets_users,
        all_tickets=all_tickets,
        tickets_delayed_30=tickets_delayed_30,
        tickets_delayed_10=tickets_delayed_10,
        tickets_detail_user=tickets_detail_user,
        count_users=count_users,
        tickets_formats=tickets_formats
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
