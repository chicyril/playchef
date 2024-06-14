#!/usr/bin/env python3
from app import app

if __name__ == '__main__':
    host = app.config.get('HOST')
    port = app.config.get('PORT')
    app.run(host=host, port=port)
