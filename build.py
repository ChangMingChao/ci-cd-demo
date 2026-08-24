#!/usr/bin/env python3
"""
CI/CD Demo Build Script
使用 Jinja2 + Faker + emoji 生成演示页面
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from jinja2 import Template
from faker import Faker
import emoji
import random
import datetime
import time

fake = Faker('zh_CN')

# HTML 模板
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>CI/CD Demo</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background: linear-gradient(135deg, #{{ color1 }} 0%, #{{ color2 }} 100%);
            color: white;
            transition: all 0.5s ease;
        }
        .card {
            text-align: center;
            background: rgba(255, 255, 255, 0.15);
            padding: 3rem;
            border-radius: 20px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            max-width: 500px;
        }
        h1 { font-size: 2.5rem; margin: 0 0 1rem 0; }
        .version { font-size: 1.2rem; opacity: 0.9; margin-top: 1rem; }
        .timestamp { font-size: 0.9rem; opacity: 0.7; margin-top: 0.5rem; }
        .emoji-icon { font-size: 4rem; margin-bottom: 1rem; }
        .quote {
            margin-top: 1.5rem;
            padding: 1rem;
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
            font-style: italic;
        }
        .info { font-size: 0.85rem; opacity: 0.6; margin-top: 1.5rem; }
    </style>
</head>
<body>
    <div class="card">
        <div class="emoji-icon">{{ random_emoji }}</div>
        <h1>CI/CD 自动部署成功！</h1>
        <p>{{ random_sentence }}</p>
        <div class="quote">{{ quote }}</div>
        <div class="version">版本: {{ version }}</div>
        <div class="timestamp">部署时间: {{ timestamp }}</div>
        <div class="info">生成者: {{ generator }} | 城市: {{ city }}</div>
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

    # 使用 emoji 包
    emojis = [":rocket:", ":sparkles:", ":fire:", ":gem:", ":zap:", 
              ":star:", ":art:", ":dart:", ":rainbow:", ":party_popper:"]
    random_emoji = emoji.emojize(random.choice(emojis))

    # 使用 Faker 生成随机内容
    random_sentence = fake.sentence(nb_words=8)
    quote = fake.sentence(nb_words=12)
    generator = fake.name()
    city = fake.city()

    # 版本号和时间戳
    version = f"v1.0.{int(time.time()) % 1000}"
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    # 渲染模板
    template = Template(HTML_TEMPLATE)
    html = template.render(
        color1=color1, color2=color2,
        random_emoji=random_emoji,
        random_sentence=random_sentence,
        quote=quote,
        generator=generator,
        city=city,
        version=version,
        timestamp=timestamp,
    )

    # 写入文件
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ 构建成功！")
    print(f"   版本: {version}")
    print(f"   颜色: #{color1} → #{color2}")
    print(f"   Emoji: {random_emoji}")
    print(f"   生成者: {generator} ({city})")

if __name__ == "__main__":
    build()
