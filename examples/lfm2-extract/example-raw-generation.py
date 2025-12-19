from transformers import AutoModelForCausalLM, AutoTokenizer

def main(
    model_id: str
):
    print("Loading model...")
    # Load model and tokenizer
    model_id = "LiquidAI/LFM2-350M-Extract"
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        device_map="auto",
        dtype="bfloat16",
    #    attn_implementation="flash_attention_2" <- uncomment on compatible GPU
    )
    tokenizer = AutoTokenizer.from_pretrained(model_id)

    # Create message
    system_prompt = """Return data as a JSON object with the following schema:

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
    Output: [{"text": "blood pressure", "category": "MEASUREMENT", "value": {"text": "120/80"}}]"""

    user_prompt = """Extract the medical entities from the following text:
    'The patient was diagnosed with hypertension and prescribed lisinopril 10 mg daily. Her cholesterol level is 200 mg/dL.'"""


    message = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    # Generate answer
    input_ids = tokenizer.apply_chat_template(
        message,
        add_generation_prompt=True,
        return_tensors="pt",
        tokenize=True,
    ).to(model.device)

    output = model.generate(
        input_ids,
        do_sample=False,
        max_new_tokens=1024,
    )

    print(tokenizer.decode(output[0], skip_special_tokens=False))

if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("--model-id", type=str, default="LiquidAI/LFM2-350M-Extract")
    args = parser.parse_args()
    main(args.model_id)