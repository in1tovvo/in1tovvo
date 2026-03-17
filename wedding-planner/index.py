#!/usr/bin/env python3
"""
Vercel 入口点
"""

from app import app as flask_app

# Vercel 需要这个变量名
app = flask_app