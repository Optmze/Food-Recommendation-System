import streamlit as st
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import random
from bs4 import BeautifulSoup
import requests

df = pd.read_csv('foodsfinal2.csv')

def get_images_links(searchTerm):
    try:
        searchUrl = "https://www.google.com/search?q={}&site=webhp&tbm=isch".format(searchTerm)
        d = requests.get(searchUrl).text
        soup = BeautifulSoup(d, 'html.parser')

        img_tags = soup.find_all('img')

        imgs_urls = []
        for img in img_tags:
            if img['src'].startswith("http"):
                imgs_urls.append(img['src'])

        return(imgs_urls[0])
    except:
        return Not_found_link

def get_meal_recommendations(calories, meal_type, num_recommendations=1):
    meal_df = df[df['Course'] == meal_type]
    nn = NearestNeighbors(n_neighbors=len(meal_df))
    nn.fit(meal_df[['calories', 'carbohydrates_total_g', 'fat_total_g', 'protein_g']])
    distances, indices = nn.kneighbors([[calories, 0, 0, 0]])
    recommendations = meal_df.iloc[random.choice(indices[0])]

    total_calories = recommendations['calories']
    if total_calories > calories:
        return None
    return recommendations


def display_bmi(bmi):
    st.header('BMI CALCULATOR')
    color_codes = {
        'Underweight': 'blue',
        'Normal': 'green',
        'Overweight': 'orange',
        'Obesity': 'red'
    }
    if bmi < 18.5:
        category = 'Underweight'
    elif bmi < 25:
        category = 'Normal'
    elif bmi < 30:
        category = 'Overweight'
    else:
        category = 'Obesity'
    category_color = color_codes.get(category, 'black')
    bmi_html = f'<p style="font-size: 35px">{bmi:.1f} kg/m²</p>'
    st.markdown(bmi_html, unsafe_allow_html=True)
    category_html = f'<p style="font-size: 25px; color: {category_color};">{category}</p>'
    st.markdown(category_html, unsafe_allow_html=True)

    st.markdown(
        """
        Healthy BMI range: 18.5 kg/m² - 25 kg/m².
        """)

def main():
    st.title("🍚Diet Recommendation System")
    st.info("This app utilizes BMI calculation and calorie estimation to suggest personalized meal plans for weight management goals")
    with st.form("user_input_form"):
        age = st.number_input("Age", min_value=1, max_value=120, value=25)
        gender = st.selectbox("Gender", ["Male", "Female"])
        height = st.number_input("Height (cm)", min_value=1, max_value=300, value=170)
        weight = st.number_input("Weight (kg)", min_value=1, max_value=500, value=70)
        weight_goal = st.selectbox("Weight Goal", ["Lose Weight", "Maintain Weight", "Gain Weight"])
        activity_level = st.selectbox("Activity Level", ["Sedentary", "Moderately Active", "Extremely Active"])
        submit_button = st.form_submit_button("Submit")

    if submit_button:
        # Mifflin-St Jeor Equation:
        bmi = weight / ((height / 100) ** 2)
        if gender == "Male":
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        else:
            bmr = 10 * weight + 6.25 * height - 5 * age - 161

        recommended_calories = bmr

        if activity_level == "Sedentary":
            total_calories = recommended_calories * 1.2
        elif activity_level == "Moderately Active":
            total_calories = recommended_calories * 1.55
        else:
            total_calories = recommended_calories * 1.9

        if weight_goal == "Lose Weight":
            total_calories = total_calories * 0.8
        elif weight_goal == "Maintain Weight":
            total_calories = total_calories * 1
        else:
            total_calories = total_calories * 1.2

        display_bmi(bmi)
        st.info(f"Recommended Calories: {round(total_calories, 1)}")
        st.markdown("<hr>", unsafe_allow_html=True)
        st.subheader("Food Recommendations")
        st.info("""
            In most Indian meals, the main dish is always accompanied by Rotis or Rice. 
            The recommendations below are for the main dish with the total calorie count at the end of the day, 
            you can choose the amount of roti or rice with that below estimate. 
            \nAs a rough estimate: 1 medium-sized roti is around 120 calories. 
            \nAs a rough estimate: 100g of cooked rice is around 130 calories.
        """)
        breakfast_recommendations = get_meal_recommendations(recommended_calories * 0.3, 'Main Course')
        lunch_recommendations = get_meal_recommendations(recommended_calories * 0.4, 'Lunch')
        dinner_recommendations = get_meal_recommendations(recommended_calories * 0.3, 'Main Course')

        st.subheader("Breakfast")
        if breakfast_recommendations is not None:
            with st.expander(f"{breakfast_recommendations['RecipeName']} - {breakfast_recommendations['Cuisine']}"):
                st.image(get_images_links(breakfast_recommendations[0]),caption="Image for Recipe: {}".format(breakfast_recommendations['RecipeName']))
                st.subheader("Ingredients:")
                st.write(breakfast_recommendations['Ingredients'])
                st.markdown(
                    f"<p style='font-size:20px'><b>Prep Time:</b> {breakfast_recommendations['PrepTimeInMins']} minutes</p>",
                    unsafe_allow_html=True)
                st.markdown(
                    f"<p style='font-size:20px'><b>Cook Time:</b> {breakfast_recommendations['CookTimeInMins']} minutes</p>",
                    unsafe_allow_html=True)
                st.markdown(f"<p style='font-size:20px'><b>Servings:</b> {breakfast_recommendations['Servings']}</p>",
                            unsafe_allow_html=True)
                st.markdown(f"<p style='font-size:20px'><b>Diet:</b> {breakfast_recommendations['Diet']}</p>",
                            unsafe_allow_html=True)
                st.subheader("Instructions:")
                st.write(breakfast_recommendations['Instructions'])
                st.subheader("Calories:")
                st.write(breakfast_recommendations['calories'])
                st.subheader("Total Fat:")
                st.write(f"{breakfast_recommendations['fat_total_g']} g")
                st.subheader("Protein:")
                st.write(f"{breakfast_recommendations['protein_g']} g")
                st.subheader("Cholesterol:")
                st.write(f"{breakfast_recommendations['cholesterol_mg']} mg")
                st.subheader("Total Carbohydrates:")
                st.write(f"{breakfast_recommendations['carbohydrates_total_g']} g")
                st.subheader("Fiber:")
                st.write(f"{breakfast_recommendations['fiber_g']} g")
                st.subheader("Sugar:")
                st.write(f"{breakfast_recommendations['sugar_g']} g")
        else:
            st.write("No breakfast recommendations within the calorie constraint.")

        st.subheader("Lunch")
        if lunch_recommendations is not None:
            with st.expander(f"{lunch_recommendations['RecipeName']} - {lunch_recommendations['Cuisine']}"):
                st.image(get_images_links(lunch_recommendations['RecipeName']), caption="Image for Recipe: {}".format(lunch_recommendations['RecipeName']))
                st.subheader("Ingredients:")
                st.write(lunch_recommendations['Ingredients'])
                st.markdown(
                    f"<p style='font-size:20px'><b>Prep Time:</b> {lunch_recommendations['PrepTimeInMins']} minutes</p>",
                    unsafe_allow_html=True)
                st.markdown(
                    f"<p style='font-size:20px'><b>Cook Time:</b> {lunch_recommendations['CookTimeInMins']} minutes</p>",
                    unsafe_allow_html=True)
                st.markdown(f"<p style='font-size:20px'><b>Servings:</b> {lunch_recommendations['Servings']}</p>",
                            unsafe_allow_html=True)
                st.markdown(f"<p style='font-size:20px'><b>Diet:</b> {lunch_recommendations['Diet']}</p>",
                            unsafe_allow_html=True)
                st.subheader("Instructions:")
                st.write(lunch_recommendations['Instructions'])
                st.subheader("Calories:")
                st.write(lunch_recommendations['calories'])
                st.subheader("Total Fat:")
                st.write(f"{lunch_recommendations['fat_total_g']} g")
                st.subheader("Protein:")
                st.write(f"{lunch_recommendations['protein_g']} g")
                st.subheader("Cholesterol:")
                st.write(f"{lunch_recommendations['cholesterol_mg']} mg")
                st.subheader("Total Carbohydrates:")
                st.write(f"{lunch_recommendations['carbohydrates_total_g']} g")
                st.subheader("Fiber:")
                st.write(f"{lunch_recommendations['fiber_g']} g")
                st.subheader("Sugar:")
                st.write(f"{lunch_recommendations['sugar_g']} g")
        else:
            st.write("No lunch recommendations within the calorie constraint.")

        st.subheader("Dinner")
        if dinner_recommendations is not None:
            with st.expander(f"{dinner_recommendations['RecipeName']} - {dinner_recommendations['Cuisine']}"):
                st.image(get_images_links(dinner_recommendations['RecipeName']), caption="Image for Recipe")
                st.subheader("Ingredients:")
                st.write(dinner_recommendations['Ingredients'])
                st.markdown(
                    f"<p style='font-size:20px'><b>Prep Time:</b> {dinner_recommendations['PrepTimeInMins']} minutes</p>",
                    unsafe_allow_html=True)
                st.markdown(
                    f"<p style='font-size:20px'><b>Cook Time:</b> {dinner_recommendations['CookTimeInMins']} minutes</p>",
                    unsafe_allow_html=True)
                st.markdown(f"<p style='font-size:20px'><b>Servings:</b> {dinner_recommendations['Servings']}</p>",
                            unsafe_allow_html=True)
                st.markdown(f"<p style='font-size:20px'><b>Diet:</b> {dinner_recommendations['Diet']}</p>",
                            unsafe_allow_html=True)
                st.subheader("Instructions:")
                st.write(dinner_recommendations['Instructions'])
                st.subheader("Calories:")
                st.write(dinner_recommendations['calories'])
                st.subheader("Total Fat:")
                st.write(f"{dinner_recommendations['fat_total_g']} g")
                st.subheader("Protein:")
                st.write(f"{dinner_recommendations['protein_g']} g")
                st.subheader("Cholesterol:")
                st.write(f"{dinner_recommendations['cholesterol_mg']} mg")
                st.subheader("Total Carbohydrates:")
                st.write(f"{dinner_recommendations['carbohydrates_total_g']} g")
                st.subheader("Fiber:")
                st.write(f"{dinner_recommendations['fiber_g']} g")
                st.subheader("Sugar:")
                st.write(f"{dinner_recommendations['sugar_g']} g")
        else:
            st.write("No dinner recommendations within the calorie constraint.")

        total_calories = 0
        if breakfast_recommendations is not None:
            total_calories += breakfast_recommendations['calories']
        if lunch_recommendations is not None:
            total_calories += lunch_recommendations['calories']
        if dinner_recommendations is not None:
            total_calories += dinner_recommendations['calories']

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown(f"Total Calories per 100 grams (assume as 1 serving) of each food item: **{round(total_calories, 1)}**")
        max_servings = recommended_calories / total_calories
        st.info(f"The maximum amount of serving for each meal that you can eat is: {max_servings:.2f}")
        st.markdown("<hr>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()