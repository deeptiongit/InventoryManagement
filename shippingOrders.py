from transformers import AutoTokenizer, BitsAndBytesConfig, Gemma3ForCausalLM
import torch
import json
import os

model_id = "google/gemma-3-1b-it"

quantization_config = BitsAndBytesConfig(load_in_8bit=True)

model = Gemma3ForCausalLM.from_pretrained(
    model_id,
    quantization_config=quantization_config,
    dtype=torch.bfloat16,
    device_map="auto"
).eval()

tokenizer = AutoTokenizer.from_pretrained(model_id)



SCHEMA = """
Return JSON in this exact structure:

{
  "Order ID": "string",

    Shipping Details:{
        "Ship Name": "string"
        "Ship Address": "string"
        "Ship City": "string"
        "Ship Region": "string"
        "Ship Postal Code": "string"
        "Ship Country": "string"
    }
    "Customer Details":{
    
        "Customer ID": "string"
        "Customer Name": "string"
    }
    "Employee Details":{
        "Employee Name": "string"
    }
    "Shipper Details":{
        "Shipper ID": "string"
        "Shipper Name": "string"
    }
    "Order Details":{
        "Order Date": "string"
        "Shipped Date": "string"
    }
    Products:[
    {
        "Product": "string"
        "Quantity": 0.0
        "Unit Price": 0.0
        "Total": 0.0
    }
    ]


}

Rules:
- Always output valid JSON.
- No explanations.
- Products must always be a list.
"""

def extract_text_from_pdf(pdf_path):
    import pdfplumber
    text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    return text



def extract(invoice_text):
    messages = [
        {
            "role": "system",
            "content": [{"type": "text", "text": f"You are an invoice extraction agent.\n\n{SCHEMA}"}]
        },
        {
            "role": "user",
            "content": [{"type": "text", "text": f"Extract JSON from this invoice:\n\n{invoice_text}"}]
        }
    ]


    inputs = tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        return_tensors="pt",
        tokenize=True,
        return_dict=True,
    ).to(model.device)


    with torch.inference_mode():
        output = model.generate(
            **inputs,
            max_new_tokens=300,
            do_sample=False,
            temperature=0.0
        )

    decoded = tokenizer.decode(output[0][inputs['input_ids'].shape[-1]:], skip_special_tokens=True)



    start = decoded.find("{")
    end = decoded.rfind("}")

    json_str = decoded[start:end+1]

    try:
        return json.loads(json_str)
    except:
        return json_str


INPUT_DIR = "/kaggle/input/company-documents-dataset/CompanyDocuments/Shipping Orders"
OUTPUT_DIR  = "/home/Shipping-Orders-jsons"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

for file in os.listdir(INPUT_DIR):
  print(f"Extracting file , {file}")
  text = extract_text_from_pdf(os.path.join(INPUT_DIR, file))
  json_obj = extract(text)
  output_file = os.path.join(OUTPUT_DIR, file)
  output_file = output_file.replace("pdf","json")
  print(f"Writing file , {output_file}")
  with open(output_file, 'w') as f:
    if isinstance(json_obj, dict):
        json.dump(json_obj, f, indent=2, ensure_ascii=False)
        print(f"Created , {output_file}")
    else:
        f.write(json_obj)

print("Done")