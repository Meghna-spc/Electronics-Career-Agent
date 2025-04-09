import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

class CareerAdvisor:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Missing Gemini API key in .env")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def get_analysis(self, input_data, is_resume=False):
        try:
            if is_resume:
                prompt = f"""Analyze this resume for electronics engineering roles:
                            Technical Skills: {input_data['technical_skills']}
                            Transferable Skills: {input_data['transferable_skills']}
                            Experience: {input_data['experience']}
                            Education: {input_data['education']}
                            
                            Provide:
                            1. Career path suggestions
                            2. Skill gap analysis
                            3. Improvement recommendations"""
            else:
                prompt = f"As an electronics career expert, answer this: {input_data}"
            
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Analysis Error: {str(e)}"
