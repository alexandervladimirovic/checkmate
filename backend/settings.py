import environ
from argon2 import PasswordHasher


env = environ.Env()
env.read_env(".env")

# Setup for hashing and verify password
ph = PasswordHasher(
    time_cost=env.int("ARGON2_TIME_COST"),
    memory_cost=env.int("ARGON2_MEMORY_COST"),
    parallelism=env.int("ARGON2_PARALLELISM"),
    hash_len=env.int("ARGON2_HASH_LEN"),
    salt_len=env.int("ARGON2_SALT_LEN"),
)

LIFETIME_ACCESS_TOKEN_IN_MINUTE = env.int("LIFETIME_ACCESS_TOKEN")
LIFETIME_REFRESH_TOKEN_IN_DAYS = env.int("LIFETIME_REFRESH_TOKEN")
