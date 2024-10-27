import torch
from transformers import LlamaForCausalLM, LlamaTokenizer

# Hugging Face model_path
model_path = 'psmathur/orca_mini_3b'
tokenizer = LlamaTokenizer.from_pretrained(model_path)
model = LlamaForCausalLM.from_pretrained(
    model_path, torch_dtype=torch.float32, offload_folder="offload"
)

# Generate text function
def generate_text(system, instruction, input=None):
    if input:
        prompt = f"### System:\n{system}\n\n### User:\n{instruction}\n\n### Input:\n{input}\n\n### Response:\n"
    else:
        prompt = f"### System:\n{system}\n\n### User:\n{instruction}\n\n### Response:\n"

    tokens = tokenizer.encode(prompt)
    tokens = torch.LongTensor(tokens).unsqueeze(0)

    instance = {'input_ids': tokens, 'top_p': 1.0, 'temperature': 0.7, 'generate_len': 1024, 'top_k': 50}

    length = len(tokens[0])
    with torch.no_grad():
        rest = model.generate(
            input_ids=tokens,
            max_length=length + instance['generate_len'],
            use_cache=True,
            do_sample=True,
            top_p=instance['top_p'],
            temperature=instance['temperature'],
            top_k=instance['top_k']
        )
    output = rest[0][length:]
    string = tokenizer.decode(output, skip_special_tokens=True)
    return f'[!] Response: {string}'

system = 'You are an AI assistant that follows instructions extremely well. Help as much as you can.'

def main():
    print("Ready!")
    while True:
        user_input = input("User: ")
        if user_input == "exit":
            break
        res = generate_text(system, user_input)
        print("Orca:", res)

if __name__ == "__main__":
    main()
    
# Orca Mini 3B
# python test32.py