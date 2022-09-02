
MANAGER=1
GENERAL=2

def is_manager(user_type:int)->bool:
    return bool(user_type==MANAGER)

def is_general(user_type:int)->bool:
    return bool(user_type==GENERAL)