import peewee
import os
from datetime import datetime

DB_PATH =  os.path.join(os.path.dirname(os.path.abspath(__file__)), "sqlite.db")
DB = peewee.SqliteDatabase(DB_PATH)

class ContextTable(peewee.Model):
    id = peewee.AutoField()
    model_name = peewee.CharField(max_length=32, null=False)
    user_id = peewee.CharField(max_length=32, null=False)
    create_time = peewee.DateTimeField(default=datetime.now)
    role = peewee.CharField(max_length=32, null=False)
    content = peewee.CharField(null=False)
    
    class Meta:
        database = DB
        table_name = "context"
        indexes = ((("user_id", "model_name"), False),)

if DB.is_closed():
    DB.connect()
existed = ContextTable.table_exists()
DB.create_tables([ContextTable], safe=True)
if not existed:
    # 如果ContextTable不存在，新建表后还要建一条记录占位，否则ollama.context直接尝试读写会报错
    ContextTable.create(model_name="model", user_id="user", role="user", content="content")
DB.close()

if __name__ == "__main__":
    DB.connect()
    # ContextTable.create(model_name="model", user_id="user", role="user", content="content")
    # ContextTable.delete().execute()
    res = ContextTable.select()
    print(len(res))
    # for rec in res.dicts():
        # print(rec)
    DB.close()
    