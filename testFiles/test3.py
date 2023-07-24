import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("Salesforce/xgen-7b-8k-inst", trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained("Salesforce/xgen-7b-8k-inst", torch_dtype=torch.bfloat16)

header = (
    "A chat between a curious human and an artificial intelligence assistant. "
    "The assistant gives helpful, detailed, and polite answers to the human's questions.\n\n"
)
article = "C:\\Users\\Gianne Bacay\\Desktop\\PROJECT_H.A.R.A.Y.A\\news\\result.txt"  # insert a document here
prompt = f"### Human: Please summarize the following article.\n\n{article}.\n###"

inputs = tokenizer(header + prompt, return_tensors="pt")
sample = model.generate(**inputs, do_sample=True, max_new_tokens=2048, top_k=100, eos_token_id=50256)
output = tokenizer.decode(sample[0])
print(output.strip().replace("Assistant:", ""))


#_______________pip install llama
#________________python test3.py
#________________Remarks: Fail