const TelegramBot = require("node-telegram-bot-api");

// replace the value below with the Telegram token you receive from @BotFather
const token = process.env.TELEGRAM_TOKEN;
const botService = process.env.BOT_SERVICE;
// Create a bot that uses 'polling' to fetch new updates
const bot = new TelegramBot(token, { polling: true });

// Matches "/echo [whatever]"
bot.onText(/\/echo (.+)/, (msg, match) => {
  // 'msg' is the received Message from Telegram
  // 'match' is the result of executing the regexp above on the text content
  // of the message

  const chatId = msg.chat.id;
  const resp = match[1]; // the captured "whatever"

  // send back the matched "whatever" to the chat
  bot.sendMessage(chatId, resp);
});

bot.onText(/\/addMe/, async (msg) => {
  const chatId = msg.chat.id;
  try {
    const response = await fetch(`${botService}user/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        telegram_id: chatId,
      }),
    });
    if (response.status === 400) {
      bot.sendMessage(chatId, "You are already registered");
    }
    if (response.status == 201) {
      bot.sendMessage(chatId, "You have been registered successfully");
    }
  } catch (error) {
    console.error("Error:", error);
    bot.sendMessage(chatId, "There was an error processing your request.");
  }
});

// Listen for any kind of message. There are different kinds of messages.
bot.on("message", async (msg) => {
  const chatId = msg.chat.id;
  if (msg.text === "/echo" || msg.text === "/addMe") {
    return;
  }

  try {
    const response = await fetch(botService, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        telegram_id: msg.from.id,
        message: msg.text,
      }),
    });

    if (!response.ok) {
      throw new Error(`Response status: ${response.status}`);
    }

    const data = await response.json();

    // Send a message to the chat acknowledging receipt of their message
    bot.sendMessage(chatId, `${data["category"]} expenses added  ✅`);
  } catch (error) {
    console.error("Error:", error);
    bot.sendMessage(chatId, "There was an error processing your request.");
  }
});
