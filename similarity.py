import streamlit as st
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import requests
from bs4 import BeautifulSoup

def get_nutritional_values(query):
    api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(query)
    key = "Dpugd2jNHFDbh74TK4i9Zg==fl7dlBv8p8a8lIC9"
    response = requests.get(api_url, headers={'X-Api-Key': key})

    if response.status_code == requests.codes.ok:
        return response.json()
    else:
        print("Error:", response.status_code, response.text)
        return None

def sum_nutritional_values(recipe_nutrition):
    total_nutrition = {
        "calories": 0,
        "serving_size_g": 0,
        "fat_total_g": 0,
        "fat_saturated_g": 0,
        "protein_g": 0,
        "sodium_mg": 0,
        "potassium_mg": 0,
        "cholesterol_mg": 0,
        "carbohydrates_total_g": 0,
        "fiber_g": 0,
        "sugar_g": 0
    }

    for ingredient_nutrition in recipe_nutrition:
        for key, value in ingredient_nutrition.items():
            if key != "name":  # Skip the name field
                total_nutrition[key] += value

    return total_nutrition

def get_and_sum_nutritional_values(query):
    response = get_nutritional_values(query)
    if response:
        total_nutrition = sum_nutritional_values(response)
        return total_nutrition
    else:
        return None

def get_image_url(recipe_name):
    try:
        search_url = "https://www.google.com/search?q={}&tbm=isch".format(recipe_name)
        response = requests.get(search_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tags = soup.find_all('img')
        for img in img_tags:
            if img['src'].startswith("http"):
                return img['src']
    except:
        pass
    return None


data = pd.read_csv("foodsfinal2.csv")
selected_columns = ["calories", "fat_total_g", "protein_g", "carbohydrates_total_g", "fiber_g", "sugar_g", "cholesterol_mg"]
X = data[selected_columns]
k = 5  # Number of neighbors
knn = NearestNeighbors(n_neighbors=k, algorithm='auto').fit(X)


def recommend_similar_recipes(selected_recipe):
    # Find nutritional values for the selected recipe
    data["RecipeName"] = data["RecipeName"].tolist()
    selected_recipe_nutrition = data[data["RecipeName"] == selected_recipe][selected_columns]

    # If nutritional values are not found in the dataset, retrieve them using API
    if len(selected_recipe_nutrition) == 0:
        selected_recipe_nutrition = get_and_sum_nutritional_values(selected_recipe)
        selected_recipe_nutrition = pd.DataFrame(selected_recipe_nutrition, index=[0])[selected_columns]

    # If still nutritional values are not found, return empty list
    if len(selected_recipe_nutrition) == 0:
        st.write(f"No nutritional information found for '{selected_recipe}'.")
        return []

    # Find similar recipes using KNN
    distances, indices = knn.kneighbors(selected_recipe_nutrition)
    similar_indices = indices[0]
    similar_recipes = data.iloc[similar_indices]["RecipeName"].tolist()
    return similar_recipes
    return top_similar_recipes

# Main function to create Streamlit app
def main():
    st.title("Recipe Similarity Recommender🍽️")
    st.info("""This app recommends similar recipes based on their nutritional values.
    \n Enter a dish below to get started.""")
    # Input field for user to enter a dish
    selected_recipe = st.text_input("Enter a dish:", "")

    if st.button("Find Similar Recipes"):
        st.markdown("<hr>", unsafe_allow_html=True)
        recommendations=recommend_similar_recipes(selected_recipe)
        nutritional_values = get_and_sum_nutritional_values(selected_recipe)
        if nutritional_values:
            # Display nutritional values within an expander
            with st.expander("Nutritional Values for Selected Dish"):
                image_url = get_image_url(selected_recipe)
                if image_url:
                    st.image(image_url, caption="Image for Recipe: {}".format(selected_recipe))
                for key, value in nutritional_values.items():
                    st.markdown(f"<p style='font-size:18px'><b>{key}</b>: {value}</p>",unsafe_allow_html=True)

        # Display similar recipes
        st.markdown("<hr>", unsafe_allow_html=True)
        st.subheader(f"🍛🔁 Recipes similar to '{selected_recipe}':")
        for recommendation in recommendations:
            recipe_details = data[data["RecipeName"] == recommendation].iloc[0]
            with st.expander(f"{recommendation} - {recipe_details['Cuisine']}"):
                st.image(get_image_url(recommendation), caption="Image for Recipe: {}".format(recommendation))
                st.subheader("Ingredients:")
                st.write(recipe_details['Ingredients'])
                st.markdown(f"<p style='font-size:20px'><b>Prep Time:</b> {recipe_details['PrepTimeInMins']} minutes</p>",unsafe_allow_html=True)
                st.markdown(f"<p style='font-size:20px'><b>Cook Time:</b> {recipe_details['CookTimeInMins']} minutes</p>",unsafe_allow_html=True)
                st.markdown(f"<p style='font-size:20px'><b>Servings:</b> {recipe_details['Servings']}</p>",unsafe_allow_html=True)
                st.markdown(f"<p style='font-size:20px'><b>Diet:</b> {recipe_details['Diet']}</p>",unsafe_allow_html=True)
                st.subheader("Instructions:")
                st.write(recipe_details['Instructions'])
                st.subheader("Calories:")
                st.write(recipe_details['calories'])
                st.subheader("Total Fat:")
                st.write(f"{recipe_details['fat_total_g']} g")
                st.subheader("Protein:")
                st.write(f"{recipe_details['protein_g']} g")
                st.subheader("Cholesterol:")
                st.write(f"{recipe_details['cholesterol_mg']} mg")
                st.subheader("Total Carbohydrates:")
                st.write(f"{recipe_details['carbohydrates_total_g']} g")
                st.subheader("Fiber:")
                st.write(f"{recipe_details['fiber_g']} g")
                st.subheader("Sugar:")
                st.write(f"{recipe_details['sugar_g']} g")
        if(len(recommendations)==0):
            st.warning("No similar dishes found")

if __name__ == "__main__":
    main()
