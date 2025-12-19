# Evaluate and fine-tune LFM2-Extract on semi-medical data

## Test various models without structured output generation

```
uv run example-raw-generation.py --model-id LFM2-1.2B-Extract
uv run example-raw-generation.py --model-id LFM2-700M
```

## Test various model with structured output generation

```
uv run example-structured-generation.py --model-id LFM2-1.2B-Extract
uv run example-structured-generation.py --model-id LFM2-700M
```

## Test things work with the GGUF checkpoints and llama.cpp

```
uv run example-with-llama-cpp.py --model-id LFM2-1.2B-Extract
uv run example-with-llama-cpp.py --model-id LFM2-700M
```

### Attention!
Make sure you install the llama.cpp build that is optimized for your backend. For example,
for my Macbook this is the install command.

```
uv add llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/metal
```

To find the right command for your platform [see these instructions](https://github.com/abetlen/llama-cpp-python?tab=readme-ov-file#supported-backends).


## Example inputs

```
Input: I have diabetes and take metformin 500 mg twice a day.
Output: [ { "text": "diabetes", "category": "MEDICAL_CONDITION" }, { "text": "metformin", "category": "MEDICATION", "dosage": { "text": "500 mg twice a day" } } ]

Input: My blood pressure was 120/80.
Output: [ { "text": "blood pressure", "category": "MEASUREMENT", "value": { "text": "120/80" } } ]
```

## Systemm prompt

```
Return data as a JSON object with the following schema:

The output should be an array of objects. Each object represents an extracted medical entity and must contain:

1. "text" (string, required): The extracted medical term, condition name, medication name, or measurement name
2. "category" (string, required): One of "MEDICAL_CONDITION", "MEDICATION", or "MEASUREMENT"
3. Additional fields based on category:
   - If category is "MEDICATION": include "dosage" object with "text" field containing dosage information
   - If category is "MEASUREMENT": include "value" object with "text" field containing the measurement value and units
   - If category is "MEDICAL_CONDITION": no additional fields required

Schema structure:
[
  {
    "text": "string",
    "category": "MEDICAL_CONDITION" | "MEDICATION" | "MEASUREMENT",
    "dosage": {  // only for MEDICATION
      "text": "string"
    },
    "value": {  // only for MEASUREMENT
      "text": "string"
    }
  }
]

Examples:
Input: "I have diabetes and take metformin 500 mg twice a day."
Output: [{"text": "diabetes", "category": "MEDICAL_CONDITION"}, {"text": "metformin", "category": "MEDICATION", "dosage": {"text": "500 mg twice a day"}}]

Input: "My blood pressure was 120/80."
Output: [{"text": "blood pressure", "category": "MEASUREMENT", "value": {"text": "120/80"}}]
```

## TODOs

- [x] Vibe check different models
    - [x] LFM2-1.2B-Extract
    - [x] LFM2-700M
- [x] Add structured generation
- [ ] Evaluate on 50 samples
- [ ] Generate a training/eval dataset for fine-tuning
- [ ] Fine-tune