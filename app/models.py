class Transaction:
    amount:int
    source:str
    tdate:str
    keywords:list[str]

    def __init__(self, a, s, t, kw):
        self.amount = a
        self.source = s
        self.tdate = t
        self.keywords = kw

    def __str__(self):
        # return f"INR {self.amount} from {self.source} on {self.tdate} with {self.keywords}"
        return f"{self.tdate}: INR {self.amount}"
