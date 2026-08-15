import os
import json
from typing import Optional
from langchain_core.tools import tool
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_core.prompts import PromptTemplate


load_dotenv(r"C:\Users\yovin\Desktop\Car-IA\.venv-1\.env")
api_key = os.getenv("OPENAI_API_KEY")

# --- Load the CSV of LinkedIn profiles ---
loader = CSVLoader("C:/Users/yovin/Desktop/Car-IA/listings.csv")
data = loader.load()  # list of Document objects, one per row


def find_profile(name: str, docs):
    """Return the first document whose content mentions `name`."""
    name_lower = name.lower()
    for doc in docs:
        if name_lower in doc.page_content.lower():
            return doc
    return None

@tool
def json_writer(overall_score: int,
    priority_improvements: list[dict],
    connections_score: Optional[int], connections_reasoning: str,
    headshot_score: Optional[int], headshot_reasoning: str, headshot_evaluated: bool,
    cover_photo_score: Optional[int], cover_photo_reasoning: str,
    about_score: Optional[int], about_reasoning: str,
    work_experience_score: Optional[int], work_experience_reasoning: str,
    education_score: Optional[int], education_reasoning: str,
    extracurriculars_score: Optional[int], extracurriculars_reasoning: str,
    posts_score: Optional[int], posts_reasoning: str,
) -> str:
    """Save the completed LinkedIn profile analysis. Call this once you have
        scored every section and identified the priority improvements."""
    data = {
        "overall_score": overall_score,
        "priority_improvements": priority_improvements,
        "sections": {
            "connections": {"score": connections_score, "max": 10, "reasoning": connections_reasoning, "evaluated": True},
            "headshot": {"score": headshot_score, "max": 10, "reasoning": headshot_reasoning, "evaluated": headshot_evaluated},
            "cover_photo": {"score": cover_photo_score, "max": 10, "reasoning": cover_photo_reasoning, "evaluated": True},
            "about": {"score": about_score, "max": 10, "reasoning": about_reasoning, "evaluated": True},
            "work_experience": {"score": work_experience_score, "max": 10, "reasoning": work_experience_reasoning, "evaluated": True},
            "education": {"score": education_score, "max": 10, "reasoning": education_reasoning, "evaluated": True},
            "extracurriculars": {"score": extracurriculars_score, "max": 10, "reasoning": extracurriculars_reasoning, "evaluated": True},
            "posts": {"score": posts_score, "max": 10, "reasoning": posts_reasoning, "evaluated": True},
        }
    }
    with open("analyzed-profile.json", "w", encoding="utf-8")  as file:
        json.dump(data ,file, indent=4)


    return "Data has been sent to the JSON"

rubric = """
Connections: 
    - At least 500 connections

Profile headshot:
    - Person should have a headshot which would be shoulders up
    - Dress clothes
    - Clean Shaven with a fresh haircut if person is a male
    - If a female, hair should be presented well
    - NO fraternity photos or at a social event 

Cover Photo:
    - Stock image of the school the user attends or of a city they are from

About section:
    - 2-3 sentences highlighting best qualifications and stats with no filler included
    - Resume should be included in the users Linkedin Profile

Work experience:
    - Should be the 3-4 of the most recent things the user has done with
    - the thing that’s most relevant should have the most detail out of anything else
    - Roughly 2-3 points for each of these experiences where the user highlights with action verbs in the most quantifiable way possible
    - In those bullets points there SHOULD NOT be : “I supported, I assisted”
    - No lying should be involved

Education Section: 
    - The college the user currently attends/ has attended 
    - Any graduate degrees as well
    - Include GPA unless your 5 to 7 years out of graduating
    - If the user has made the deans list add that in awards/honors

Pre professional Extracurriculars:
    - If you have leadership positions are good
    - Social extracurriculars are not as good


Posts:
    - Good posts:
        - Internships, research, jobs that user that relates to the major
        - A huge accomplishment like winning a hackathon
        - Earning a certification WITH explaining
        - Building a project that highlights their expertise in their respected major
Bad posts:
    - Attending a career fair
    - Standalone certificate
    - Generic work anniversaries
    - Facebook style life updates
    - Inspirational platitudes
    - Political rants
Format of posting:
    - The post should be humble, straight to the point, and how it will help my career
    - The post shouldn’t have overly dramatic writing, one-sentence paragraphs about mundane daily occurrences 

"""

prompt_template = PromptTemplate.from_template(
    """
    You are a professional linkedin analyzer seeing how a college 
    student can improve their linkedin account to be seen by 
    recruiters and eventually be given an interview. 
    Give a priority on what would need the most improvement.
    This should be given in a numbered list. If you can’t access a 
    certain section of the user's profile, please give the sections you couldn’t access. 
    Rate each subsection out of 10 and then rate the whole profile out of 100. If the user is too young or
    they don’t have a certain experience don’t take it out of the score.Instead encourage the user to fill those things out.
    Your tone should be completely professional. To assess the profile, 
    use the rubric and profile data delimited in triple backticks.

    ```{profile_data}```

    ```{rubric}```
    
    """
)

llm = ChatOpenAI(model="gpt-5.6", api_key=api_key, temperature=0, reasoning_effort="none")
llm_with_tool = llm.bind_tools([json_writer])


name_to_find = "Yovin"
profile_doc = find_profile(name_to_find, data)

if profile_doc is None:
    print(f"No profile found matching '{name_to_find}'.")
else:
    formatted_prompt = prompt_template.format(
        profile_data=profile_doc.page_content,
        rubric=rubric
    )
    response = llm_with_tool.invoke(formatted_prompt)

    if response.tool_calls:
        tool_call = response.tool_calls[0]
        args = tool_call["args"]          # this is your scored data as a dict
        json_writer.invoke(args)          # actually runs the write
        print(json.dumps(args, indent=2))
    else:
        print("Model did not call the tool:", response.content)