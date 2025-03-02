import openai
import os
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# Set up OpenAI API key
OPENAI_API_KEY = "key"
class ActionGenerateLinkedInMessage(Action):
    def name(self):
        return "action_generate_linkedin_message"

    def run(self, dispatcher, tracker, domain):
        company = tracker.get_slot("company")
        job_title = tracker.get_slot("job_title")
        conversation_tone = "Keep it professional yet warm and engaging."
        if job_title and company:
            prompt = f"Write a personalized LinkedIn connection request for a {job_title} at {company}. {conversation_tone}" 
        elif company:
            prompt = f"Write a LinkedIn connection request message for someone working at {company}. {conversation_tone}"
        else:
            prompt = f"Write a generic LinkedIn connection request message. {conversation_tone}"
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "system", "content": "You are an expert in professional networking. Craft clear and effective LinkedIn connection messages."},
                          {"role": "user", "content": prompt}]
            )
            message = response["choices"][0]["message"]["content"]
        except Exception as e:
            message = f"Error generating LinkedIn message: {str(e)}"

        dispatcher.utter_message(text=message)
        return []

class ActionReviewResume(Action):
    def name(self):
        return "action_review_resume"

    def run(self, dispatcher, tracker, domain):
        prompt = "Review this resume and provide constructive feedback, highlighting strengths, areas for improvement, and suggestions to tailor it for specific roles."
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "system", "content": "You are an expert career advisor skilled in resume review. Provide actionable insights."},
                          {"role": "user", "content": prompt}]
            )
            feedback = response["choices"][0]["message"]["content"]
        except Exception as e:
            feedback = f"Error generating resume feedback: {str(e)}"

        dispatcher.utter_message(text=feedback)
        return []

class ActionFallbackToOpenAI(Action):
    def name(self):
        return "action_fallback_to_openai"

    def run(self, dispatcher, tracker, domain):
        user_input = tracker.latest_message.get("text", "")
        prompt = f"The user asked: '{user_input}'. Respond helpfully and professionally."
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "system", "content": "You are a helpful AI assistant that provides relevant responses to any query."},
                          {"role": "user", "content": prompt}]
            )
            ai_response = response["choices"][0]["message"]["content"]
        except Exception as e:
            ai_response = f"I'm sorry, I couldn't process your request. Error: {str(e)}"
        
        dispatcher.utter_message(text=ai_response)
        return []
