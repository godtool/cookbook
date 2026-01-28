# 发票提取工具

[English](README.md) | [中文](README_zh.md)


[![Discord](https://img.shields.io/discord/1385439864920739850?color=7289da&label=Join%20Discord&logo=discord&logoColor=white)](https://discord.com/invite/liquid-ai)

一个从发票 PDF 中提取付款信息的 Python CLI。

这是一个使用本地 AI 构建工具与应用的实用示例，具备：

- 无云端成本
- 无网络延迟
- 不牺牲数据隐私


## 里面有什么？

在这个示例中，你将学习如何：

- **搭建本地 AI 推理**，使用 Ollama 在本机运行 Liquid 模型，无需云服务或 API Key
- **构建文件监控系统**，自动处理放入目录的新文件
- **从图像中提取结构化输出**，使用小型视觉语言模型 LFM2-VL-3B


## 架构说明

当你把发票图片放入被监控的目录时，工具会使用 [LFM2-VL-3B](https://huggingface.co/LiquidAI/LFM2-VL-3B) 提取发票中的关键信息，生成结构化记录，包括：

- 需要支付的服务/单位
- 付款金额
- 付款币种

该记录会追加到一个 CSV 文件中。

![](./media/diagram.jpg)


## 环境配置

你需要：

- [Ollama](https://ollama.com/) 用于本地提供语言模型服务。
- [uv](https://docs.astral.sh/uv/) 用于管理 Python 依赖并高效运行应用，无需手动创建虚拟环境。

### 安装 Ollama

<details>
<summary>点击查看各平台安装说明</summary>

**macOS:**
```bash
# 从官网下载安装包
# 访问: https://ollama.ai/download

# 或使用 Homebrew
brew install ollama
```

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Windows:**
从 [https://ollama.ai/download](https://ollama.ai/download) 下载并安装

</details>


### 安装 uv

<details>
<summary>点击查看各平台安装说明</summary>

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

</details>


## 如何运行？

先克隆仓库：

```sh
git clone https://github.com/Liquid4All/cookbook.git
cd cookbook/examples/invoice-parser
```

然后使用仓库内置的发票样例运行应用：
```sh
uv run python src/invoice_parser/main.py \
    --dir invoices/ \
    --image-model hf.co/LiquidAI/LFM2-VL-3B-GGUF:F16 \
    --process-existing
```


你可以根据需要修改发票目录路径与模型 ID。

> [!NOTE]
>
> 你也可以这样使用 1.6B 版本的 VLM 模型：
> 
> ```sh
> uv run python src/invoice_parser/main.py \
>     --dir invoices/ \
>     --image-model hf.co/LiquidAI/LFM2-VL-1.6B-GGUF:F16 \
>     --process-existing
> ```

如果你安装了 `make`，也可以用如下命令运行：
```sh
make run
```

从发票中提取的数据会保存在发票所在目录下的 `bills.csv` 文件中。
打开文件可以看到如下数据：

| processed_at | file_path | utility | amount | currency |
|--------------|-----------|---------|--------|----------|
| 2025-10-31 11:25:47 | invoices/water_australia.png | electricity | 68.46 | AUD |
| 2025-10-31 11:26:00 | invoices/Sample-electric-Bill-2023.jpg | electricity | 28.32 | USD |
| 2025-10-31 11:26:09 | invoices/british_gas.png | electricity | 81.31 | GBP |
| 2025-10-31 11:42:35 | invoices/castlewater1.png | electricity | 150.0 | USD |

观察：
- 前 3 张发票提取正确，金额与币种准确。
- 第 4 张发票提取不正确，金额与币种均有误。

## 下一步

在样例发票上，这个工具大约 75% 的时间表现良好，属于：

- 演示用途足够
- 生产场景不够

下一步我们会在做提示词优化或微调之前，先尝试最新的 `LFM2.5-VL-1.6B` 并比较结果。

如果你想进一步了解视觉语言模型的定制，我们推荐这个示例：

- [猫狗图像分类](https://github.com/Paulescu/image-classification-with-local-vlms/tree/main)


## 需要帮助？

加入 [Liquid AI Discord 社区](https://discord.com/invite/liquid-ai) 并提问。
[![Discord](https://img.shields.io/discord/1385439864920739850?color=7289da&label=Join%20Discord&logo=discord&logoColor=white)](https://discord.com/invite/liquid-ai)
