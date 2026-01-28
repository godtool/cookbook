# 使用 GRPO 与 OpenEnv 微调 LFM2-350M 进行浏览器控制

[English](README.md) | [中文](README_zh.md)


[![Discord](https://img.shields.io/discord/1385439864920739850?color=7289da&label=Join%20Discord&logo=discord&logoColor=white)](https://discord.gg/DFU3WQeaYD)

### 目录
- [什么是浏览器控制？](#什么是浏览器控制)
- [真实世界用例](#真实世界用例)
- [为什么需要强化学习（RL）？](#为什么需要强化学习rl)
  - [示例](#示例)
- [RL 训练框架的构建模块](#rl-训练框架的构建模块)
  - [1. 环境 -> 通过 OpenEnv 使用 BrowserGym](#1-环境---通过-openenv-使用-browsergym)
  - [2. RL 算法 -> GRPO](#2-rl-算法---grpo)
  - [3. 策略 -> LFM2-350M](#3-策略---lfm2-350m)
- [架构](#架构)
- [实验](#实验)
  - [全量微调](#全量微调)
  - [使用 LoRA 的高效微调](#使用-lora-的高效微调)
- [下一步](#下一步)


## 什么是浏览器控制？

浏览器控制是指语言模型通过生成一系列动作（点击元素、输入文本、滚动等）来导航并与网站交互，以完成用户指定的任务，比如订机票、填写表单或从网页提取信息。

例如：

- 视觉语言模型（VLM）可将截图与用户目标作为输入，生成完成目标的动作序列。

    ![](./media/browser_control_multimodal.gif)

- 纯文本语言模型可以将页面 HTML 作为输入，并以相同方式行动。

    ![](./media/browser_control_text_only.gif)

## 真实世界用例
浏览器控制有许多真实应用场景，包括正向用途，例如：

- **无障碍辅助**：屏幕阅读器伙伴帮助视障用户在亚马逊或生鲜配送网站完成复杂结账流程、阅读商品描述并下单

- **医疗预约管理**：应用自动检查多个诊所网站的预约情况，选择与你保险匹配的最早时段并加入日历

- **账单支付自动化**：每月自动访问公共事业网站，核对金额并从银行账户安排付款

不过，任何强大的技术也可能被滥用，例如：

- **评价操纵**：机器人创建虚假账号在亚马逊、Yelp 或 Google 发布虚假评论，以抬高商品评分或打击竞争对手

了解这些系统如何训练与部署，对于最大化正面价值、最小化负面影响至关重要。


## 为什么需要强化学习（RL）？

在浏览器控制任务中，往往存在多种有效的完成路径。验证语言模型是否完成任务（带可验证奖励的 RL）通常比收集足够大且多样的 (输入, 输出) 样本用于监督微调更容易、更便宜也更快。

### 示例
任务：“预订 2016/12/06 从 LAF 到 Akuton, AK 的最短单程航班”

![](./media/book-flight.png)

这个问题可能有很多解法：从“理想路径”（先填 From，再填 To，再填日期）到“出错后修正”（比如误输入 LAT，再改回并完成）。

为 SFT 收集涵盖这些情况的专家示范很不现实。而 RL 环境可以在每步验证任务是否完成，并提供稀疏反馈（奖励），RL 算法据此迭代提升模型表现。

此外，RL 还能让模型学会出错时纠正路径。如果点错元素或进入意料之外的页面，模型可以回退并尝试其他路径。而仅用成功示范训练的 SFT 模型一旦偏离预期轨迹往往会卡住。

因此我们在该任务中使用 RL 而非 SFT。当然，也可以先用 SFT 进行热身，再用 RL 提升性能。


## RL 训练框架的构建模块

RL 的核心思路是让语言模型（即策略）反复：

- 观察环境 **状态**（例如网站 DOM 元素）
- 输出一个 **动作**（即文本补全）
- 偶尔从环境获得正向奖励（反馈）

![](./media/not_so_happy_path_example.gif)

重复这个过程并配合合适的 RL 算法，语言模型会逐步提升完成任务的能力。

浏览器控制任务的奖励可通过 [Playwright](https://github.com/microsoft/playwright) 等工具以编程方式计算。Playwright 是端到端测试框架，可：

- 从页面 DOM 中提取结构与内容
- 检查 URL 来验证是否到达目标页面
- 查询数据库以确认代理是否正确修改系统状态

### 1. 环境 -> 通过 OpenEnv 使用 BrowserGym

[OpenEnv](https://github.com/meta-pytorch/OpenEnv) 是一个开源库，能够：

- 标准化 Python 对大量 RL 环境的访问
- 将 RL 环境作为独立 **Docker 容器** 部署，可在本地、Kubernetes 或 Hugging Face Spaces 上运行
- 帮助研究人员创建并发布新的 RL 环境

OpenEnv 内置的环境之一是 [BrowserGym](https://github.com/ServiceNow/BrowserGym)，它是一个开源浏览器自动化基准集合：

- [Mini World of Bits++](https://miniwob.farama.org/)（即 MiniWoB）
- [WebArena](https://github.com/web-arena-x/webarena)
- [VisualWebArena](https://github.com/web-arena-x/visualwebarena)
- [WorkArena](https://github.com/ServiceNow/WorkArena)

MiniWoB 是 BrowserGym 中最简单的基准，因为任务定义非常明确，是 RL 练习的绝佳起点。这里有一些示例任务，完整列表见 [这里](https://miniwob.farama.org/environments/list/)。

![](https://miniwob.farama.org/_images/showcase.gif)

在本仓库中，我们使用 MiniWoB 的简单任务 `click-test`，即学会点击按钮。

![](./media/click_test.gif)

它足够简单，可以展示完整训练流水线而无需太久训练。

也欢迎你从 [这个列表](https://miniwob.farama.org/environments/list/) 选择其他任务，消耗一些 GPU 来跑出更好的性能。

### 2. RL 算法 -> GRPO

当语言模型与环境交互时，会收集一系列带稀疏奖励的 rollouts。RL 算法（如 GRPO）使用这些稀疏奖励调整模型参数，提高获得高奖励的概率。

下面是同一初始提示/任务的 4 个 rollout 示例，模型分别：

1. 第一步完成任务
2. 第二步完成任务
3. 第三步完成任务
4. 第四步后仍未完成（这是我们设定的最大 rollout 步数）

![](./media/4_rollouts.gif)

GRPO 使用组内相对表现来判断强化哪些动作。

![](./media/grpo_rewards.jpg)

表现优于同组的响应会获得正向优势，表现较差的获得负向优势。相比 PPO 等以往算法，GRPO 更省内存，因为不需要训练和存储用于价值函数的第二个语言模型。

GRPO 已成为 AI 实验室和实践者使用最广泛的 RL 算法之一。

### 3. 策略 -> LFM2-350M

我们将使用 [LFM2-350M](https://huggingface.co/LiquidAI/LFM2-350M)，这是一个小而强、速度快的语言模型，具备：
- 知识能力（MMLU、GPQA）
- 指令跟随（IFEval、IFBench）
- 数学推理（GSM8K、MGSM）

为加速训练，我们还会加入 LoRA 适配器支持，避免全量微调。


## 架构

RL 训练框架的 3 个组件如下：

1. 来自 trl 的 `GRPOTrainer` 实现 GRPO 算法。需要在 GPU 上运行以保证反向传播足够快。
2. 用于生成 rollouts 的 `vLLM` 服务器，基于 LFM2-300M。需要 GPU 并行生成。
3. 运行 `BrowserGym` 环境的 Docker 容器，作为 Hugging Face Space 部署。可在本地或 Kubernetes 上运行，CPU 即可。

![](./media/3_components.jpg)

为简化流程，我们将 `GRPOTrainer` 与 `vLLM` 部署在同一张 GPU 上。

![](./media/collocate_vllm.jpg)

我们使用 [Modal](https://modal.com/) 作为无服务器 GPU 基础设施。Modal 适合不想投入过多运维、希望按量付费的 AI 工程师。它提供按需 GPU 与简洁的 Python 配置，方便在不管理集群或复杂 DevOps 的情况下扩展训练任务。

## 实验

### 全量微调

第一个实验是对 LFM2-350M 进行全量微调：

```
make run config=lfm2_350m.yaml
```

`click-test` 任务很简单，模型从零开始在不到 10 次尝试内即可完成。

最终 checkpoint 已发布在 HF：

- [Paulescu/LFM2-350M-browsergym-20251224-013119](https://huggingface.co/Paulescu/LFM2-350M-browsergym-20251224-013119)


### 使用 LoRA 的高效微调

LoRA 以更少算力与时间即可达到接近全量微调的效果。
```
make run config=lfm2_350m_lora.yaml
```


## 下一步

- 在更复杂任务上运行实验，例如 [`book-flight`](https://miniwob.farama.org/environments/book-flight/)
