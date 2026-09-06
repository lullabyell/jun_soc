from app.auth import hash_password


users = {
    "aidana": {
        "username": "aidana",
        "email": "aidana@example.com",
        "full_name": "Aidana",
        "hashed_password": "$argon2id$v=19$m=65536,t=3,p=4$AtCgmoaNNTH/4Jr0/ONrPg$0jNFoxL6s2qSdmUH3F43EYLmdlQozojwtuITL2KOwk8",
    }
}


def get_user(username: str):
    return users.get(username)