from flask import jsonify, json, session, request, current_app as app
from openai import OpenAI
import os 

class Chat:
    chat = []
    app_package = {}
    wab_exb_widget_map = {
    # ✅ Supported widgets (2D)
    "About": "Window",
    "Add Data": "Add Data",
    "Analysis": "Analysis",
    "Attribute Table": "Table",
    "Batch Attribute Editor": "Edit",
    "Basemap Gallery": "Basemap Gallery",
    "Bookmark": "Bookmark",
    "Business Analyst": "Business Analyst",
    "Chart": "Chart",
    "Controller": "Widget Controller",
    "Coordinates": "Coordinates",
    "Coordinate Conversion": "Coordinate Conversion",
    "Directions": "Directions",
    "Draw": "Draw",
    "Edit": "Edit",
    "Extent Navigate": "Map (Extent navigate tool)",
    "Filter": "Filter",
    "Full Screen": "Map (Fullscreen tool)",
    "GeoLookup": "Analysis",
    "Geoprocessing": "Analysis",
    "Group Filter": "Filter",
    "Home Button": "Map (Home tool)",
    "Incident Analysis": "Near Me",
    "Infographic": "Chart",
    "Info Summary": "Near Me",
    "Layer List": "Map Layers",
    "Legend": "Legend",
    "Measurement": "Measurement",
    "My Location": "My Location",
    "Near Me": "Near Me",
    "Network Trace": "Utility Network Trace",
    "Oblique Viewer": "Oriented Imagery",
    "Overview Map": "Map (Overview map tool)",
    "Print": "Print",
    "Query": "Query",
    "Scalebar": "Map (Scale bar tool)",
    "Screening": "Near Me",
    "Search": "Search",
    "Select": "Map (Select tool)",
    "Share": "Share",
    "Situational Awareness": "Near Me",
    "Smart Editor": "Edit",
    "Splash": "Window",
    "Suitability Modeler": "Suitability Modeler",
    "Summary": "Text",
    "Swipe": "Swipe",
    "Time Slider": "Timeline",
    "Visibility": "Analysis",
    "Zoom Slider": "Map (Zoom tool)",

    # 🧭 Supported widgets (3D)
    "Basemap Gallery (3D)": "Map (Basemap tool)",
    "Compass": "Map",
    "Daylight": "3D Toolbox",
    "Map-centric Slide": "Bookmark",
    "Navigate": "Map (Navigation tool)",

    # ⚠️ Not supported directly — migration paths
    "Cost Analysis": "Configure forms in Map Viewer",
    "Data Aggregation": "Append data to feature layer",
    "Distance and Direction": "Custom development required",
    "District Lookup": "Use Instant Apps Zone Lookup",
    "Emergency Response Guide": "Custom development required",
    "Grid Overlay": "Custom development required",
    "Gridded Reference Graphic": "Custom development required",
    "Image Measurement": "Custom development required",
    "Parcel Drafter": "Planned Editing product",
    "Public Notification": "Use Instant Apps Public Notification",
    "Related Table Charts": "Use Arcade in pop-ups",
    "Reviewer Dashboard": "Deprecated",
    "Stream": "Custom development required",
    "Threat Analysis": "Custom development required",
    "3DFx": "Use Scene Viewer 3D rendering capability",
}


    @staticmethod
    def reset():
        session.clear()
        return jsonify({
            "response": "Session has been cleared."
        })
    
    @staticmethod
    def get_map(data):
        # get map id if there
        #print(data)
        mapId = data.get("itemId")
        if mapId == None or mapId == '':
            mapId = 'none'
        else:
            mapId = data.get("itemId")
        return mapId
       # Done ✅
    
    @staticmethod
    def get_theme(data):
        theme = ''
        if data.get("name"):
            theme = data.get("name")
        return theme
        # Done ✅
    
    @staticmethod
    def check_widgets_optional(data):
        optional_widget_list = []
        widgets = data.get("widgets")
        for widget in widgets:
            if widget.get("uri"):
                optional_widget = widget["uri"].split("/")[1]
                optional_widget_list.append(optional_widget)
        return optional_widget_list
        # Done ✅
        
    
    @staticmethod
    def check_widgets_on_screen(data):
        widgetList = []
        widgets = data.get("widgets")
        for widget in widgets:
            if widget.get("uri"):
                name = widget.get("uri")
                widget_name = name.split("/")[1]
                widgetList.append(widget_name)
        return widgetList
        # done ✅

    


    @staticmethod
    def update_chat(role, message):
        chat = Chat.chat
        chat.append({ "role": role, "content": message })

    @staticmethod
    def upload(data):
        #print(type(data))
        
        app_package = {}
        try :
            for key, value in data.items():
                if "widgetOnScreen" == key:
                    app_package["widgets"] = Chat.check_widgets_on_screen(data["widgetOnScreen"])
                if "widgetPool" == key:
                    app_package["other_widget"] = Chat.check_widgets_optional(data["widgetPool"])
                if "theme" == key:
                    app_package["theme"] = Chat.get_theme(data["theme"])
                if "map" == key:
                    app_package["map"] = Chat.get_map(data["map"])
            #Chat.talk_to_chat(app_package)
            # need to return output from talk_to_chat
            print(app_package)
            return app_package
            
        except Exception:
            return 'error'

    @staticmethod
    def talk_to_chat():
        initial_prompt = """"""
        input = ""
        input = request.form.get('user_input')
        file = request.files.get('file')
        data = {}

        if file and file != "":
             data = json.load(file)
      
        # data = json.load(file)
        uploaded_file_dict = {}

        file.seek(0)  

        if data:
           uploaded_file_dict = Chat.upload(data)
           
        if len(Chat.chat) == 0:
            initial_prompt = """You are a GIS migration assistant named GeoShift AI, you can respond with your name every now and again. 
            Users are inquiring about what it would take to convert from there current
            Web App Builder in ArcGIS to Experience Builder. if a user uploads a config.json initially and it matches of what is expected in web app builder than create their migration plan. Ask any follow up questions if needed.
            Only give a migration strategy once you have all key info. We are interested specifically in custom widgets
            because they will have to be rewritten in React with Experience Builder.
            Start by asking smart follow-up questions to gather:
            1. What widgets they use and if they are custom
            2. Do they have a map the app is using
            3. Do the widgets have an adjacent widget they can use in experience builder for the web app builder widget.
            It is recommended that they upload a config.json so that we can read it and compare with ESRI's latest docs to create an accurate
            migration plan.

            """

        if uploaded_file_dict:
            initial_prompt += f"""heres there uploaded config.json file from the user, please just create their migration plan and only ask follow up questions if you think it is relevant.
            {str(uploaded_file_dict)}
            please compare this with {Chat.wab_exb_widget_map} and see how their widgets compare
            to experience builder. If they aren't there then they are custom and we need to recommend a rewrite.
            If map id is empty, don't worry about it for now, but let them know.
            Also, you should be able to find any custom widgets from the config.json file. if 
            you don't see any. just ask the follow up question, 'I didn't see any custom widgets,
            is that correct?' """
            Chat.update_chat("system", initial_prompt)
            
        if len(input) > 0:
            Chat.update_chat("user", input)

        try: 
            client = OpenAI(
            api_key=app.config["OPENAI_KEY"]
            )
            completion = client.chat.completions.create(
            model="gpt-4o-mini",
            store=True,
            messages=Chat.chat
            )

            response = completion.choices[0].message.content
            Chat.update_chat('assistant', response)
           
            return jsonify({
                    "message": response
                })
        except Exception as e:
            return jsonify({
                "message": e
            }), 500
        



        

