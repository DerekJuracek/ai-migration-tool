from flask import jsonify, session, request, current_app as app
from openai import OpenAI
import os 

class Chat:

    @staticmethod
    def reset():
        session.clear()
        return jsonify({
            "response": "Session has been cleared."
        })

    @staticmethod
    def update_chat(role, message):
        chat = session.get("chat_history", [])
        chat.append({ "role": role, "content": message })
        session["chat_history"] = chat  # This reassigns the session, which Flask needs
        print(session["chat_history"])
        #session["chat_history"].append({ role: message })

    @staticmethod
    def talk_to_chat():
        data = request.get_json()
        input = data.get('user_input')

        if "chat_history" not in session:
            session["chat_history"] = []
            initial_prompt = """You are a GIS migration assistant. 
            Users are inquiring about what it would take to convert from there current
            Web App Builder in ArcGIS to Experience Builder. We are interested specifically in custom widgets
            because they will have to be rewritten in React with Experience Builder.
            Start by asking smart follow-up questions to gather:
            1. What widgets they use and if they are custom
            2. Who the users are
            3. What must be preserved
            Only give a migration strategy once you have all key info."""
            Chat.update_chat("system", initial_prompt)
            

        Chat.update_chat("user", input)
        
     
        try: 
            print(app.config)
            client = OpenAI(
            api_key=app.config["OPENAI_KEY"]
            )
            print(client)

            completion = client.chat.completions.create(
            model="gpt-4o-mini",
            store=True,
            messages=session["chat_history"]
            )
            # return the chats response

            
            response = completion.choices[0].message.content
            Chat.update_chat('assistant', response)
        
            #print(session["chat_history"])
            #print(response)
            return jsonify({
                "response": response
            })
        except Exception:
            return jsonify({
                "response": "Something went wrong. Please try again later."
            }), 500

        

