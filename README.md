
# ringcentral-at-all-bot

![ ](screenshots/at-all-bot-min.png)

Add @all function to glip chatgroup with this bot. This is [@linjunpop](https://github.com/linjunpop)'s idea, posted at [Good ideas for new bots](https://github.com/ringcentral/ringcentral-chatbot-js/issues/8)

![ ](screenshots/ss.png)

## Prerequisites$

- Python3.6+ and Pip3
- Create the bot App: Login to [developer.ringcentral.com](https://developer.ringcentral.com) and create an `public` `Server/Bot` app with permissions: `ReadAccounts, Edit Extensions, WebhookSubscriptions, Glip`(or more as you may need)

## Development & Quick start

```bash

# init
bin/init
source ./venv/bin/activate

# run ngrok proxy
# since bot need https server,
# so we need a https proxy for ringcentral to visit our local server
./bin/proxy
# will show:
# Forwarding https://xxxxx.ngrok.io -> localhost:9890

# create env file
# .env already created from .sample.env
# just edit .env, set proper setting,
RINGCENTRAL_BOT_SERVER=https://xxxxx.ngrok.io

## for bots auth required, get them from your ringcentral app page
RINGCENTRAL_BOT_CLIENT_ID=
RINGCENTRAL_BOT_CLIENT_SECRET=

# and goto your ringcentral app setting page, set OAuth Redirect URI to https://https://xxxxx.ngrok.io/bot-oauth

# run local dev server
./bin/start
```

## Test bot

- Goto your ringcentral app's bot section, click 'Add to glip'
- Login to [https://glip-app.devtest.ringcentral.com](https://glip-app.devtest.ringcentral.com), find the bot by searching its name. Talk to the bot.
- Edit config.py to change bot bahavior and test in [https://glip-app.devtest.ringcentral.com](https://glip-app.devtest.ringcentral.com)

## Create your own bot logic

- You can edit/add method in `config.py` you need to use, write your own bot logic, restart the app, check it in [https://glip-app.devtest.ringcentral.com](https://glip-app.devtest.ringcentral.com).
- You can read all configs available from [all-config.py](all-config.py)

And we have examples bots you can check out as examples:

- [date-time-chatbot](https://github.com/zxdong262/ringcentral-date-time-chatbot) : Simple ringcentral chatbot which can tell time/date.
- [assistant-bot](https://github.com/zxdong262/ringcentral-assistant-bot) : Simple assistant Glip bot to show user/company information, this bot will show you how to access user data.
- [survey-bot](https://github.com/zxdong262/ringcentral-survey-bot) : Example survey bot, this bot will show you how to create/use custom database wrapper.

## Advanced topics

- [Deploy to AWS Lambda](https://github.com/zxdong262/ringcentral-chatbot-python/blob/master/docs/deploy-to-aws-lambda.md)
- [Use or write extensions](https://github.com/zxdong262/ringcentral-chatbot-python/blob/master/docs/extensions.md)

## License

MIT