"""Gemini AI service for breaking down goals into tasks."""

import os
import json
from typing import Dict, List
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini AI
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)


def break_down_goal(goal_text: str) -> Dict[str, any]:
    """
    Use Gemini AI to break down a vague goal into 5 actionable steps.
    
    Args:
        goal_text: The user's goal description
        
    Returns:
        Dictionary containing tasks list and complexity score
    """
    try:
        # Initialize the model
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Create the prompt
        prompt = f"""You are an expert goal-setting coach. Break down the following goal into exactly 5 actionable, specific steps.
Also provide a complexity score from 1-10 (1 being very simple, 10 being extremely complex).

Goal: "{goal_text}"

Return your response as a JSON object with this exact structure:
{{
    "tasks": [
        "Step 1 description",
        "Step 2 description", 
        "Step 3 description",
        "Step 4 description",
        "Step 5 description"
    ],
    "complexity_score": <number between 1-10>
}}

Make each step:
- Specific and actionable
- Progressive (building on previous steps)
- Realistic and achievable
- Clear and concise

Respond ONLY with the JSON object, no additional text."""

        # Generate response
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Clean up response (remove markdown code blocks if present)
        if response_text.startswith("```json"):
            response_text = response_text[7:]  # Remove ```json
        if response_text.startswith("```"):
            response_text = response_text[3:]  # Remove ```
        if response_text.endswith("```"):
            response_text = response_text[:-3]  # Remove trailing ```
        response_text = response_text.strip()
        
        # Parse JSON response
        result = json.loads(response_text)
        
        # Validate response structure
        if "tasks" not in result or "complexity_score" not in result:
            raise ValueError("Invalid response structure from AI")
        
        if len(result["tasks"]) != 5:
            raise ValueError("AI did not return exactly 5 tasks")
        
        if not (1 <= result["complexity_score"] <= 10):
            raise ValueError("Complexity score must be between 1 and 10")
        
        return result
        
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        print(f"Response text: {response_text}")
        # Return fallback response
        return {
            "tasks": [
                "Research and gather information about this goal",
                "Create a detailed plan with milestones",
                "Set up necessary resources and tools",
                "Take the first actionable step",
                "Monitor progress and adjust as needed"
            ],
            "complexity_score": 5
        }
    except Exception as e:
        print(f"Error in AI service: {e}")
        # Return fallback response
        return {
            "tasks": [
                "Research and gather information about this goal",
                "Create a detailed plan with milestones",
                "Set up necessary resources and tools",
                "Take the first actionable step",
                "Monitor progress and adjust as needed"
            ],
            "complexity_score": 5
        }
