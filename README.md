# telegram_bot_expenses

# A simple telegram bot to manage expenses.
The current version of the bot is running on Heroku and can be accessed by the link: [https://t.me/mjldarwinbot](https://t.me/mjldarwinbot)

# How to use the bot
Send the command `/start` to the bot to start using it. Then start sending messages to the bot with the following format:
```
  Pizza 20 bucks
```
If your user is in the database the bot will save the expense.

# Implementation
There are two service the Bot service to manage the bot and the Database service to manage the database. And the Connector Service to connect telegram with the bot.
For more information about the implementation check the README in the respective folders.
