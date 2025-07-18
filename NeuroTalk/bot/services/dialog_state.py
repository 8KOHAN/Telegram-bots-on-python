dialog_history = {}

def add_to_history(user_id: int, role: str, content: str):
    if user_id not in dialog_history:
        dialog_history[user_id] = []
    dialog_history[user_id].append({"role": role, "content": content})
    if len(dialog_history[user_id]) > 10:
        dialog_history[user_id] = dialog_history[user_id][-10:]
