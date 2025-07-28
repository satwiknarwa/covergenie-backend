import httpx
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from decouple import config
from datetime import datetime

GROQ_API_KEY = config("GROQ_API_KEY")

class CoverLetterGenerator(APIView):
    def post(self, request):
        data = request.data

        # Extract all fields from request data
        name = data.get("Name")
        email = data.get("Email")
        phone = data.get("Phone")
        address = data.get("Address")
        job_title = data.get("jobTitle")
        company = data.get("Company")
        skills = data.get("Skills")
        experience = data.get("Experience")

        # Optional: use today's date if not provided
        today_date = datetime.now().strftime("%d %B %Y")

        # Prompt with personal info included
        prompt = (
            f"Write a formal, professional cover letter for {name}, who lives at {address}, "
            f"with email {email} and phone number {phone}, dated {today_date}. "
            f"The letter is for the position of {job_title} at {company}. "
            f"Include these skills: {skills}, and this experience: {experience}. "
            "Use proper formatting with address and contact details at the top, and sign off using the applicant's name. "
            "Avoid using any placeholders like [Your Name], [Address], etc."
        )

        try:
            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            }

            json_data = {
                "model": "llama3-8b-8192",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 400
            }

            response = httpx.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=json_data
            )

            result = response.json()
            cover_letter = result["choices"][0]["message"]["content"]

            return Response({"cover_letter": cover_letter}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
