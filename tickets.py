import db
import peewee
from peewee import fn
from playhouse.reflection import generate_models
import MySQLdb
import datetime as dt
from datetime import timedelta


database = peewee.MySQLDatabase(
    db.DATABASE, host=db.HOST, port=db.PORT, user=db.USER, passwd=db.PASSWORD
)
models = generate_models(database)
globals().update(models)


def list_tickets():
    current_month = dt.date(dt.datetime.now().year, dt.datetime.now().month, 1)
    query_tickets_closed = (
        hesk_tickets.select(hesk_users.user, fn.count(hesk_tickets.id))
        .join(hesk_users, on=(hesk_tickets.owner == hesk_users.id))
        .where((hesk_tickets.status == 3) & (hesk_tickets.dt > current_month))
        .group_by(hesk_tickets.owner)
        .dicts()
    )

    total_tickets = (
        hesk_tickets.select(fn.COUNT(hesk_tickets.id).alias("count"))
        .where(hesk_tickets.status << [0, 1, 2])
        .dicts()
    )
    query = (
        hesk_tickets.select(
            hesk_users.user.alias("user"), fn.COUNT(hesk_tickets.id).alias("count")
        )
        .join(hesk_users, on=(hesk_tickets.owner == hesk_users.id))
        .where(hesk_tickets.status << [0, 1, 2])
        .group_by(hesk_tickets.owner)
        .dicts()
    )
    tickets_count = []
    for row in total_tickets:
        all_tickets = row["count"]
    for row in query:
        user_count = {}
        user, count = row.values()
        user_count["user"] = user
        user_count["count"] = count
        user_count["closed"] = 0
        for ticket_row in query_tickets_closed:
            if ticket_row["user"] == user:
                user_count["closed"] = ticket_row["id"]
        tickets_count.append(user_count)
    return tickets_count, all_tickets


def get_tickets_delayed():
    tickets_delayed_10 = 0
    tickets_delayed_30 = 0
    query = (
        hesk_tickets.select(hesk_tickets.id, hesk_tickets.dt)
        .where(hesk_tickets.status << [0, 1, 2])
        .dicts()
    )
    for row in query:
        ticket_date = dt.datetime(
            int(str(row["dt"])[:4]), int(str(row["dt"])[5:7]), int(str(row["dt"])[8:10])
        )
        today = dt.datetime.now()
        days = (today - ticket_date).days
        if days >= 30:
            tickets_delayed_30 += 1
        elif days >= 10:
            tickets_delayed_10 += 1
    return tickets_delayed_30, tickets_delayed_10

