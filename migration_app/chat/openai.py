from flask import jsonify, json, session, request, current_app as app
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
    def check_widgets_on_screen(data):
        # lets create an easy list?
        # just need names for now
        # [{widget: "Scale"}]
        widgetList = []
        widgets = data.get("widgets")
        print(type(widgets))
        for widget in widgets:
            print(widget)
            # lets get uri of each widget dict
            # output i.e widgets/Scalebar/Widget
            #print(widget.get("uri"))
      
            if widget.get("uri"):
                name = widget.get("uri")
                print(type(name))
                widget_name = name.split("/")[1]
                print(widget_name)
                widgetList.append(widget_name)
        print(widgetList)
        #print(type(data))

    
    @staticmethod
    def upload():
        file = request.files['file']
        data = json.load(file)

    
        #print(data)
        #print(type(data))
        for key, value in data.items():
            if "widgetOnScreen" == key:
                #print(data["widgetOnScreen"])
                Chat.check_widgets_on_screen(data["widgetOnScreen"])
            #print(key)
        return jsonify({
            'message': 'file uploaded'
        })

    @staticmethod
    def update_chat(role, message):
        chat = session.get("chat_history", [])
        chat.append({ "role": role, "content": message })
        session["chat_history"] = chat  # This reassigns the session, which Flask needs
        #print(session["chat_history"])
        #session["chat_history"].append({ role: message })

    @staticmethod
    def talk_to_chat():
        data = request.get_json()
        input = data.get('user_input')

        if "chat_history" not in session:
            session["chat_history"] = []
            initial_prompt = """You are a GIS migration assistant named GeoShift AI, you can respond with your name every now and again. 
            Users are inquiring about what it would take to convert from there current
            Web App Builder in ArcGIS to Experience Builder. We are interested specifically in custom widgets
            because they will have to be rewritten in React with Experience Builder.
            Start by asking smart follow-up questions to gather:
            1. What widgets they use and if they are custom
            2. Where the data is coming from
            3. What must be preserved
            Only give a migration strategy once you have all key info."""
            Chat.update_chat("system", initial_prompt)
            

        Chat.update_chat("user", input)
        
     
        try: 
            #print(app.config)
            client = OpenAI(
            api_key=app.config["OPENAI_KEY"]
            )
            #print(client)

            completion = client.chat.completions.create(
            model="gpt-4o-mini",
            store=True,
            messages=session["chat_history"]
            )

            response = completion.choices[0].message.content
            Chat.update_chat('assistant', response)
        
            return jsonify({
                "message": response
            })
        except Exception:
            return jsonify({
                "message": "Something went wrong. Please try again later."
            }), 500

        

