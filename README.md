# Agent 智能邮件发送助手

岳云鹏说：我的天呐！

一个基于 LangChain 构建的智能邮件发送 Agent，支持流式输出和 YAML 配置提示词。

## 📖 项目简介

本项目是一个智能邮件发送助手，通过自然语言交互方式，自动理解用户需求并调用邮件发送工具。项目采用 LangChain 框架，支持异步流式输出，提供良好的用户体验。

## ✨ 功能特点

- 🤖 **智能理解**：通过 LangChain Agent 自动理解用户意图
- 📧 **邮件发送**：集成 SMTP 协议，支持 SSL 加密发送
- 🌊 **流式输出**：支持异步流式响应，实时反馈处理进度
- 📝 **配置化提示词**：通过 YAML 文件管理 Prompt，便于维护和调整
- 🔧 **工具化设计**：邮件发送功能封装为 LangChain 工具，可复用
- 🎯 **参数验证**：使用 Pydantic 进行参数校验，提高健壮性

## 🏗️ 项目结构

agent-08-31/
├── prompt/ # 提示词模块
│ ├── **init**.py
│ ├── prompt_builder.py # 提示词构建器
│ └── email.yaml # 邮件助手提示词配置
├── tool/ # 工具模块
│ ├── **init**.py
│ └── send_email_tool.py # 邮件发送工具
├── model/ # 模型模块
│ ├── **init**.py
│ └── my_model.py # 大模型配置
├── demo/ # 示例代码
├── .env # 环境变量配置（敏感信息）
├── .gitignore # Git 忽略文件
└── README.md # 项目说明