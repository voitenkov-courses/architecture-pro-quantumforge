from telegram import Update
from telegram.ext import ContextTypes
from bot_utils import (
    get_main_menu_keyboard, get_cancel_keyboard
)
from bot_config import (
    LANGUAGES, MAIN_MENU, ASK_QUESTION
)
import ragbot_cli2

# Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['lang'] = 'en'
    lang = context.user_data['lang']
    
    await update.message.reply_text(
        text=LANGUAGES[lang]['welcome'],
        parse_mode="HTML",
        reply_markup=get_main_menu_keyboard(lang),
        disable_web_page_preview=True
    )
    return MAIN_MENU

async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get('lang', 'en')
    text = update.message.text
    
    valid_commands = [
        LANGUAGES[lang]['ask_btn'],
        LANGUAGES[lang]['cancel']
    ]
    
    if text not in valid_commands:
        await update.message.reply_text(
            LANGUAGES[lang]['invalid_input'],
            reply_markup=get_main_menu_keyboard(lang)
        )
        return MAIN_MENU
    
    if text == LANGUAGES[lang]['ask_btn']:

        return ASK_QUESTION

    return MAIN_MENU

async def handle_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get('lang', 'en')
    question = update.message.text

    if question == LANGUAGES[lang]['cancel']:
        await update.message.reply_text(
            LANGUAGES[lang].get('canceled', 'Canceled'),
            reply_markup=get_main_menu_keyboard(lang)
        )
        return MAIN_MENU
    
    await update.message.reply_text(LANGUAGES[lang]['processing'])
    
    try:
        log_data = ragbot_cli2.new_log_data(question)
        log_data = ragbot_cli2.rag_chain(question, log_data)
        response = log_data["answer"]
        
        await update.message.reply_text(
            response,
            parse_mode="Markdown"
        )
        
        await update.message.reply_text(
            LANGUAGES[lang]['after_answer'],
            reply_markup=get_main_menu_keyboard(lang)
        )
        
    except Exception as e:
        error_msg = f"❌ {LANGUAGES[lang].get('error', 'Error')}: {str(e)}"
        await update.message.reply_text(
            error_msg,
            reply_markup=get_main_menu_keyboard(lang)
        )
    
    return MAIN_MENU
