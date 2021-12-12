import logging

from telegram import Update
from telegram.ext import CommandHandler, Updater
from telegram.ext.callbackcontext import CallbackContext
from todoist import TodoistAPI

from config import CREDENTIALS

logging.basicConfig(
    format="%(asctime)s - $(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


def initialize_todoist():
    return TodoistAPI(CREDENTIALS.get("TODOIST_TOKEN"))


def get_todoist_completed_tasks(client: TodoistAPI, **kwargs):
    tasks_list = client.completed.get_all(**kwargs).get("items")

    return tasks_list


def get_help() -> str:
    help_str = """
Select one of the following commands:
\t/authenticate {TODOIST_TOKEN}\t Authenticate to your Todoist account by specifying your Todoist API key.
    """

    return help_str


# Command handlers
def start(update: Update, context: CallbackContext) -> None:
    user_first_name = update.effective_chat.first_name
    start_msg = f"Hi {user_first_name}!\n"
    start_msg += get_help()
    update.message.reply_text(start_msg)


def help(update: Update, context: CallbackContext) -> None:
    help_str = get_help()
    update.message.reply_text(help_str)


def main() -> None:
    updater = Updater(CREDENTIALS.TELEGRAM_BOT_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))

    updater.start_polling()

    return updater

    # updater.idle()
