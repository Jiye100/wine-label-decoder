from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch

# Trying out different pretrained model to see which one is best for wine description generation
# Uncomment the best model and use that one

# Google flan T5 base model
# model_name = "google/flan-t5-base"
# tokenizer = T5Tokenizer.from_pretrained(model_name)
# model = T5ForConditionalGeneration.from_pretrained(model_name)

# Google flan T5 xl model
model_name = "google/flan-t5-xl"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name, device_map="auto", torch_dtype=torch.float16)


def generate_wine_description(name, region):

    # We need to give a prompt for the input for the generative description model
    # Try out various prompt to see which one gives the best one
    # Uncomment the best prompt to use it

    # prompt = f"Generate a wine description: {name}"

    # prompt = (
    #     f"Write a detailed and elegant wine description for '{name}', "
    #     f"a wine from {region}. Include tasting notes, aroma, and style."
    # )

    # prompt = (
    #     f"Write a detailed information wine description for '{name}', "
    #     f"a wine from {region}. Include aging, taste, aroma, style, mouthfeel, appearance, and food pairing if possible."
    # )

    prompt = (
        f"Write a professional wine description for '{name}', a wine from {region}. "
        "Include grape varietals, tasting notes, mouthfeel, finish, food pairings, "
        "serving temperature, and aging potential."
    )

    # Run the model here
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids
    outputs = model.generate(
      input_ids,
      max_length=500,
      min_length=50, # How long do you want to generate a wine description
      num_beams=4,
      no_repeat_ngram_size=3,
      repetition_penalty=2.5,
      early_stopping=True
    )
    description = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return description

def generate_wine_law(grape, region, vintage):
    prompt = (
        """Explain the labeling requirements for a wine labeled as a 2020 Pinot Noir from the Willamette Valley AVA. Grape law: 0.75, Region law: 0.85, Vintage law: 0.85

          - The wine must contain at least 75% Pinot Noir grapes.
          - At least 85% of the grapes must be grown in that AVA.
          - At least 85% of the grapes must be harvested in that year.

          """
          """Explain the labeling requirements for a wine labeled as a 2023 Merlot from New Zealand. Grape law: 0.85, Region law: 0.85, Vintage law: 0.85

          - The wine must contain at least 85% Merlot grapes.
          - At least 85% of the grapes must be grown in that region.
          - At least 85% of the grapes must be harvested in that year.

          """
        f"Explain the labeling requirements for a wine labeled as a {vintage} {grape} from the {region}. Grape law: 0.85, Region law: 0.85, Vintage law: 0.85"
    )

    # Run the model here
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids
    outputs = model.generate(
      input_ids,
      max_length=500,
      min_length=50, # How long do you want to generate a wine description
      num_beams=4,
      no_repeat_ngram_size=3,
      repetition_penalty=2.5,
      early_stopping=True
    )
    description = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return description


# Uncomment this and run this file to specifically testing generative description code
# print(generate_wine_description("Château Margaux 2015", "Bordeaux, France"))
print(generate_wine_law("Cabernet Sauvignon", "Californian AVA","2022"))
