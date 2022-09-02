
MANAGER="manager"
GENERAL="general"

def is_manager(user_type:str)->bool:
    return bool(user_type==MANAGER)

def is_general(user_type:str)->bool:
    return bool(user_type==GENERAL)