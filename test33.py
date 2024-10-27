import torch
from transformers import pipeline

# Initialize the text-generation pipeline with optimizations
pipe = pipeline(
    "text-generation", 
    model="TinyLlama/TinyLlama-1.1B-Chat-v1.0", 
    torch_dtype=torch.float32,
    device_map="cpu"
)

# Define the chat messages
messages = [
    {
        "role": "system",
        "content": "You are a friendly chatbot who always responds in the style of a pirate",
    },
    {
        "role": "user",
        "content": "How many letter 'r' in the word 'strawberry'?",
    },
]

# Format the messages using the tokenizer's chat template
prompt = pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

# Generate a response with optimized parameters
outputs = pipe(
    prompt, 
    max_new_tokens=50,  # Shorter outputs for faster generation
)

# Print the generated text
print(outputs[0]["generated_text"])

# To execute: python test33.py
