# LFM2 英韩翻译：基于 1.2B 参数的高效双向翻译

[English](README.md) | [中文](README_zh.md)


[![Discord](https://img.shields.io/discord/1385439864920739850?color=7289da&label=Join%20Discord&logo=discord&logoColor=white)](https://discord.com/invite/liquid-ai)

## 里面有什么？

基于 Liquid AI 的 LFM2 1.2B 模型微调而成的高效英韩双向翻译系统。该项目展示了领域定向微调如何在 Flores-200 基准上超越 3 倍参数规模的模型，性能超过 Google 的 Gemma-3 4B 和阿里巴巴的 Qwen3 4B。

关键特性：
- **自动语言检测** - 智能识别输入语言并自动翻译
- **高质量翻译** - Flores-200 基准上 CHrF++ 34.61 / BLEU 13.21
- **高效推理** - 通过合并适配器在中等硬件上也能运行
- **易用 CLI** - 基于 Fire 的简洁命令行接口

*该项目由 [Kiwoong Yeom](https://www.linkedin.com/in/kiwoong-yeom/) 构建并发布，并得到 [Maxime Labone](https://www.linkedin.com/in/maxime-labonne/) 的支持。*
*[LinkedIn 原始发布链接](https://www.linkedin.com/posts/activity-7406831565210583040-2B9p?utm_source=share&utm_medium=member_desktop&rcm=ACoAAAqH-bMBMXBij-GI7SN8H4dk_E4j4k19f_w)*

## 快速开始

1. 克隆仓库
```bash
git clone https://github.com/Liquid4All/cookbook.git
cd cookbook/examples/lfm2-english-to-korean
```

2. 安装依赖
```bash
uv sync
```

3. 运行翻译示例
```bash
uv run python main.py --text "$(cat linkedin_post.txt)" --max-new-tokens 1024
```

## 架构说明

系统采用两阶段训练方法：

1. **监督微调（SFT）**：使用 28 万条高质量英韩平行数据打下翻译基础
2. **强化学习（RL）**：通过 GRPO 优化并增加 1 万条样本提升翻译质量

### 模型组件

- **基础模型**：`gyung/lfm2-1.2b-koen-mt-v6.4-merged` - 经过 SFT 微调的 LFM2 1.2B
- **适配器**：`gyung/lfm2-1.2b-koen-mt-v8-rl-10k-adapter` - 通过 GRPO 训练的 LoRA 适配器
- **自动检测**：使用正则表达式匹配韩文文本（韩文音节与字母）

系统会自动检测输入语言，并执行对应方向的翻译，支持英→韩与韩→英双向翻译。

## CLI 使用方式

```bash
uv run python main.py [OPTIONS]

Options:
  --text TEXT                    要翻译的文本（必填）
  --model-name TEXT             基础模型名称（默认：gyung/lfm2-1.2b-koen-mt-v6.4-merged）
  --adapter-name TEXT           适配器名称（默认：gyung/lfm2-1.2b-koen-mt-v8-rl-10k-adapter）
  --max-new-tokens INTEGER     最大生成 token 数（默认：256）
  --temperature FLOAT          采样温度（默认：0.3）
  --min-p FLOAT               最小概率阈值（默认：0.15）
  --repetition-penalty FLOAT   重复惩罚（默认：1.05）
```

### 使用示例

英译韩：
```bash
uv run python main.py --text "Hello, how are you today?"
```

韩译英：
```bash
uv run python main.py --text "안녕하세요, 오늘 어떻게 지내세요?"
```

处理文件：
```bash
uv run python main.py --text "$(cat your_file.txt)" --max-new-tokens 1024
```

## 性能基准

Flores-200 基准（1,012 条样本）：

| 模型 | 参数量 | CHrF++ | BLEU |
|-------|------------|--------|------|
| **LFM2-KoEn-v8-rl** | **1.2B** | **34.61** | **13.21** |
| Gemma-3-4B | 4B | 32.83 | 11.36 |
| Qwen3-4B | 4B | 25.62 | 7.46 |

1.2B 参数模型超越 3 倍规模模型，证明专门化训练比单纯增加参数量更关键。

## 进一步改进

提升性能与效率的下一步：

- **速度优化**：量化技术（GGUF、AWQ、GPTQ）
- **llama.cpp 集成**：更快的 CPU 推理
- **全参数 RL 训练**：扩大算力资源
- **移除长度归一化**：参考 Qwen 团队最新发现
- **扩展数据集训练**：20 万 SFT + 2.5 万 RL 样本

### 性能优化方向

当前实现使用适配器合并以加速推理。未来可考虑：

- 面向资源受限环境的量化模型版本
- 实时翻译的流式推理
- 大文档翻译的批处理

## 需要帮助？

加入 [Liquid AI Discord 社区](https://discord.com/invite/liquid-ai) 并提问。
[![Discord](https://img.shields.io/discord/1385439864920739850?color=7289da&label=Join%20Discord&logo=discord&logoColor=white)](https://discord.com/invite/liquid-ai)
