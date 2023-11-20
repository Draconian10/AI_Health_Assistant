import streamlit as st
import openai
import os
import toml

# Initialize session state for conversation history
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

openai.api_key = st.secrets["OPENAI_API_KEY"]

# Streamlit app layout
st.title('Health and Fitness Assistant')

# Dropdown for selecting between Diet Plan and Workout Plan
with st.sidebar:
    st.header("Choose Your Plan")
    plan_type = st.selectbox('Select a Plan', ['Diet Plan and Recipes', 'Workout Plan'])

    if plan_type == 'Diet Plan and Recipes':
        # Input fields for Diet Plan
        st.header("Input Your Details for Diet Plan")
        age = st.number_input('Age', min_value=18, max_value=100)
        gender = st.selectbox('Gender', ['Male', 'Female'])
        height = st.number_input('Height in cm', min_value=100, max_value=250)
        weight = st.number_input('Weight in kg', min_value=30, max_value=200)
        goal = st.selectbox('Goal', ['Gain Muscle', 'Lose Weight'])
        activity = st.selectbox('Activity Level', ['Sedentary', 'Light', 'Moderate', 'Active'])
        submit_button_diet = st.button('Generate Diet Plan and Recipes')

    elif plan_type == 'Workout Plan':
        # Input fields for Workout Plan
        st.header("Input Your Details for Workout Plan")
        age_w = st.number_input('Age', min_value=18, max_value=100, key='workout_age')
        gender_w = st.selectbox('Gender', ['Male', 'Female'], key='workout_gender')
        height_w = st.number_input('Height in cm', min_value=100, max_value=250, key='workout_height')
        weight_w = st.number_input('Weight in kg', min_value=30, max_value=200, key='workout_weight')
        weight_goal = st.selectbox('Weight Goal', ['Gain Muscle', 'Lose Weight', 'Maintain Weight'], key='workout_goal')
        submit_button_workout = st.button('Generate Workout Plan')

# Handling the output generation outside the sidebar block
if plan_type == 'Diet Plan and Recipes' and submit_button_diet:
    st.session_state.user_text = ""
    st.session_state.conversation = None

    initial_prompt = "Act like a ChatGPT. You know everything."
    if st.session_state.conversation is None:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        st.session_state.conversation = []

        question1 = f"Generate a diet plan for a {age}-year-old {gender}, height {height} cm, weight {weight} kg, goal: {goal}, activity level: {activity}. The diet plan should be in the following format: Breakfast, Mid-Morning Snack, Lunch, Evening Snack, Dinner. Generate it in proper markdown format."

        response1 = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": initial_prompt},
                {"role": "user", "content": question1},
            ],
        )['choices'][0]['message']['content']

        question2 = f"Generate simple recipes for the dishes present in the following diet plan: {response1}. The recipes should be in the following format: Dish name, Ingredients, Instructions. Generate it in proper markdown format."

        response2 = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": initial_prompt},
                {"role": "user", "content": question2},
            ],
        )['choices'][0]['message']['content']

        st.session_state.conversation.extend([response1, response2])

    st.write("Diet Plan:\n\n" + st.session_state.conversation[0])
    st.write("Recipes:\n\n" + st.session_state.conversation[1])

elif plan_type == 'Workout Plan' and submit_button_workout:
    st.session_state.user_text = ""
    st.session_state.conversation = None

    initial_prompt = "Act like a ChatGPT. You know everything."
    if st.session_state.conversation is None:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        st.session_state.conversation = []

        question = f"Generate a workout plan for a {age_w}-year-old {gender_w}, height {height_w} cm, weight {weight_w} kg, weight goal: {weight_goal}. The workout plan should be tailored to the individual's needs. Generate it in proper markdown format."

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": initial_prompt},
                {"role": "user", "content": question},
            ],
        )['choices'][0]['message']['content']

        st.session_state.conversation.append(response)

    st.write("Workout Plan:\n\n" + st.session_state.conversation[0])
