import pandas as pd
import numpy as np
import random

# --- Configuration ---
NUM_RESPONDENTS = 50

# --- Dataset 1: Demographics ---
demographics_data = []

# Brisbane Postcodes (a selection for variety)
brisbane_postcodes = [
    4000, 4001, 4005, 4006, 4007, 4008, 4009, 4010, 4011, 4012, 4013, 4014, 4017,
    4018, 4019, 4020, 4021, 4022, 4029, 4030, 4031, 4032, 4034, 4035, 4036, 4037,
    4051, 4053, 4054, 4055, 4060, 4061, 4064, 4065, 4066, 4067, 4068, 4069, 4070,
    4073, 4074, 4075, 4076, 4077, 4078, 4101, 4102, 4103, 4104, 4105, 4106, 4107,
    4108, 4109, 4110, 4111, 4112, 4113, 4114, 4115, 4116, 4117, 4118, 4119, 4120,
    4121, 4122, 4123, 4124, 4125, 4127, 4128, 4129, 4130, 4131, 4132, 4133, 4151,
    4152, 4153, 4154, 4155, 4156, 4157, 4158, 4159, 4160, 4161, 4163, 4164, 4165,
    4169, 4170, 4171, 4172, 4173, 4174, 4178, 4179, 4205, 4207
]

# Education levels with approximate probabilities
education_levels = {
    "High School": 0.25,
    "Bachelor's Degree": 0.40,
    "Master's Degree": 0.20,
    "PhD": 0.05,
    "Other/Vocational": 0.10
}

# Nationalities with approximate probabilities (Australian context)
nationalities = {
    "Australian": 0.70,
    "Indian": 0.05,
    "Chinese": 0.04,
    "Filipino": 0.03,
    "UK": 0.03,
    "New Zealander": 0.02,
    "South African": 0.01,
    "Other": 0.12
}

genders = ['Male', 'Female', 'Non-binary']

# --- Dataset 2: Likert Scale Traffic Experience ---
likert_data = []
likert_questions = [
    "Q1: Traffic congestion significantly impacts my daily routine.",
    "Q2: I feel stressed and frustrated because of local traffic.",
    "Q3: Public transport in my area is an effective alternative to driving.",
    "Q4: I believe existing road infrastructure is adequate for current traffic volumes.",
    "Q5: I am willing to tolerate significant delays for road maintenance/upgrades."
]

# --- Dataset 3: Open-Ended Text Response ---
open_response_data = []

# Main causes themes for open-ended responses
cause_themes = [
    "poor road design", "not enough lanes", "bad intersections", "outdated infrastructure",
    "too many cars on the road", "population growth", "too many people moving here",
    "bad drivers", "people not merging correctly", "distracted drivers", "aggressive drivers",
    "lack of adequate public transport", "public transport is too expensive", "public transport doesn't go where I need it",
    "constant roadworks", "construction everywhere", "poor planning of roadworks",
    "trucks and large vehicles on city roads", "heavy vehicle movements"
]

# Filler phrases and variations
filler_phrases = [
    "I think it's mainly ", "Honestly, it's just ", "The biggest issue is probably ",
    "Definitely ", "It's a combination of things, but primarily ", "You can blame ",
    "Mostly due to ", "Seems like ", "The main culprit is ", "It boils down to "
]

frustration_phrases = [
    ". It drives me crazy.", ". It's getting worse every year.", ". Something needs to be done.",
    ". It's a nightmare.", ". It's just constant.", ". Very frustrating.",
    ". Needs urgent attention."
]

for i in range(1, NUM_RESPONDENTS + 1):
    # Respondent ID
    respondent_id = i

    # --- Generate Demographics ---
    age = np.random.randint(18, 75)
    gender = np.random.choice(genders, p=[0.48, 0.50, 0.02])
    education = np.random.choice(list(education_levels.keys()), p=list(education_levels.values()))
    nationality = np.random.choice(list(nationalities.keys()), p=list(nationalities.values()))
    postcode = np.random.choice(brisbane_postcodes)

    demographics_data.append({
        'respondent_id': respondent_id,
        'age': age,
        'gender': gender,
        'education_level': education,
        'nationality': nationality,
        'postcode': postcode
    })

    # --- Generate Likert Scale Responses with Age Bias ---
    # Scale: 1 = Strongly Disagree, 5 = Strongly Agree
    # Younger people (e.g., <35) -> more frustrated/less accepting
    # Older people (e.g., >50) -> potentially more tolerant/less impacted, or just different views

    likert_scores = {}
    for q_idx, question in enumerate(likert_questions):
        q_num = q_idx + 1
        score = 0

        # Q1: Traffic congestion significantly impacts my daily routine. (Higher score = more impact/frustration)
        # Q2: I feel stressed and frustrated because of local traffic. (Higher score = more stress)
        if q_num in [1, 2]:
            if age < 30: # Young, very impacted/frustrated
                score = np.random.choice([4, 5], p=[0.4, 0.6])
            elif 30 <= age < 50: # Middle-aged, moderately impacted
                score = np.random.choice([3, 4, 5], p=[0.2, 0.5, 0.3])
            else: # Older, possibly less daily commute, or more tolerant
                score = np.random.choice([2, 3, 4], p=[0.3, 0.5, 0.2])
        # Q3: Public transport in my area is an effective alternative to driving. (Lower score = less effective)
        # Q4: I believe existing road infrastructure is adequate for current traffic volumes. (Lower score = less adequate)
        # Q5: I am willing to tolerate significant delays for road maintenance/upgrades. (Lower score = less tolerant)
        elif q_num in [3, 4, 5]: # For these, lower scores mean less acceptance/more impatience
            if age < 30: # Young, likely impatient/disagree PT/infra is good
                score = np.random.choice([1, 2], p=[0.6, 0.4])
            elif 30 <= age < 50: # Middle-aged
                score = np.random.choice([1, 2, 3], p=[0.3, 0.5, 0.2])
            else: # Older, possibly more tolerant or use PT less
                score = np.random.choice([2, 3, 4], p=[0.2, 0.5, 0.3])

        likert_scores[f'q{q_num}'] = score

    likert_data.append({'respondent_id': respondent_id, **likert_scores})

    # --- Generate Open-Ended Text Response ---
    num_causes = random.randint(1, 3) # Each response will mention 1 to 3 causes
    selected_causes = random.sample(cause_themes, num_causes)

    response_parts = []
    for j, cause in enumerate(selected_causes):
        if j == 0:
            response_parts.append(random.choice(filler_phrases) + cause)
        elif j == num_causes - 1: # Last cause, potentially add frustration
            if num_causes > 1:
                response_parts.append(random.choice([" and ", ", and "]) + cause + random.choice(frustration_phrases))
            else:
                response_parts.append(cause + random.choice(frustration_phrases))
        else:
            response_parts.append(random.choice([", ", "; "]) + cause)

    open_response = "".join(response_parts).capitalize() # Capitalize first letter

    # Add some general conversational noise sometimes
    if random.random() < 0.2: # 20% chance to add a general comment
        general_comments = [
            " It's a real challenge in Brisbane.",
            " Gets worse during peak hours.",
            " My commute is just getting longer.",
            " Always something happening on the roads.",
            " Brisbane traffic is unique."
        ]
        open_response += random.choice(general_comments)

    open_response_data.append({
        'respondent_id': respondent_id,
        'open_response': open_response
    })

# --- Create DataFrames ---
df_demographics = pd.DataFrame(demographics_data)
df_likert = pd.DataFrame(likert_data)
df_open_response = pd.DataFrame(open_response_data)

# --- Save to CSV files ---
df_demographics.to_csv('/home/fleetr/workshop_syn_data/traffic_survey_demographics.csv', index=False)
df_likert.to_csv('/home/fleetr/workshop_syn_data/traffic_survey_likert.csv', index=False)
df_open_response.to_csv('/home/fleetr/workshop_syn_data/traffic_survey_open_response.csv', index=False)

print("Synthetic data generated successfully!")
print("Files created:")
print("- traffic_survey_demographics.csv")
print("- traffic_survey_likert.csv")
print("- traffic_survey_open_response.csv")

print("\n--- Demographics Sample ---")
print(df_demographics.head())
print("\n--- Likert Sample ---")
print(df_likert.head())
print("\n--- Open Response Sample ---")
print(df_open_response.head())

# Optional: Check age distribution in Likert data for bias confirmation
print("\n--- Likert Q2 scores by Age Group (Frustration) ---")
df_merged = pd.merge(df_demographics, df_likert, on='respondent_id')
df_merged['age_group'] = pd.cut(df_merged['age'], bins=[18, 30, 50, 75], labels=['18-29', '30-49', '50-74'])
print(df_merged.groupby('age_group')['q2'].mean())

print("\n--- Likert Q3 scores by Age Group (Public Transport Effectiveness) ---")
print(df_merged.groupby('age_group')['q3'].mean())