import outlines
from outlines.inputs import Chat
from transformers import AutoModelForCausalLM, AutoTokenizer
from pydantic import BaseModel, Field, model_validator
from typing import List, Literal, Optional

class Dosage(BaseModel):
    """Dosage information for medications"""
    text: str = Field(..., description="The dosage information including amount, frequency, and administration instructions")

class Value(BaseModel):
    """Measurement value information"""
    text: str = Field(..., description="The measurement value including units")

class MedicalEntity(BaseModel):
    """Represents an extracted medical entity from text"""
    text: str = Field(..., description="The extracted medical term, condition, medication, or measurement name")
    category: Literal["MEDICAL_CONDITION", "MEDICATION", "MEASUREMENT"] = Field(
        ..., 
        description="The category of the extracted entity"
    )
    dosage: Optional[Dosage] = Field(None, description="Present only when category is MEDICATION")
    value: Optional[Value] = Field(None, description="Present only when category is MEASUREMENT")

    @model_validator(mode='after')
    def validate_category_fields(self):
        """Ensure dosage is present for MEDICATION and value is present for MEASUREMENT"""
        if self.category == "MEDICATION":
            if self.dosage is None:
                raise ValueError("MEDICATION category requires 'dosage' field")
            if self.value is not None:
                raise ValueError("MEDICATION category should not have 'value' field")
        elif self.category == "MEASUREMENT":
            if self.value is None:
                raise ValueError("MEASUREMENT category requires 'value' field")
            if self.dosage is not None:
                raise ValueError("MEASUREMENT category should not have 'dosage' field")
        elif self.category == "MEDICAL_CONDITION":
            if self.dosage is not None or self.value is not None:
                raise ValueError("MEDICAL_CONDITION category should not have 'dosage' or 'value' fields")
        return self


class MedicalExtractionOutput(BaseModel):
    """Root model representing the complete extraction output"""
    entities: List[MedicalEntity] = Field(..., description="List of extracted medical entities")

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

    # Wrapping the model with Outlines for structured generation
    model = outlines.from_transformers(model, tokenizer)

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

    message = Chat([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ])

    result = model(message, output_type=MedicalExtractionOutput, max_new_tokens=200, repetition_penalty=0.5)

    print(result)


if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("--model-id", type=str, default="LiquidAI/LFM2-350M-Extract")
    args = parser.parse_args()
    main(args.model_id)