import os
from flask import Flask
from flask_debug import Debug
from migration_app.__init__ import create_app

app = create_app()

if __name__ == "main":
    app.run(port=3001)
else:
    app.run(port=3001)



  