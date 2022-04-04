import db
import peewee
from peewee import fn
from playhouse.reflection import generate_models
import MySQLdb

database = peewee.MySQLDatabase(db.DATABASE, host=db.HOST, port=db.PORT, user=db.USER, passwd=db.PASSWORD)
models = generate_models(database)
globals().update(models)

def list_tickets():
    total_tickets = hesk_tickets.select(fn.COUNT(hesk_tickets.id).alias('count')).where(hesk_tickets.status << [0,2]).dicts()
    query = hesk_tickets.select(hesk_users.user.alias('user'), fn.COUNT(hesk_tickets.id).alias('count')).join(hesk_users, on=(hesk_tickets.owner == hesk_users.id)).where(hesk_tickets.status << [0,2]).group_by(hesk_tickets.owner).dicts()
    tickets_count = []
    for row in total_tickets:
        all_tickets = row["count"]
    for row in query:
        user_count = {}
        user, count = row.values()
        user_count["user"] = user
        user_count["count"] = count
        tickets_count.append(user_count)
    return tickets_count, all_tickets