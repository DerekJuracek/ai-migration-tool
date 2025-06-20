import os
from flask import render_template, request, session
from migration_app.chat import chat_bp as chat
from .openai import Chat

@chat.route('/talk', methods=['POST'])
def ask_chat():
    return Chat.talk_to_chat()

@chat.route('/reset', methods=['POST'])
def clear_session():
   return Chat.reset()

