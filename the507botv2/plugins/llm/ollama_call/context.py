from . import env, model

class ContextManager:
    context_cache = {} # { model_name: { user_id: [{},{},{}...]}}
    max_context_num = 100 # 一个模型下一个用户最多存储的上下文数量

    def __init__(self):
        max_context_num = env.MAX_CONTEXT_NUM
        
    def get(self, user_id):
        model_name = model.cur_model.get_name()
        model_context_cache = self.context_cache.get(model_name)
        if model_context_cache is None:
            return []
        return  model_context_cache.get(user_id, [])

    def append(self, user_id, user_msg, model_msg):
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
        # 如果超出上限则删除旧消息
        context_length = len(self.context_cache[model_name][user_id])
        if  context_length > self.max_context_num:
            self.context_cache[model_name][user_id] = self.context_cache[model_name][user_id][context_length-self.max_context_num:]

contextManager = ContextManager()
