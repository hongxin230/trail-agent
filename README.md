# Trail Running AI Agent

一个基于 LangGraph 构建的 AI Agent 项目，面向越野跑训练与装备推荐场景。

项目实现了：

* LangGraph Agent Workflow
* Tool Calling
* RAG（Retrieval Augmented Generation）
* FastAPI 服务化部署
* DeepSeek LLM 集成

---

# 项目背景

越野跑训练涉及：

* 训练计划制定
* 周跑量计算
* 长距离训练安排
* 装备选择
* 赛事准备

传统 ChatBot 只能回答问题，而无法结合训练规则、工具计算和装备知识库进行决策。

因此构建一个具备：

* Workflow
* Tool Calling
* RAG

能力的 AI Agent。

---

# 项目功能

## 1. Training Agent

根据用户目标赛事和训练情况生成训练计划。

示例：

输入：

我要准备50km越野赛，目前周跑量40km

输出：

* 4周训练计划
* 周跑量建议
* 长距离训练安排
* 训练建议

---

## 2. Tool Calling

针对确定性逻辑，调用 Python Tool。

当前实现：

### calculate_weekly_volume

计算下一周训练量。

### suggest_long_run

根据周跑量推荐长距离训练距离。

示例：

输入：

我当前周跑量40km

输出：

下一周建议44km

---

## 3. Gear Agent

基于装备知识库进行推荐。

示例：

输入：

推荐适合100km越野赛的跑鞋

输出：

* Hoka Speedgoat 6
* Hoka Mafate Speed 4
* Salomon Genesis

并给出推荐理由。

---

## 4. RAG知识库

使用 Chroma 构建向量数据库。

知识库包含：

* 越野跑鞋
* 越野跑背包
* 跑杖
* GPS手表

支持：

* 相似度检索
* TopK召回
* 基于知识库回答

---

# 技术架构

## 整体架构

                        User
                          │
                          ▼
                    FastAPI API
                          │
                          ▼
                    LangGraph
                          │
                    Router Node
                 ┌────────┴────────┐
                 │                 │
                 ▼                 ▼

          Training Agent      Gear Agent
                 │                 │
                 ▼                 ▼

           Tool Calling         RAG

                 │                 │
                 ▼                 ▼

         Training Tools      Chroma Vector DB

                 └──────┬──────────┘
                        ▼

                   DeepSeek LLM

                        ▼

                 Structured Output

---

## Agent Workflow

Training Agent：

Question

↓

Tool Decision

↓

Tool Execution

↓

LLM Summary

↓

Training Plan

---

Gear Agent：

Question

↓

Embedding

↓

Vector Search

↓

TopK Documents

↓

Prompt Construction

↓

DeepSeek

↓

Recommendation

---

# 技术栈

* Python
* FastAPI
* LangGraph
* DeepSeek
* Chroma
* LangChain
* Sentence Transformers

---

# 项目结构

trail-agent/

├── app/

│   ├── main.py

│   └── config.py

│

├── agents/

│   ├── training_agent.py

│   ├── gear_agent.py

│   └── chat_agent.py

│

├── graph/

│   ├── graph.py

│   └── state.py

│

├── rag/

│   ├── build_vector_store.py

│   ├── retriever.py

│   └── test_retriever.py

│

├── tools/

│   ├── training_tools.py

│   └── tool_registry.py

│

├── prompts/

│   ├── training_prompt.py

│   └── gear_prompt.py

│

├── data/

│   └── gear_docs.json

│

├── chroma_db/

│

├── requirements.txt

│

└── README.md

---

# 快速开始

## 1. 克隆项目

git clone <your-repo-url>

cd trail-agent

---

## 2. 创建虚拟环境

python -m venv venv

source venv/bin/activate

---

## 3. 安装依赖

pip install -r requirements.txt

---

## 4. 配置环境变量

创建 .env

DEEPSEEK_API_KEY=your_api_key

---

## 5. 构建向量库

python rag/build_vector_store.py

---

## 6. 启动服务

uvicorn app.main:app --reload

---

## 7. 访问接口

http://127.0.0.1:8000/docs

---

# API 示例

POST /chat

请求：

{
"message": "推荐100公里越野跑鞋"
}

返回：

{
"type": "gear_recommendation",
"data": {
"recommended_products": [
{
"name": "Hoka Speedgoat 6",
"reason": "适合长距离越野赛事"
}
]
},
"metadata": {
"retrieved_docs": 3
}
}

---

# 后续规划

* 用户训练历史 Memory
* Garmin / Coros 数据接入
* Strava 数据同步
* Multi-Agent 协作
* MCP Tool 集成
* 赛事知识库扩展

---

# 作者

Zhao Hongxin


