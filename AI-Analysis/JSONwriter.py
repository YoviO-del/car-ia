import json
from langchain_core.tools import tool

@tool
def json_writer():

    data = {
        "overall_score": 0,
        "priority_improvements": [
            {"rank": 1, "issue": "Missing headshot", "detail": "..."},
            {"rank": 2, "issue": "About section has filler language", "detail": "..."}
        ],
        "sections": {
            "connections": {"score": 4, "max": 10, "reasoning": "..."},
            "headshot": {"score": None, "max": 10, "reasoning": "No image provided — cannot evaluate", "evaluated": false},
            "cover_photo": {"score": 6, "max": 10, "reasoning": "..."},
            "about": {"score": 5, "max": 10, "reasoning": "..."},
            "work_experience": {"score": 7, "max": 10, "reasoning": "..."},
            "education": {"score": 9, "max": 10, "reasoning": "..."},
            "extracurriculars": {"score": 3, "max": 10, "reasoning": "..."},
            "posts": {"score": 2, "max": 10, "reasoning": "..."}
        }
    }
    with open("analyzed-profile.json", "w", encoding="utf-")  as file:
        json.dump(data ,file, indent=4)


agent = create_react_agent(llm, [json_writer])