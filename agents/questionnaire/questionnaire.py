import pandas as pd
import json
ph9_q=["Over the last two weeks, how often have you been bothered by little interest or pleasure in doing things? (0 = Not at all, 1 = Several days, 2 = More than half the days, 3 = Nearly every day): ",
        "Over the last two weeks, how often have you been bothered by feeling down, depressed, or hopeless? (0 = Not at all, 1 = Several days, 2 = More than half the days, 3 = Nearly every day): ",
        "Over the last two weeks, how often have you been bothered by trouble falling or staying asleep, or sleeping too much? (0 = Not at all, 1 = Several days, 2 = More than half the days, 3 = Nearly every day): ",
        "Over the last two weeks, how often have you been bothered by feeling tired or having little energy? (0 = Not at all, 1 = Several days, 2 = More than half the days, 3 = Nearly every day): ",
        "Over the last two weeks, how often have you been bothered by poor appetite or overeating? (0 = Not at all, 1 = Several days, 2 = More than half the days, 3 = Nearly every day): ",
        "Over the last two weeks, how often have you been bothered by feeling bad about yourself – or that you are a failure or have let yourself or your family down? (0 = Not at all, 1 = Several days, 2 = More than half the days, 3 = Nearly every day): ",
        "Over the last two weeks, how often have you been bothered by trouble concentrating on things, such as reading the newspaper or watching television? (0 = Not at all, 1 = Several days, 2 = More than half the days, 3 = Nearly every day): ",
        "Over the last two weeks, how often have you been bothered by moving or speaking so slowly that other people could have noticed? Or the opposite – being so restless that you have to move around a lot more than usual? (0 = Not at all, 1 = Several days, 2 = More than half the days, 3 = Nearly every day): ",
        "Over the last two weeks, how often have you been bothered by thoughts that you would be better off dead or of hurting yourself in some way? (0 = Not at all, 1 = Several days, 2 = More than half the days, 3 = Nearly every day): "
]
responses={}
for i, q in enumerate(ph9_q):
    user_response=input(f"Q{i+1}:{q}")
    responses[f"Q{i+1}"]=user_response
print("\nUser responses",responses)

### Stored as json file
with open("php_9.json","w") as f:
    json.dump(responses,f, indent=4)
#### Not invoking an LLM here
#prompt_t=ChatPromptTemplate.from_messages([
                        #("system", "You an question interviewer that analyzes the patient mental health"),
                        #("human",  """Based on the questions
#Little interest:{Q1}
#Feeling down:{Q2}
#Trouble falling sleep:{Q3}
#Feeling tired:{Q4}
#Poor appetite:{Q5}
#Feeling bad:{Q6}
#Trouble concentrating:{Q7}
#Being restless:{Q8}
#Suicidal thought:{Q9}
 #Provide the accurate responses""")
#])
