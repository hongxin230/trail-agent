import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from config import client

resp = client.chat.completions.create(
    model="deepseek-v4-flash",
    messages=[
        {"role":"user","content":"你好"}
    ]
)

print(resp.choices[0].message.content)