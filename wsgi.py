import os
from flask import Flask
from flask_debug import Debug
from migration_app.__init__ import create_app

app = create_app()

if __name__ == "main":
    Debug(app)
    app.run(port=3001, debug=True)
else:
    app.run(port=3001)



  