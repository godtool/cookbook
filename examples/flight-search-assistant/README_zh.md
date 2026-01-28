# 使用 LFM2.5-1.2B-Thinking 查找并预订机票

[English](README.md) | [中文](README_zh.md)


[![Discord](https://img.shields.io/discord/1385439864920739850?color=7289da&label=Join%20Discord&logo=discord&logoColor=white)](https://discord.com/invite/liquid-ai)

这是一个最小化的 Python CLI，使用工具调用与推理来完成多步流程，帮助你查找并预订机票。

例如：
```Book the cheapest flight from Barcelona to Belgrade on 2026-01-31```

该项目展示了 LFM2.5-1.2B-Thinking 的能力——一个小型语言模型，擅长需要推理、逻辑与强工具调用能力的任务。更棒的是，它可以运行在端侧设备上。

![See it in action](./media/demo.gif)

### 目录
- [快速开始](#快速开始)
- [工作原理](#工作原理)
- [下一步](#下一步)
- [需要帮助？](#需要帮助)

## 快速开始

1. 确保系统已安装 `uv`
    ```
    uv --version
    ```
    如果命令失败，请按照 [这些说明](https://docs.astral.sh/uv/getting-started/installation/) 安装 `uv`。


2. 构建项目
    ```
    uv sync
    ```

3. 使用机票搜索助手查找并预订机票。例如：
    ```
    # 单次调用 `search_flights`
    uv run flight_search.py --query "What flights are available from New York to Paris on 2026-01-19?"
    
    # 单次调用 `book_flight`
    uv run flight_search.py --query "Book flight AA495 for 2026-02-04"

    # 2 步顺序调用：先 `search_flights` 再 `book_flight`
    uv run flight_search.py --query "Book the cheapest flight from Barcelona to Belgrade on 2026-01-31"

    # N 步顺序调用
    uv run flight_search.py --query "Book the cheapest flight from Barcelona to a US city on the East Coast that is not NYC on 2026-02-14"
    ```

## 工作原理

模型可访问 2 个工具：

- `search_flights` -> 检索上下文信息
- `book_flights` -> 对外部世界执行操作

> **Note:** `search_flights` 与 `book_flight` 函数使用的是用于演示的合成数据。若用于生产环境，可集成真实航班数据 API（如 Amadeus、Skyscanner 或 Kiwi）。

给定用户请求（例如 `Book the cheapest flight from Barcelona to Belgrade on 2026-01-31`），模型会迭代执行：

- 生成包含工具调用的响应
- 执行工具调用
- 重新生成响应

模型完全本地运行，使用 llama.cpp 提供服务，使用的是

## 下一步

- [ ] 添加评估数据集与循环。
- [ ] 如有必要，使用带可验证奖励的 GRPO 微调提升模型性能。


## 需要帮助？
加入 Liquid AI Discord 社区并提问。

[![Discord](https://img.shields.io/discord/1385439864920739850?color=7289da&label=Join%20Discord&logo=discord&logoColor=white)](https://discord.com/invite/liquid-ai)
