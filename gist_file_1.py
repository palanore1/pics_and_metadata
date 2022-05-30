from PIL import Image
from IPython.display import display
import random
import json
import os

from trait_rarity import *


# Classify Traits

face_files = {"White": "face1", "Black": "face2"}

ears_files = {
    "No Earring": "ears1",
    "Left Earring": "ears2",
    "Right Earring": "ears3",
    "Two Earrings": "ears4",
}

eyes_files = {
    "Regular": "eyes1",
    "Small": "eyes2",
    "Rayban": "eyes3",
    "Hipster": "eyes4",
    "Focused": "eyes5",
}

hair_files = {
    "Up Hair": "hair1",
    "Down Hair": "hair2",
    "Mohawk": "hair3",
    "Red Mohawk": "hair4",
    "Orange Hair": "hair5",
    "Bubble Hair": "hair6",
    "Emo Hair": "hair7",
    "Thin Hair": "hair8",
    "Bald": "hair9",
    "Blonde Hair": "hair10",
    "Caret Hair": "hair11",
    "Pony Tails": "hair12",
}


mouth_files = {
    "Black Lipstick": "m1",
    "Red Lipstick": "m2",
    "Big Smile": "m3",
    "Smile": "m4",
    "Teeth Smile": "m5",
    "Purple Lipstick": "m6",
}

nose_files = {"Nose": "n1", "Nose Ring": "n2"}

# Generate Traits

TOTAL_IMAGES = 100

all_images = []


def create_new_image():
    new_image = {}

    # For each trait category, slect a random trait
    new_image["Face"] = random.choices(face, face_weights)[0]
    new_image["Ears"] = random.choices(ears, ears_weights)[0]
    new_image["Eyes"] = random.choices(eyes, eyes_weights)[0]
    new_image["Hair"] = random.choices(hair, hair_weights)[0]
    new_image["Mouth"] = random.choices(mouth, mouth_weights)[0]
    new_image["Nose"] = random.choices(nose, nose_weights)[0]

    if new_image in all_images:
        return create_new_image()
    else:
        return new_image


for i in range(TOTAL_IMAGES):
    new_trait_image = create_new_image()
    all_images.append(new_trait_image)


# Returns True if all images are unique


def all_images_unique(all_images):
    seen = list()
    return not any(i in seen or seen.append(i) for i in all_images)


print("Are all images unique ?", all_images_unique(all_images))
# Add token Id to each image
i = 0
for item in all_images:
    item["tokenId"] = i
    i += 1

print(all_images)

## Generate Metadata

# Get trait counts

face_count = {}
for item in face:
    face_count[item] = 0

ears_count = {}
for item in ears:
    ears_count[item] = 0

eyes_count = {}
for item in eyes:
    eyes_count[item] = 0

hair_count = {}
for item in hair:
    hair_count[item] = 0

mouth_count = {}
for item in mouth:
    mouth_count[item] = 0

nose_count = {}
for item in nose:
    nose_count[item] = 0


for image in all_images:
    face_count[image["Face"]] += 1
    ears_count[image["Ears"]] += 1
    eyes_count[image["Eyes"]] += 1
    hair_count[image["Hair"]] += 1
    mouth_count[image["Mouth"]] += 1
    nose_count[image["Nose"]] += 1

print("Face\nEars\nEyes\nHair\nMouth\nNose")
print(face_count)
print(ears_count)
print(eyes_count)
print(hair_count)
print(mouth_count)
print(nose_count)


os.mkdir(f"./images")

for item in all_images:

    im1 = Image.open(f'./face_parts/face/{face_files[item["Face"]]}.png').convert(
        "RGBA"
    )
    im2 = Image.open(f'./face_parts/eyes/{eyes_files[item["Eyes"]]}.png').convert(
        "RGBA"
    )
    im3 = Image.open(f'./face_parts/ears/{ears_files[item["Ears"]]}.png').convert(
        "RGBA"
    )
    im4 = Image.open(f'./face_parts/hair/{hair_files[item["Hair"]]}.png').convert(
        "RGBA"
    )
    im5 = Image.open(f'./face_parts/mouth/{mouth_files[item["Mouth"]]}.png').convert(
        "RGBA"
    )
    im6 = Image.open(f'./face_parts/nose/{nose_files[item["Nose"]]}.png').convert(
        "RGBA"
    )

    # Create each composite
    com1 = Image.alpha_composite(im1, im2)
    com2 = Image.alpha_composite(com1, im3)
    com3 = Image.alpha_composite(com2, im4)
    com4 = Image.alpha_composite(com3, im5)
    com5 = Image.alpha_composite(com4, im6)

    # Convert to RGB
    rgb_im = com5.convert("RGB")
    file_name = str(item["tokenId"]) + ".jpeg"
    rgb_im.save("./images/" + file_name)


# Generate all_traits.json
os.mkdir(f"./metadata")

METADATA_FILE_NAME = "./metadata/all-traits.json"
with open(METADATA_FILE_NAME, "w") as outfile:
    json.dump(all_images, outfile, indent=4)
