from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("tiiuae/falcon-mamba-7b")
model = AutoModelForCausalLM.from_pretrained("tiiuae/falcon-mamba-7b")

input_text = "Question: How many hours in one day? Answer: "
input_ids = tokenizer(input_text, return_tensors="pt").input_ids

outputs = model.generate(input_ids)
print(tokenizer.decode(outputs[0]))

# Falcon Mamba
# python test31.py