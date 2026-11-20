"""
AI 需求助手：把访谈记录交给大模型，让它按"不许编造、标注出处"的要求提取需求。

和第 3 周的区别：第 3 周是在聊天窗口里问 AI；这里把提示词写进程序，
同一个提示词可以反复运行、对比结果、放进 Git 管理 —— 这就是"提示词工程化"。

运行（在 repair_system 文件夹里）：
    python tools/ai_requirements.py              # 用严格版提示词（模板 T4-01）
    python tools/ai_requirements.py --naive      # 用"随便问"的提示词，对比一下差别
结果保存在 docs/ 目录下。

需要 .env 里配置 Key（和第 3 周一样，把 .env.example 复制成 .env 再填 Key）。
没有 Key 也没关系：把下面 STRICT 里的提示词复制到网页版 DeepSeek / 通义 / 豆包，效果一样。
"""
import os
import sys

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

NAIVE = "帮我把下面的访谈记录整理成一份需求文档。"

STRICT = """你是一名有 10 年经验的需求分析师。下面是一份客户访谈记录。
请从中提取需求，严格遵守：
1. 只提取访谈中明确提到的内容，不要补充"一般系统都有"的功能；
2. 每条需求后面用【原话】标注出处，引用访谈中的原句；
3. 遇到前后矛盾、语气犹豫（"都行""可以考虑"）的地方，不要替我决定，
   把它单独列入"待确认问题"，并写出两种可选方案；
4. 遇到"美观""快速""安全"这类无法验收的说法，改写成可度量的标准，并标注【待确认】；
5. 输出：先输出 Markdown 表格（编号 | 角色 | 需求描述 | 原话出处），再输出"待确认问题"列表。"""


def main():
    naive = "--naive" in sys.argv
    key = os.getenv("LLM_API_KEY", "")
    if not key or key.startswith("sk-在这里"):
        raise SystemExit("没有配置 LLM_API_KEY。可以把本文件里 STRICT 的提示词复制到网页版大模型里使用。")

    from openai import OpenAI
    client = OpenAI(api_key=key, base_url=os.getenv("LLM_BASE_URL", "https://api.deepseek.com"))

    with open(os.path.join(ROOT, "docs", "访谈记录.md"), encoding="utf-8") as f:
        interview = f.read()

    prompt = NAIVE if naive else STRICT
    print(f"使用{'随便问' if naive else '严格版'}提示词，正在请求模型（约 20~60 秒）……")
    resp = client.chat.completions.create(
        model=os.getenv("LLM_MODEL", "deepseek-chat"),
        messages=[{"role": "system", "content": prompt},
                  {"role": "user", "content": f'访谈记录：\n"""\n{interview}\n"""'}],
        temperature=0.2,          # 整理需求要稳，不要太"有创意"
    )
    out = os.path.join(ROOT, "docs", f"AI需求初稿_{'随便问' if naive else '严格版'}.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write(resp.choices[0].message.content)
    print(f"已保存：{out}")
    print(f"本次用了 {resp.usage.total_tokens} 个 token。")
    print("下一步：拿《需求审查清单》检查它。记住，AI 的输出是初稿，不是答案。")


if __name__ == "__main__":
    main()
