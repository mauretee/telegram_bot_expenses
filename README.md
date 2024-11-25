# telegram_bot_expenses

# How to use the bot
Send the command `/start` to the bot to start using it after taht send the command /addMe to add yourself to the database.

```
  Pizza 20 bucks
```
If your user is in the database the bot will save the expense.

# Implementation
There are two service the Bot service to manage the bot and the Database service to manage the database. And the Connector Service to connect telegram with the bot.
For more information about the implementation check the README in the respective folders.


# Running the bot locally
Complete the OPENAI_API_KEY in makefile after that run the following command:
The current bot is running on: [https://t.me/mjldarwinbot](https://t.me/mjldarwinbot). You can change the bot changing the TELGRAM_TOKEN in the makefile.

```
make
```
