import datetime
from fastapi import FastAPI
from decimal import Decimal
from util import get_axis_transactions
app = FastAPI()

@app.get("/axis/get_transactions")
def get_axis_trasnactions(from_date:str, to_date:str):
    return get_axis_transactions(from_date, to_date)

@app.get("/axis/get_unbilled")
def get_axis_unbilled(as_of=None):
    
    today = None

    if as_of is None:
        today = datetime.date.today()
    else:
        today = datetime.datetime.strptime(as_of, "%Y-%m-%d").date()

    day = today.day
    from_date = None
    to_date = None
    if day >= 15:
        from_date = datetime.date(year=today.year, month=today.month, day=15)
        next_month =  1 if today.month == 12 else today.month + 1
        to_date = datetime.date(year=today.year, month=next_month, day=15)
    else:
        prev_month =  12 if today.month == 1 else today.month - 1
        from_date = datetime.date(year=today.year, month=prev_month, day=15)
        to_date = datetime.date(year=today.year, month=today.month, day=15)
    print(from_date, to_date)
    return sum(Decimal(x.amount) for x in get_axis_transactions(from_date, to_date))