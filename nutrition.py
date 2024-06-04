import openai
import pandas as pd

openai.api_key = 'sk-proj-ll5CgZx6jPW7YcwriHw4T3BlbkFJ25L3pWg4cDZDoSjBAd6o'

# Example user details
height = 72
weight = 175
age = 18
gender = "male"
activity_level = "very active"
goal = "Gain Muscle"

# taking theos csv and reading  file
file_path = 'supps.csv'
df = pd.read_csv(file_path)
data_str = df.to_string(index=False)

def get_target_macros(height, weight, age, gender, activity_level, goal):
    prompt = (
        f"User details: Height = {height} inches, Weight = {weight} pounds, Age = {age}, Gender = {gender}, "
        f"Activity Level = {activity_level}, Health Goal = {goal}.\n"
        "Provide me with a number of calories, grams of protein, fat, and carbs in order to reach my fitness goals."
    )
    
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300
    )
    
    return response.choices[0].message.content

#Step 2
def analyze_diet_description(diet_description):
    prompt = (
        f"Diet description: {diet_description}\n"
        "Estimate the total number of calories, grams of protein, fat, and carbs in this daily diet."
    )
    
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300
    )
    
    return response.choices[0].message.content

# Step 3: Score the daily diet based on the target macros using GPT-4
def score_diet_with_gpt(target_macros, diet_analysis):
    prompt = (
        f"Target macros: {target_macros}\n"
        f"Diet analysis: {diet_analysis}\n"
        "Based on these numbers, score the diet overall on a scale of 1 to 5 according to how well it meets the target macros. Then offer advice on what foods to add to the diet to meet the target macronutrients."
    )
    
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300
    )
    
    return response.choices[0].message.content


# Step 4: Offer supplement advice
def supplement_advice(myGoal):
    prompt = (
        "Here is the data from the CSV file:\n\n"
        f"{data_str}\n\n"
        "Based on my fitness goal of " + myGoal + " , tell me if any of the supplements listed on this csv file could benefit me"
    )
    
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300
    )
    
    return response.choices[0].message.content


def main():
    # Step 1: Get the macro nutrients and calorie counts
    target_macros = get_target_macros(height, weight, age, gender, activity_level, goal)
    print(f"Fitness Plan:\n{target_macros}\n")
    
    # Step 2: Describe the daily diet 
    diet_description = (
        "Breakfast: 3 scrambled eggs, 2 slices cheese, 2 frozen hasbrowns, 1 roll. \n"
        "Snack: chocolate bar"
        "Dinner: grilled chicken, vegetables, 1 roll \n"
        "Snack: milk with a scoop of protein powder"
    )
    print(f"Diet Description: {diet_description}\n")
    
    # Step 3: Analyze the daily diet description using GPT-4
    diet_analysis = analyze_diet_description(diet_description)
    print(f"Diet Analysis: {diet_analysis}\n")
    
    # Step 4: Score the diet using GPT-4
    diet_score = score_diet_with_gpt(target_macros, diet_analysis)
    print(f"Diet Score: {diet_score}")

    # Step 5: Give supplement advice
    supp_Advice = supplement_advice(goal)
    print(f"\n\nSupplement Advice: {supp_Advice}")

# Call the function
if __name__ == "__main__":
    main()
