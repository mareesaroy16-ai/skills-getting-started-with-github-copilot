"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    # Sports activities
    "Volleyball Team": {
        "description": "Competitive volleyball practices and matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 12,
        "participants": ["chloe@mergington.edu", "zac@mergington.edu"]
    },
    "Swimming Team": {
        "description": "Lap training and swim meets for all levels",
        "schedule": "Mondays, Wednesdays, Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["sarah@mergington.edu", "noah@mergington.edu"]
    },
    # Artistic activities
    "Photography Club": {
        "description": "Explore digital and film photography techniques",
        "schedule": "Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 18,
        "participants": ["nora@mergington.edu", "henry@mergington.edu"]
    },
    "Music Ensemble": {
        "description": "Instrumental ensemble rehearsals and performances",
        "schedule": "Fridays, 3:30 PM - 5:30 PM",
        "max_participants": 30,
        "participants": ["grace@mergington.edu", "jack@mergington.edu"]
    },
    # Intellectual activities
    "Math Club": {
        "description": "Problem solving, competitions, and advanced topics",
        "schedule": "Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["ethan@mergington.edu", "matthew@mergington.edu"]
    },
    "Science Club": {
        "description": "Labs, experiments, and science fair projects",
        "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
        "max_participants": 25,
        "participants": ["ava@mergington.edu", "zoe@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


from pydantic import BaseModel

class RegistrationRequest(BaseModel):
    activity: str
    email: str

@app.post("/activities/register")
async def register_activity(registration: RegistrationRequest):
    """Register a student for an activity"""
    # Validate activity exists
    if registration.activity not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    # Check if activity is full
    if len(activities[registration.activity]["participants"]) >= activities[registration.activity]["max_participants"]:
        raise HTTPException(status_code=400, detail="Activity is full")
        
    # Check if student is already registered
    if registration.email in activities[registration.activity]["participants"]:
        raise HTTPException(status_code=400, detail="Already registered for this activity")
        
    # Register the student
    activities[registration.activity]["participants"].append(registration.email)
    return {"message": "Successfully registered for activity"}


@app.post("/activities/{activity}/unregister")
async def unregister_activity(activity: str, email: str):
    """Unregister a student from an activity"""
    # Validate activity exists
    if activity not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
        
    # Check if student is registered
    if email not in activities[activity]["participants"]:
        raise HTTPException(status_code=400, detail="Not registered for this activity")
        
    # Unregister the student
    activities[activity]["participants"].remove(email)
    return {"message": "Successfully unregistered from activity"}

    # Get the specific activity
    # Ensure additional activities exist (idempotent)
    extra_activities = {
        "Soccer Team": {
            "description": "Team-based soccer practices and inter-school matches",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 18,
            "participants": ["liam@mergington.edu", "noah@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Competitive basketball team and skills training",
            "schedule": "Mondays, Wednesdays, 4:00 PM - 6:00 PM",
            "max_participants": 12,
            "participants": ["mia@mergington.edu", "ava@mergington.edu"]
        },
        "Art Club": {
            "description": "Explore painting, drawing, and mixed media projects",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participants": ["isabella@mergington.edu", "charlotte@mergington.edu"]
        },
        "Drama Club": {
            "description": "Acting, stagecraft, and school play productions",
            "schedule": "Fridays, 3:30 PM - 5:30 PM",
            "max_participants": 25,
            "participants": ["lucas@mergington.edu", "ethan@mergington.edu"]
        },
        "Debate Team": {
            "description": "Competitive debating and public speaking practice",
            "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
            "max_participants": 16,
            "participants": ["oliver@mergington.edu", "sophia@mergington.edu"]
        },
        "Robotics Club": {
            "description": "Design and build robots; participate in competitions",
            "schedule": "Thursdays, 3:30 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["amelia@mergington.edu", "harry@mergington.edu"]
        }
    }

    for name, info in extra_activities.items():
        activities.setdefault(name, info)

    activity = activities[activity_name]

    # Validate student is not already signed up
    if len(activity["participants"]) >= activity["max_participants"]:
        raise HTTPException(status_code=400, detail="Activity is full")
    
    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}
