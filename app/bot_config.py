import sqlite3
import logging
from dotenv import load_dotenv

# Initialize logging
logging.basicConfig(
    level=logging.INFO,
    filename="../logs/ragbot_log.log",
    filemode="a",
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Language settings
LANGUAGES = {
    'en': {
        'welcome': """<b>- Welcome to RAG Bot!</b>

This bot uses RAG (Retrieval-Augmented Generation) to answer questions based on your documents.
""",
        'ask_btn': "Ask question",
        'processing': "🔍 Searching for answer in the article...",
        'after_answer': "💡 You can ask another question or choose another option below",
        'cancel': "Cancel",
        'error': "❌ Error occurred",
        'invalid_input': "⚠️ Please use the buttons below to interact with me",
    },
    'ru': {
        'welcome': """<b>— Добро пожаловать в RAG Bot!</b>

Этот бот использует RAG (Retrieval-Augmented Generation — генерация дополненной реальности) для ответов на вопросы на основе ваших документов.
""",
        'ask_btn': "Задать вопрос",
        'processing': "🔍 Ищу ответ в статье...",
        'after_answer': "💡 Вы можете задать другой вопрос или выбрать другую опцию ниже",
        'cancel': "Отмена",
        'error': "❌ Произошла ошибка",
        'invalid_input': "⚠️ Пожалуйста, используйте кнопки ниже для взаимодействия",
    }
}

# Conversation states
(MAIN_MENU, ASK_QUESTION) = range(2)
