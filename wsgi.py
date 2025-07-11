import os
from flask import Flask
from migration_app.__init__ import create_app

app = create_app()

if __name__ == "__main__":
    app.run(port=3001)



  