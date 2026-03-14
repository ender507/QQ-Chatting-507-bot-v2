from . import env, model
from ..dal import dal

class ContextManager:
    context_cache = {} # { model_name: { user_id: [{},{},{}...]}}
    max_context_num = 100 # 一个模型下一个用户最多存储的上下文数量

    def __init__(self, max_context_num=100):
        self.context_cache = {}
        self.max_context_num = max_context_num
        # 初始化时从数据库读历史上下文数据写入内存作为缓存
        if dal.DB.is_closed():
            dal.DB.connect()
        res = dal.ContextTable.select().order_by("id")
        dal.DB.close()
        for rec in res.dicts():
            if self.context_cache.get(rec["model_name"]) is None:
                self.context_cache[rec["model_name"]] = {}
            if self.context_cache[rec["model_name"]].get(rec["user_id"]) is None:
                self.context_cache[rec["model_name"]][rec["user_id"]] = []
            self.context_cache[rec["model_name"]][rec["user_id"]] += [{"role": rec["role"], "content": rec["content"]}]
        
    def get(self, user_id):
        model_name = model.cur_model.get_name()
        model_context_cache = self.context_cache.get(model_name)
        if model_context_cache is None:
            return []
        return  model_context_cache.get(user_id, [])

    def add(self, user_id, user_msg, model_msg):
        if dal.DB.is_closed():
            dal.DB.connect()
        # 把新消息加入存储
        model_name = model.cur_model.get_name()
        if self.context_cache.get(model_name) is None:
            self.context_cache[model_name] = {}
        if self.context_cache[model_name].get(user_id) is None:
            self.context_cache[model_name][user_id] = []
        self.context_cache[model_name][user_id] += [
            {"role": "user", "content": user_msg}, \
            {"role": "assistant", "content": model_msg} \
        ]
        dal.ContextTable.insert_many([
            {"model_name": model_name, "user_id": user_id, "role": "user", "content": user_msg},
            {"model_name": model_name, "user_id": user_id, "role": "assistant", "content": model_msg},
        ]).execute()
         # 如果超出上下文长度上限则删除旧消息
        context_length = len(self.context_cache[model_name][user_id])
        if context_length > self.max_context_num:
            delete_num = context_length - self.max_context_num
            self.context_cache[model_name][user_id] = self.context_cache[model_name][user_id][delete_num:]
            rec_to_delete = (dal.ContextTable.select(dal.ContextTable.id).where(
                dal.ContextTable.user_id == user_id,
                dal.ContextTable.model_name == model_name
                ).order_by(dal.ContextTable.id).limit(delete_num)
            )
            ids_to_delete = [row.id for row in rec_to_delete]
            dal.ContextTable.delete().where(dal.ContextTable.id.in_(ids_to_delete)).execute()
        dal.DB.close()

contextManager = ContextManager(env.MAX_CONTEXT_NUM)
