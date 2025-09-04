#  0: no emotion, 1: anger, 2: disgust, 3: fear, 4: happiness, 5: sadness, 6: surprise

# Use a pipeline as a high-level helper
from transformers import pipeline
import json
from  data_loader import data_loader


from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer

model_name = "PrompTart/m2m100_418M_PTT_en_ko"
tokenizer = M2M100Tokenizer.from_pretrained(model_name)
model = M2M100ForConditionalGeneration.from_pretrained(model_name)

# Tokenize and generate translation
tokenizer.src_lang = "en"


# translator = pipeline("translation", model="Helsinki-NLP/opus-mt-en-ko")
file_path = 'dialogues_dataset.json'

dl = data_loader()
sentiment_pair = dl.load_sentiment_data(file_path)
# Translate text
# with open('dialogues_dataset.json', 'r', encoding='utf-8') as file:
#     text = file.read()

new_pair = {"Conversation" : []}

for txt, label in sentiment_pair:
    encoded = tokenizer(txt, return_tensors="pt", padding=True)
    generated_tokens = model.generate(**encoded, forced_bos_token_id=tokenizer.get_lang_id("ko")).to('cuda')
    outputs = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
    
    print(f"Original: {txt} | Translated: {outputs[0]} | Label: {label}")
    new_pair["Conversation"].append( {"text":outputs[0], "SpeakerEmotionTarget":label} )

with open('translated_dataset.json', 'w', encoding='utf-8') as f:
    json.dump(new_pair, f, ensure_ascii=False, indent=4)