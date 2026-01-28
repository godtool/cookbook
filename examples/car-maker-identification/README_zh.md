# 微调 LFM2-VL 进行车辆品牌识别

[English](README.md) | [中文](README_zh.md)


[![Discord](https://img.shields.io/discord/1385439864920739850?color=7289da&label=Join%20Discord&logo=discord&logoColor=white)](https://discord.com/invite/liquid-ai)

这是一个分步骤的教程，演示如何微调视觉语言模型用于图像识别任务。本示例任务是从图片中识别汽车厂商，但其中的思路可迁移到你感兴趣的任何图像分类任务。

![](./media/task.png)

## 目录

- [你将学到什么](#你将学到什么)
- [快速开始](#快速开始)
- [环境准备](#环境准备)
  - [安装 UV](#安装-uv)
  - [Modal 配置](#modal-配置)
  - [Weights & Biases 配置](#weights--biases-配置)
  - [安装 make](#安装-make)
- [步骤](#微调-lfm2-vl-完成本任务的步骤)
- [步骤 1：数据集准备](#步骤-1数据集准备)
- [步骤 2：LFM2-VL 模型基线表现](#步骤-2lfm2-vl-模型基线表现)
- [步骤 3：结构化生成提升模型鲁棒性](#步骤-3结构化生成提升模型鲁棒性)
- [步骤 4：使用 LoRA 微调](#步骤-4使用-lora-微调)
- [接下来？](#接下来)


## 你将学到什么

在本示例中，你将学习如何：

- 构建与模型无关的**评估流水线**，用于视觉分类任务
- **使用 Outlines 的结构化输出**确保一致可靠的模型响应并提升准确率
- **使用 LoRA 微调视觉语言模型**，进一步提高准确率


## 快速开始

### 1. 克隆仓库：
```sh
git clone https://github.com/Liquid4All/cookbook.git
cd cookbook/examples/car-maker-identification
```

### 2. 在不使用结构化生成的情况下评估基础 LFM2-VL 模型
```sh
make evaluate config=eval_lfm_450M_raw_generation.yaml
make evaluate config=eval_lfm_1.6B_raw_generation.yaml
make evaluate config=eval_lfm_3B_raw_generation.yaml
```

### 3. 使用结构化生成评估基础 LFM2-VL 模型
```sh
make evaluate config=eval_lfm_450M_structured_generation.yaml
make evaluate config=eval_lfm_1.6B_structured_generation.yaml
make evaluate config=eval_lfm_3B_structured_generation.yaml
```

### 4. 使用 LoRA 微调基础 LFM2-VL 模型
```sh
make fine-tune config=finetune_lfm_450M.yaml
make fine-tune config=finetune_lfm_1.6B.yaml
make fine-tune config=finetune_lfm_3B.yaml
```


## 环境准备

你需要：

- [uv](https://docs.astral.sh/uv/) 用于管理 Python 依赖并高效运行应用，无需手动创建虚拟环境。

- [Modal](https://modal.com/) 用于 GPU 云计算。没有 GPU 的话，微调视觉语言模型会非常慢。Modal 是一种便捷方式，可按量付费且无需运维配置，帮我们快速启动微调实验。

- [Weights & Biases](https://wandb.ai/)（可选，但强烈推荐）用于实验跟踪与监控

- [make](https://www.gnu.org/software/make/)（可选）用于简化运行与微调实验流程

我们逐个来。

### 安装 UV

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

### Modal 配置

<details>
<summary>点击查看安装说明</summary>

1. 在 [modal.com](https://modal.com/) 创建账号
2. 在虚拟环境中安装 Modal Python 包：
   ```bash
   uv add modal
   ```
3. 使用 Modal 进行认证：
   ```bash
   uv run modal setup
   ```
   如果第一条命令失败，尝试：
   ```bash
   uv run python -m modal setup
   ```
</details>

### Weights & Biases 配置

<details>
<summary>点击查看安装说明</summary>

1. 在 [wandb.ai](https://wandb.ai/) 创建账号
2. 在虚拟环境中安装 Weights & Biases Python 包：
   ```bash
   uv add wandb
   ```
3. 使用 Weights & Biases 认证：
   ```bash
   uv run wandb login
   ```
   该命令会打开浏览器窗口，复制你的 API Key 并粘贴到终端。
</details>

### 安装 make

<details>
<summary>点击查看安装说明</summary>

1. 安装 make：
   ```bash
   sudo apt-get install make
   ```
</details>

<br>
安装完这些工具后，克隆仓库并创建虚拟环境：

```sh
git clone https://github.com/Liquid4All/cookbook.git
cd cookbook/examples/car-maker-identification
uv sync
```

## 微调 LFM2-VL 完成本任务的步骤

以下是我们为“汽车厂商识别”微调 LFM2-VL 的系统流程：

1. **准备数据集**。收集准确且多样的 (image, car_maker) 配对数据，覆盖模型部署后可能遇到的输入分布。尽量覆盖更多厂商，避免分布外问题。

2. **建立基线表现**。评估不同规模的预训练模型（450M、1.6B、3B）以了解当前能力。如果结果已满足需求且符合部署约束，就无需微调。否则就需要微调。

3. **使用 LoRA 微调**。应用低秩适配进行参数高效微调，提升准确率且控制计算成本。

4. **评估改进**。将微调后模型与基线对比评估，衡量定制效果。如果满意就结束；不满意则深入分析失败案例，改进数据集或微调流程。

我们逐步展开。


## 步骤 1：数据集准备

数据集构建是整个项目中最关键的一环。

> [!NOTE]
> 微调后的语言模型的好坏，**取决于用于微调的数据集质量**。

> [!TIP]
> **这里的“好”指什么？**
>
> 用于图像分类的优质数据集需要：
>
> - **准确**：标签必须与图像正确匹配。对于汽车厂商识别，这意味着每张车图都标注正确厂商（例如 BMW X5 应标为 “BMW”，不是 “Mercedes-Benz”）。错误标注会教坏模型。
>
> - **多样**：数据集应覆盖生产环境中可能遇到的各种条件，包括：
>   - 每个厂商的不同车型
>   - 不同角度、光照与背景
>   - 不同图像质量与分辨率
>   - 不同年份与不同状态（新车、旧车、脏车、干净车）


本指南使用托管在 Hugging Face 的 [Stanford Cars 数据集](https://huggingface.co/datasets/Paulescu/stanford_cars)。

该数据集包含：

- **类别**：49 个汽车厂商。
- **划分**：训练集（6,860 张）与测试集（6,750 张）。

[TODO 添加类别分布条形图]

数据集还包含多个带图像扰动（高斯噪声、运动模糊等）的额外划分，用于鲁棒性测试。本教程仅使用训练与测试划分。


## 步骤 2：LFM2-VL 模型基线表现

在任何微调实验前，需要先建立现有模型的基线表现。本例评估以下模型：

- LFM2-VL-450M
- LFM2-VL-1.6B
- LFM2-VL-3B

为构建与模型无关的评估脚本，最佳实践是将评估逻辑与模型/数据集代码解耦。可以将实验参数封装到配置文件中，常见做法是使用 YAML 文件，本例亦如此。

在 `configs` 目录中，你会看到评估这 3 个模型的 YAML 文件：

```sh
configs/
   ├── eval_lfm_450M_raw_generation.yaml
   ├── eval_lfm_1.6B_raw_generation.yaml
   └── eval_lfm_3B_raw_generation.yaml
```

这些 YAML 配置通过 `src/car_maker_identification/config.py` 中的 `EvaluationConfig` 类加载，确保：
- 所有必要参数都已传入
- 参数类型和值都合法

我们对 3 个模型使用相同的 100 条样本评估数据，以及相同的 system/user prompt。

<details>
<summary>点击查看 system 与 user prompt</summary>

```yaml
system_prompt: |
  You excel at identifying car makers from pictures.

user_prompt: |
  What car maker do you see in this picture?
  Pick one from the following list:

  - AM
  - Acura
  - Aston
  - Audi
  - BMW
  - Bentley
  - Bugatti
  - Buick
  - Cadillac
  - Chevrolet
  - Chrysler
  - Daewoo
  - Dodge
  - Eagle
  - FIAT
  - Ferrari
  - Fisker
  - Ford
  - GMC
  - Geo
  - HUMMER
  - Honda
  - Hyundai
  - Infiniti
  - Isuzu
  - Jaguar
  - Jeep
  - Lamborghini
  - Land
  - Lincoln
  - MINI
  - Maybach
  - Mazda
  - McLaren
  - Mercedes-Benz
  - Mitsubishi
  - Nissan
  - Plymouth
  - Porsche
  - Ram
  - Rolls-Royce
  - Scion
  - Spyker
  - Suzuki
  - Tesla
  - Toyota
  - Volkswagen
  - Volvo
  - smart
```
</details>
<br>

使用以下命令对 3 个模型进行评估：
```sh
make evaluate config=eval_lfm_450M_raw_generation.yaml
make evaluate config=eval_lfm_1.6B_raw_generation.yaml
make evaluate config=eval_lfm_3B_raw_generation.yaml
```

每次评估都会记录为一次 Weights & Biases 运行，你可以在 [WandB 仪表盘](https://wandb.ai/home) 查看结果。我们记录两个关键指标：

- **准确率**：模型正确分类图片的比例，用于总体性能判断。
- **混淆矩阵**：展示预测标签与真实标签之间的关系，帮助理解各类别表现。


### 结果

从准确率来看，只有 3B 模型具备相对可用的表现，450M 与 1.6B 模型表现很差。

| 模型 | 准确率 |
|-------|----------|
| LFM2-VL-450M | 3% |
| LFM2-VL-1.6B | 0% |
| LFM2-VL-3B | 66% |

但在责怪模型之前，我们需要更深入分析预测结果。

如果你查看 3B 模型的混淆矩阵，会发现它整体表现尚可，但也会出现严重错误，生成不属于任何厂商名称的输出。

![](./media/confusion_matrix_lfm2_3b_raw_generation.png)

这个问题不仅限于 3B 模型。450M 和 1.6B 的混淆矩阵同样存在类似模式。

因此我们面临第一个挑战：如何“强制”模型只输出厂商列表中的合法结果？

这就是下一步要解决的问题。

## 步骤 3：结构化生成提升模型鲁棒性

结构化生成是一种让语言模型“被迫”输出特定格式的技术，例如 JSON，或（如本例）输出厂商列表中的合法值。

> [!NOTE]
> **请记住**
>
> 语言模型是逐 token 采样生成文本的。每个解码步骤，模型都会生成下一个 token 的概率分布，并据此采样。
>
> 结构化生成会在每个解码步骤进行“干预”，屏蔽与目标结构不兼容的 token。

![](./media/structured_generation.webp)

在 Python 应用中，我们推荐使用 [Outlines](https://github.com/dottxt-ai/outlines) 进行结构化生成，因为它易用、稳定且文档完善。

使用 Outlines 时，我们先定义输出模式，然后 Outlines 会在推理时与推理引擎（本例为 Transformers）集成，确保每个解码步骤只生成符合模式的 token。

```python
class CarIdentificationOutputType(BaseModel):
   pred_class: Literal[
      "AM",
      "Acura",
      "Aston",
      "Audi",
      "BMW",
      "Bentley",
      "Bugatti",
      "Buick",
      ...
      "Tesla",
      "Toyota",
      "Volkswagen",
      "Volvo",
      "smart",
   ]
```

用于结构化生成评估的 3 个配置文件如下：
```sh
configs/
   ├── eval_lfm_450M_structured_generation.yaml
   ├── eval_lfm_1.6B_structured_generation.yaml
   └── eval_lfm_3B_structured_generation.yaml
```

可使用如下命令重新评估：
```sh
make evaluate config=eval_lfm_450M_structured_generation.yaml
make evaluate config=eval_lfm_1.6B_structured_generation.yaml
make evaluate config=eval_lfm_3B_structured_generation.yaml
```

### 结果

| 模型 | 准确率 |
|-------|----------|
| LFM2-VL-450M | 58% |
| LFM2-VL-1.6B | 74% |
| LFM2-VL-3B | 81% |

查看 3B 模型的混淆矩阵会发现，它只输出合法厂商名称，不再生成其他文本。很好！

![](./media/confusion_matrix_lfm2_3b_structured_generation.png)

此时你需要判断性能是否满足需求。若满足即可结束；否则需要微调。

## 步骤 4：使用 LoRA 微调

我们使用 LoRA 技术进行微调。LoRA 是一种参数高效的微调方法，通过添加并训练少量参数来调整模型。

![](./media/lora.webp)

你可以这样对 3 个 LFM2-VL 模型进行 LoRA 微调：
```sh
make fine-tune config=finetune_lfm_450M.yaml
make fine-tune config=finetune_lfm_1.6B.yaml
make fine-tune config=finetune_lfm_3B.yaml
```

三种模型的训练损失曲线收敛到不同水平，其中：

- LFM2-VL-3B 损失最低
- LFM2-VL-450M 损失最高

![](./media/train_loss.png)

这说明在相同训练数据下，LFM2-VL-3B 能更好地拟合数据。

然而训练损失本身并不能说明真实表现。语言模型高度参数化，能拟合训练数据中的**任何**模式，包括噪声，而噪声无法泛化到测试集。

因此我们需要看评估损失曲线，了解模型在留出数据上的表现。

![](./media/eval_loss.png)

同样，LFM2-VL-3B 表现最好。其评估损失严格下降，说明模型逐轮学习且尚未过拟合。

下表展示了微调过程中不同 checkpoint 的评估损失：

| Checkpoint | Train Loss | Eval Loss |
|------------|------------|-----------|
| 100        | 5.82       | 5.46      |
| 200        | 0.16       | 0.20      |
| 300        | 0.07       | 0.10      |
| 500        | 0.03       | 0.03      |
| 1000        | 0.008       | 0.005      |

> [!TIP]
> **什么是过拟合？**
>
> 过拟合是指模型学到了训练数据的噪声，无法泛化到测试集。即训练损失下降，而评估损失上升。

此时我们可以认为 LFM2-VL-3B 是最有前景的模型。

但仍需检查其在测试集上的实际表现。

因此回到评估步骤。

### 在测试集上评估微调模型

使用 `evaluate.py` 再次评估，但这次使用最后一个模型 checkpoint。

```sh
make evaluate config=eval_lfm_3B_checkpoint_1000.yaml
```

### 结果

| Checkpoint | 准确率 |
|------------|----------|
| Base Model (LFM2-VL-3B) | 81% |
| checkpoint-1000 | 82% |

微调模型的混淆矩阵如下：

![](./media/confusion_matrix_lfm2_3b_checkpoint_1000.png)

## 接下来？

在这个示例中，我们展示了微调视觉语言模型进行图像识别任务的主要步骤。

如前所述，最终模型质量取决于用于微调的数据集质量。

要提升数据集质量，你可以：

- 过滤严重裁剪、遮挡或低质量图像（品牌难以辨识）的样本，从而提高质量

- 通过数据增强提升少数类的多样性
