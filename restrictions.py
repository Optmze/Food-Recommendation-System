
# import streamlit as st
# import pandas as pd
# import random
#
# # Load data
# data = pd.read_csv("foodsfinal3.csv")
#
# # Define the desired order of course types
# desired_order = ['Breakfast', 'Lunch', 'Side Dish', 'Snacks', 'Dinner']
#
#
# # Function to get recipe recommendations based on dietary restrictions and group by course
# def get_recipe_recommendations(dietary_restrictions, dataset=data):
#     # Filter recipes based on dietary restrictions
#     restricted_recipes = dataset.copy()
#     for restriction in dietary_restrictions:
#         restricted_recipes = restricted_recipes.loc[
#             restricted_recipes[restriction] <= dietary_restrictions[restriction]]
#
#     # Group recipes by course
#     grouped_recipes = restricted_recipes.groupby('Course')['RecipeName'].apply(list).reset_index()
#     for index, row in grouped_recipes.iterrows():
#         if len(row['RecipeName']) > 5:
#             grouped_recipes.at[index, 'RecipeName'] = random.sample(row['RecipeName'], 5)
#
#     return grouped_recipes
#
#
# # Main function to create Streamlit app
# def main():
#     st.title("Recipe Recommendations Based on Dietary Restrictions")
#
#     # Select disease
#     selected_disease = st.selectbox("Select Disease:",
#                                     ["Choose an option", "Heart Disease", "Renal Disease", "Diabetes"], index=0)
#
#     if selected_disease != "Choose an option":
#         # Set dietary restrictions based on selected disease
#         dietary_restrictions = {}
#         if selected_disease == "Heart Disease":
#             dietary_restrictions.update({"cholesterol_mg": 0.5, "fat_total_g": 5})
#             recommendations = get_recipe_recommendations(dietary_restrictions)
#         elif selected_disease == "Renal Disease":
#             dietary_restrictions.update({"sodium_mg": 15, "potassium_mg": 50})
#             recommendations = get_recipe_recommendations(dietary_restrictions)
#         elif selected_disease == "Diabetes":
#             dietary_restrictions.update({"sugar_g": 5, "carbohydrates_total_g": 25})
#             recommendations = \
#             data[(data['Diet'] == 'Diabetic Friendly') | (data['Diet'] == 'Sugar Free Diet')].groupby('Course')[
#                 'RecipeName'].apply(list).reset_index()
#             for index, row in recommendations.iterrows():
#                 if len(row['RecipeName']) > 5:
#                     recommendations.at[index, 'RecipeName'] = random.sample(row['RecipeName'], 5)
#
#         # Display recommended recipes grouped by course
#         if not recommendations.empty:
#             st.subheader("Recommended Recipes:")
#             for course in desired_order:
#                 if course in recommendations['Course'].values:
#                     st.subheader(course)
#                     recipes = recommendations[recommendations['Course'] == course]['RecipeName'].iloc[0]
#                     for recipe in recipes:
#                         recipe_details = data[data['RecipeName'] == recipe].iloc[0]
#                         with st.expander(f"{recipe} - {recipe_details['Cuisine']}"):
#                             st.subheader("Ingredients:")
#                             st.write(recipe_details['Ingredients'])
#                             st.markdown("<p style='font-size:20px'><b>Prep Time:</b> " + f"{recipe_details['PrepTimeInMins']} minutes</p>", unsafe_allow_html=True)
#                             st.markdown(f"<p style='font-size:20px'><b>Prep Time:</b> {recipe_details['PrepTimeInMins']} minutes</p>",unsafe_allow_html=True)
#                             st.markdown(f"<p style='font-size:20px'><b>Cook Time:</b> {recipe_details['CookTimeInMins']} minutes</p>",unsafe_allow_html=True)
#                             st.markdown(f"<p style='font-size:20px'><b>Servings:</b> {recipe_details['Servings']}</p>",unsafe_allow_html=True)
#                             st.markdown(f"<p style='font-size:20px'><b>Diet:</b> {recipe_details['Diet']}</p>",unsafe_allow_html=True)
#                             st.subheader("Instructions:")
#                             st.write(recipe_details['Instructions'])
#                             st.subheader("Calories:")
#                             st.write(recipe_details['calories'])
#                             st.subheader("Total Fat:")
#                             st.write(f"{recipe_details['fat_total_g']} g")
#                             st.subheader("Protein:")
#                             st.write(f"{recipe_details['protein_g']} g")
#                             st.subheader("Cholesterol:")
#                             st.write(f"{recipe_details['cholesterol_mg']} mg")
#                             st.subheader("Total Carbohydrates:")
#                             st.write(f"{recipe_details['carbohydrates_total_g']} g")
#                             st.subheader("Fiber:")
#                             st.write(f"{recipe_details['fiber_g']} g")
#                             st.subheader("Sugar:")
#                             st.write(f"{recipe_details['sugar_g']} g")
#         else:
#             st.write("No recipes found matching the selected dietary restrictions.")
#
#
# if __name__ == "__main__":
#     main()
#
# import streamlit as st
# import requests
# from bs4 import BeautifulSoup
#
# def get_images_links(searchTerm):
#     try:
#         searchUrl = "https://www.google.com/search?q={}&site=webhp&tbm=isch".format(searchTerm)
#         d = requests.get(searchUrl).text
#         soup = BeautifulSoup(d, 'html.parser')
#
#         img_tags = soup.find_all('img')
#
#         imgs_urls = []
#         for img in img_tags:
#             if img['src'].startswith("http"):
#                 imgs_urls.append(img['src'])
#
#         return imgs_urls[0] if imgs_urls else None
#     except:
#         return None
#
# search_term = "Tomato rice"
# image_url = get_images_links(search_term)
#
# if image_url:
#     st.image(image_url, caption='Image for Recipe: {}'.format(search_term))
# else:
#     st.error("Image not found for {}".format(search_term))
import streamlit as st
import pandas as pd
import random
import requests
from bs4 import BeautifulSoup
print("DEBUG: Data loaded successfully.")
# Load data
data = pd.read_csv("foodsfinal3.csv")

# Define the desired order of course types
desired_order = ['Breakfast', 'Lunch', 'Side Dish', 'Snacks', 'Dinner']

# Function to get recipe recommendations based on dietary restrictions and group by course
def get_recipe_recommendations(dietary_restrictions, dataset=data):
    # Filter recipes based on dietary restrictions
    restricted_recipes = dataset.copy()
    for restriction in dietary_restrictions:
        restricted_recipes = restricted_recipes.loc[
            restricted_recipes[restriction] <= dietary_restrictions[restriction]]

    # Group recipes by course
    grouped_recipes = restricted_recipes.groupby('Course')['RecipeName'].apply(list).reset_index()
    for index, row in grouped_recipes.iterrows():
        if len(row['RecipeName']) > 5:
            grouped_recipes.at[index, 'RecipeName'] = random.sample(row['RecipeName'], 5)

    return grouped_recipes

# Function to scrape image URL from Google Images
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
def display_disease_description(disease):
    if disease == "Heart Disease":
        st.info("Manage your cholesterol and fat intake with heart-healthy recipes.")
    elif disease == "Renal Disease":
        st.info("Control your sodium and potassium levels with kidney-friendly meals.")
    elif disease == "Diabetes":
        st.info("Balance your sugar and carbohydrate intake with diabetic-friendly dishes.")

# Main function to create Streamlit app
def main():
    st.title("🍲Recipe Recommendations Based on Dietary Restrictions")
    st.markdown("<hr>", unsafe_allow_html=True)
    # Select disease
    selected_disease = st.selectbox("Select Disease:",
                                    ["Choose an option", "Heart Disease", "Renal Disease", "Diabetes"], index=0)
    if selected_disease != "Choose an option":
        # Set dietary restrictions based on selected disease
        dietary_restrictions = {}
        if selected_disease == "Heart Disease":
            dietary_restrictions.update({"cholesterol_mg": 0.5, "fat_total_g": 5})
            recommendations = get_recipe_recommendations(dietary_restrictions)
        elif selected_disease == "Renal Disease":
            dietary_restrictions.update({"sodium_mg": 15, "potassium_mg": 50})
            recommendations = get_recipe_recommendations(dietary_restrictions)
        elif selected_disease == "Diabetes":
            dietary_restrictions.update({"sugar_g": 5, "carbohydrates_total_g": 25})
            recommendations = \
                data[(data['Diet'] == 'Diabetic Friendly') | (data['Diet'] == 'Sugar Free Diet')].groupby('Course')[
                    'RecipeName'].apply(list).reset_index()
            for index, row in recommendations.iterrows():
                if len(row['RecipeName']) > 5:
                    recommendations.at[index, 'RecipeName'] = random.sample(row['RecipeName'], 5)

        # Display recommended recipes grouped by course
        if not recommendations.empty:
            st.markdown("<hr>", unsafe_allow_html=True)
            st.subheader("Recommended Recipes:")
            display_disease_description(selected_disease)
            st.markdown("<hr>", unsafe_allow_html=True)
            for course in desired_order:
                if course in recommendations['Course'].values:
                    st.subheader(course)
                    recipes = recommendations[recommendations['Course'] == course]['RecipeName'].iloc[0]
                    for recipe in recipes:
                        recipe_details = data[data['RecipeName'] == recipe].iloc[0]
                        with st.expander(f"{recipe} - {recipe_details['Cuisine']}"):
                            st.image(get_image_url(recipe), caption="Image for Recipe: {}".format(recipe))
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
                    st.markdown("<hr>", unsafe_allow_html=True)
        else:
            st.write("No recipes found matching the selected dietary restrictions.")

if __name__ == "__main__":
    main()
