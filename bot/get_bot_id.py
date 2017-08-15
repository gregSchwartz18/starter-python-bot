from slackclient import SlackClient

BOT_NAME = 'red_eye'
BOT_ID = 'U666TFZ29'
token = "xoxp-40267905093-40267773191-209471726528-526ed8f2ea10b5e8ca8b0cacc0fa72ca"
client_id = '40267905093.210943618326'
client_secret = '1d882041ded84a27db29f169e68ec4a1'


client = SlackClient(token)
print(client.api_call("api.test"))

client.api_call(
  "chat.postMessage",
  channel="#python",
  text="Hello from Python! :tada:"
)

if __name__ == '__main__':
    api_call = client.api_call('users.list')
    if api_call.get('ok'):
        users = api_call.get('members')
        for user in users:
            if 'name' in user and user.get('name') == BOT_NAME:
                print('Bot ID for {} is {}'.format(user['name'], user.get('id')))
            else:
                print('Couldn\'t find the bot named {}'.format(BOT_NAME))
    else:
        print('not ok')