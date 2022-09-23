from config.env_config import prefix_config, mysql_config

# 指定环境：'test160'/'test25'/'test26'
env = 'test160'

env_prefix_config = env_config.prefix_config.get(env)
db_config = env_config.mysql_config.get(env)

user = {
    'username': 'xuhongwei@popicorns.com',
    'password': 'hw123456'
}
