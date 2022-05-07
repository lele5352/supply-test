from config.env_prefix_config import env_prefix_configs
from config.mysql_config import mysql_config

# env:'test160'/'test25'/'test26'
env = 'test160'

env_prefix_config = env_prefix_configs.get(env)
db_config = mysql_config.get(env)

user = {
    'username': 'xuhongwei@popicorns.com',
    'password': 'hw123456'
}
