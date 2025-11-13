# # import pandas as pd
# # import requests
# # import json
# #
# # def analyze_nutrition(ingredients, usda_api_key):
# #     api_endpoint = "https://api.nal.usda.gov/fdc/v1/foods/search"
# #     api_params = {"query": ingredients, "api_key": usda_api_key}
# #
# #     response = requests.get(api_endpoint, params=api_params)
# #
# #     if response.status_code == 200:
# #         data = response.json()
# #         # Extract nutrient information from each item
# #         nutrients = []
# #         for item in data["foods"]:
# #             nutrient_info = {
# #                 "description": item["description"],
# #                 "nutrients": item["foodNutrients"]  # Extracting nutrient information only
# #             }
# #             nutrients.append(nutrient_info)
# #         return nutrients
# #     else:
# #         print("Error:", response.text)
# #         return None
# #
# #
# # # Example usage
# # ingredients = ["Carrots, milk, sugar, ghee, cashews, raisins"]
# # usda_api_key = "ehGqisFIV5oBXHjP4htWyAeWrzD0xco2NCaqTjoH"
# # result = analyze_nutrition(ingredients, usda_api_key)
# #
# # data = result[0]
# #
# # # Extract only the nutrient name and its important values
# # important_nutrients = {}
# # for nutrient in data["nutrients"]:
# #     nutrient_name = nutrient["nutrientName"].split(',')[0]
# #     value = nutrient.get("value", None)
# #     if value is not None:
# #         important_nutrients[nutrient_name] = value
# #
# # print(pd.DataFrame(important_nutrients.items()))
# import pandas as pd
# import requests
#
# def analyze_nutrition(ingredient, usda_api_key):
#     api_endpoint = "https://api.nal.usda.gov/fdc/v1/foods/search"
#     api_params = {"query": ingredient, "api_key": usda_api_key}
#
#     response = requests.get(api_endpoint, params=api_params)
#
#     if response.status_code == 200:
#         data = response.json()
#         # Extract nutrient information from each item
#         nutrients = []
#         for item in data["foods"]:
#             nutrient_info = {
#                 "description": item["description"],
#                 "nutrients": item["foodNutrients"]  # Extracting nutrient information only
#             }
#             nutrients.append(nutrient_info)
#         return nutrients
#     else:
#         print("Error:", response.text)
#         return None
#
# # Example usage
# usda_api_key = "ehGqisFIV5oBXHjP4htWyAeWrzD0xco2NCaqTjoH"
# ingredients = ["Coriander","flour"]
# # result = analyze_nutrition(ingredients, usda_api_key)
# # print(result[0])
# important_nutrients = {}
# for ingredient in ingredients:
#     result = analyze_nutrition(ingredient, usda_api_key)
#     if result:
#         result = result[0]  # Ensure there is at least one result before accessing its elements
#         for nutrient in result["nutrients"]:
#             nutrient_name = nutrient["nutrientName"].split(',')[0]
#             value = nutrient.get("value", None)
#             if value is not None:
#                 # If the nutrient key doesn't exist, initialize it with 0
#                 if nutrient_name not in important_nutrients:
#                     important_nutrients[nutrient_name] = 0
#                 important_nutrients[nutrient_name] += value
#
# # Create a DataFrame from the collected nutrient data
# df = pd.DataFrame(important_nutrients.items(), columns=["Nutrient", "Total Value"])
# print(df)

# import requests
#
# query = '1lb brisket and fries'
# api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(query)
# key="zBfZ7IKBT2H35WjLi5B7vA==sBRJ7LmMh3CP9Vs4"
# response = requests.get(api_url, headers={'X-Api-Key': key})
# if response.status_code == requests.codes.ok:
#     print(response.text)
# else:
#     print("Error:", response.status_code, response.text)
# # t=zBfZ7IKBT2H35WjLi5B7vA==sBRJ7LmMh3CP9Vs4

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa

def generate_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()
    return private_key, public_key

def sign_message(private_key, message):
    signature = private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature

def verify_signature(public_key, signature, message):
    try:
        public_key.verify(
            signature,
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        print("Signature verified: Valid signature for the message.")
        return True
    except:
        print("Signature verification failed: Invalid signature for the message.")
        return False

if __name__ == "__main__":
    # Generate key pair
    private_key, public_key = generate_key_pair()

    # Message to be signed
    message = b"Hello, world!"

    # Sign the message
    signature = sign_message(private_key, message)

    # Verify the signature
    verify_signature(public_key, signature, message)
