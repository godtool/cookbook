# LFM2 模型微调配方

[English](README.md) | [中文](README_zh.md)


如果你希望提升模型在特定场景中的表现，我们建议对 LFM2 模型进行微调。

本页收集了使用不同技术微调 LFM2 模型的笔记本与示例。

- [文本到文本模型](#文本到文本模型)
- [视觉语言模型](#视觉语言模型)
- 音频模型（敬请期待）

## 文本到文本模型

模型：
- `LFM2.5-1.2B-Base`
- `LFM2.5-1.2B-Instruct`
- `LFM2.5-1.2B-Thinking`
- `LFM2-2.6B-Exp`
- `LFM2-2.6B`
- `LFM2-8B-A1B`
- `LFM2-700M`
- `LFM2-350M`

| 微调技术 | 链接 |
|---|---|
| 继续预训练（CPT）（仅用于 `LFM2.5-1.2B-Base`） | [文本补全预训练](https://colab.research.google.com/drive/10fm7eNMezs-DSn36mF7vAsNYlOsx9YZO?usp=sharing)<br>[跨语言预训练](https://colab.research.google.com/drive/1gaP8yTle2_v35Um8Gpu9239fqbU7UgY8?usp=sharing) |
| 使用 LoRA 的监督微调（SFT） | [使用 TRL](https://colab.research.google.com/drive/1j5Hk_SyBb2soUsuhU0eIEA9GwLNRnElF?usp=sharing)<br>[使用 Unsloth](https://colab.research.google.com/drive/1vGRg4ksRj__6OLvXkHhvji_Pamv801Ss?usp=sharing) |
| 使用 LoRA 的直接偏好优化（DPO） | [使用 TRL](https://colab.research.google.com/drive/1MQdsPxFHeZweGsNx4RH7Ia8lG8PiGE1t?usp=sharing) |
| 使用 LoRA 的组相对策略优化（GRPO） | - 使用 [Unsloth](https://colab.research.google.com/drive/1mIikXFaGvcW4vXOZXLbVTxfBRw_XsXa5?usp=sharing) 或 [TRL](./grpo_for_verifiable_tasks.ipynb) 将非推理模型转为推理模型 <br> - [使用 OpenEnv 与 GRPO 强化浏览器控制任务](../examples/browser-control/README.md) |

## 视觉语言模型

模型：

- `LFM2.5-VL-1.6B`
- `LFM2-VL-3B`
- `LFM2-VL-450M`

| 微调技术 | 链接 |
|---|---|
| 使用 LoRA 的监督微调（SFT） | - [使用 Unsloth 进行 OCR](https://colab.research.google.com/drive/1FaR2HSe91YDe88TG97-JVxMygl-rL6vB?usp=sharing#scrollTo=vITh0KVJ10qX)<br> - [使用 TRL 进行医疗视觉微调](https://colab.research.google.com/drive/10530_jt_Joa5zH2wgYlyXosypq1R7PIz?usp=sharing) <br> - [汽车图像分类示例](../examples/car-maker-identification/README.md) |
