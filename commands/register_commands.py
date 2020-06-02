from commands.privacy.main import delete_users_message_history
from commands.help.main import send_default_help

commands = {}

commands["privacy"] = delete_users_message_history
commands["help"] = send_default_help

# if len(args) > 1:
#     print("Iterating...")
#     for x in args:
#         print(x)