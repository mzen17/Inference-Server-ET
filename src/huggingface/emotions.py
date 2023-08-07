import torch
from transformers import AutoTokenizer, RobertaForSequenceClassification
def get_emotion(text):
    tokenizer = AutoTokenizer.from_pretrained("SamLowe/roberta-base-go_emotions")
    model = RobertaForSequenceClassification.from_pretrained("SamLowe/roberta-base-go_emotions")

    inputs = tokenizer(text, return_tensors="pt")

    with torch.no_grad():
        logits = model(**inputs).logits

    predicted_class_id = logits.argmax().item()
    model.config.id2label[predicted_class_id]

    return model.config.id2label[predicted_class_id]
