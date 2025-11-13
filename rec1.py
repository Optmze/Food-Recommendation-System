import streamlit as st
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import random

df = pd.read_csv('foodsfinal2.csv')


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


def main():
    st.title("🍚Diet Recommendation System")

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

        st.write("BMI:", bmi)
        st.write("Recommended Calories:", total_calories)

        st.subheader("Food Recommendations")
        st.write(
            "Note: In most Indian meals, the main dish is always accompanied by Rotis or Rice. The recommendations below are for the main dish with the total calorie count at the end of the day, you can choose the amount of roti or rice with that below estimate")
        st.write("As a rough estimate: 1 medium sized roti is around 120 calories")
        st.write("As a rough estimate: 100g of cooked rice is around 130 calories")
        breakfast_recommendations = get_meal_recommendations(recommended_calories * 0.3, 'Main Course')
        lunch_recommendations = get_meal_recommendations(recommended_calories * 0.4, 'Lunch')
        dinner_recommendations = get_meal_recommendations(recommended_calories * 0.3, 'Main Course')

        st.subheader("Breakfast")
        if breakfast_recommendations is not None:
            st.dataframe(breakfast_recommendations)
        else:
            st.write("No breakfast recommendations within the calorie constraint.")

        st.subheader("Lunch")
        if lunch_recommendations is not None:
            st.dataframe(lunch_recommendations)
        else:
            st.write("No lunch recommendations within the calorie constraint.")

        st.subheader("Dinner")
        if dinner_recommendations is not None:
            st.dataframe(dinner_recommendations)
        else:
            st.write("No dinner recommendations within the calorie constraint.")

        total_calories = 0
        if breakfast_recommendations is not None:
            total_calories += breakfast_recommendations['calories']
        if lunch_recommendations is not None:
            total_calories += lunch_recommendations['calories']
        if dinner_recommendations is not None:
            total_calories += dinner_recommendations['calories']

        st.subheader("Total Calories per 100 grams (assume as 1 serving) of each food item:")
        st.write(total_calories)
        st.write("The maximum amount of serving for each meal that you can eat is:", recommended_calories / total_calories)
