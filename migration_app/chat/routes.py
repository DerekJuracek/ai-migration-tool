import os
from flask import render_template, request
from migration_app.chat import chat_bp as chat
from .openai import Chat

@chat.route('/', methods=['POST'])
def ask_chat():
    return Chat.talk_to_chat()

