import openai
import pandas as pd
import speech_recognition as sr
import pyttsx3 


openai.api_key = 'API-KEY-GPT4o'

# TRAIN ON MORE SPECIFIC NUTRITION RESOURCES
# SIMPLIFY USER EXPERIENCE
# WHAT TO EAT, WHEN, AND IF IM ON TRACK
# USE DATABASE TO STORE PREVIOUS SCORES/DATA, USE THAT TO GIVE FUTURE RECOMMENDATIONS 
# USE SPEECH TO TEXT LIBRARY 
# score metrics from baseline to rolling 30 day score

# Python program to translate
# speech to text and text to speech
 
 

 
# Initialize the recognizer 
r = sr.Recognizer() 

# Function to convert text to speech
def SpeakText(command):
    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command) 
    engine.runAndWait()
     
# Function to convert speech to text
def get_speech_input():
    try:
        # Use the microphone as source for input.
        with sr.Microphone() as source:
            # Wait for a second to let the recognizer adjust the energy threshold
            r.adjust_for_ambient_noise(source, duration=0.2)
            # Listens for the user's input
            audio = r.listen(source)
            # Using Google to recognize audio
            text = r.recognize_google(audio)
            text = text.lower()
            print("Did you say:", text)
            return text
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
        return None
    except sr.UnknownValueError:
        print("Unknown error occurred")
        return None

# Example user details
height = 72
weight = 175
age = 18
gender = "male"
activity_level = "very active"
goal = "Gain Muscle"

# Taking Theo's CSV and reading file
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

# Step 2
def analyze_nutrition_description(nutrition_description):
    prompt = (
        f"Nutrition description: {nutrition_description}\n"
        "Estimate the total number of calories, grams of protein, fat, and carbs in this daily nutrition."
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

# Step 3: Score the daily nutrition based on the target macros using GPT-4
def score_nutrition_with_gpt(target_macros, nutrition_analysis):
    prompt = (
        f"Target macros: {target_macros}\n"
        f"Nutrition analysis: {nutrition_analysis}\n"
        "Based on these numbers, score the nutrition overall on a scale of 1 to 5 according to how well it meets the target macros. Then tell me exactly what to eat and when to hit reach my goals."
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
    
    # Step 2: Describe the daily nutrition 
    nutrition_description = get_speech_input()
    print(f"Nutrition Description: {nutrition_description}\n")
    
    # Step 3: Analyze the daily nutrition description using GPT-4
    nutrition_analysis = analyze_nutrition_description(nutrition_description)
    print(f"Nutrition Analysis: {nutrition_analysis}\n")
    
    # Step 4: Score the nutrition using GPT-4
    nutrition_score = score_nutrition_with_gpt(target_macros, nutrition_analysis)
    print(f"Nutrition Score: {nutrition_score}")

    # Step 5: Give supplement advice
    supp_Advice = supplement_advice(goal)
    print(f"\n\nSupplement Advice: {supp_Advice}")

# Call the function
if __name__ == "__main__":
    main()
