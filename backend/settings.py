import environ


env = environ.Env()
env.read_env(".env")


ARGON2_TIME_COST = env.int("ARGON2_TIME_COST")
ARGON2_MEMORY_COST = env.int("ARGON2_MEMORY_COST")
ARGON2_PARALLELISM = env.int("ARGON2_PARALLELISM")
ARGON2_HASH_LEN = env.int("ARGON2_HASH_LEN")
ARGON2_SALT_LEN = env.int("ARGON2_SALT_LEN")
