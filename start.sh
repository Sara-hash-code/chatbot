#!/bin/bash
gunicorn -w 4 -k gthread -b 0.0.0.0:10000 chatbot:app
