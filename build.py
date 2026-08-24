#!/usr/bin/env python3
"""
CI/CD Demo Build Script
使用 Jinja2 渲染页面，内容固定，版本和时间动态
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from jinja2 import Template
import datetime
import time
import random

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>CI/CD Demo — Jenkins</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background: linear-gradient(135deg, #{{ color1 }} 0%, #{{ color2 }} 100%);
            color: white;
        }
        .card {
            text-align: center;
            background: rgba(255, 255, 255, 0.12);
            padding: 3rem 4rem;
            border-radius: 20px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
        }
        .icon { font-size: 5rem; margin-bottom: 1rem; }
        h1 { font-size: 2.5rem; margin-bottom: 0.5rem; font-weight: 700; }
        .subtitle { font-size: 1.1rem; opacity: 0.8; margin-bottom: 2rem; }
        .version {
            font-size: 0.95rem;
            opacity: 0.7;
            margin-top: 1.5rem;
            padding: 0.5rem 1.5rem;
            background: rgba(255,255,255,0.1);
            border-radius: 20px;
            display: inline-block;
        }
        .timestamp {
            font-size: 0.85rem;
            opacity: 0.5;
            margin-top: 0.5rem;
        }
    </style>
</head>
<body>
    <div class="card">
        <div class="icon">🔧</div>
        <h1>欢迎使用 Jenkins</h1>
        <p class="subtitle">CI/CD 自动构建与部署演示页面</p>
        <div class="version">版本: {{ version }}</div>
        <div class="timestamp">部署时间: {{ timestamp }}</div>
    </div>
</body>
</html>"""

def build():
    # 随机颜色
    colors = [
        ("667eea", "764ba2"), ("f093fb", "f5576c"), ("4facfe", "00f2fe"),
        ("43e97b", "38f9d7"), ("fa709a", "fee140"), ("a8edea", "feed6c"),
    ]
    color1, color2 = random.choice(colors)

    version = f"v1.0.{int(time.time()) % 1000}"
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    template = Template(HTML_TEMPLATE)
    html = template.render(color1=color1, color2=color2, version=version, timestamp=timestamp)

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ 构建成功！")
    print(f"   版本: {version}")
    print(f"   时间: {timestamp}")

if __name__ == "__main__":
    build()
