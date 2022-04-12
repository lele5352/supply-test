from config import env_configs, mysql_config

# env = 'test26'
env = 'test160'
# env = 'test25'
env_config = env_configs.get(env)
db_config = mysql_config.get(env)

user = {
    'username': 'xuhongwei@popicorns.com',
    'password': '123456'
}
