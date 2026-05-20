from django.shortcuts import render
import json
import base64
import io
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
from google import genai
from google.genai import types
import os
load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)
print("API KEY =", os.getenv("GEMINI_API_KEY"))

def slide_builder(request):
    return render(request, 'slide_builder.html')


def _generate_slide_titles(topic: str) -> list[str]:
    
    print("API KEY =", os.getenv("GEMINI_API_KEY"))
    prompt = f"""
You generate slide titles for presentations.

Return exactly five slide titles for a beginner friendly talk about "{topic}".

MUST return ONLY valid JSON in this exact structure:

{{
  "slides": [
    {{"title": "..." }},
    {{"title": "..." }},
    {{"title": "..." }},
    {{"title": "..." }},
    {{"title": "..." }}
  ]
}}
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[{"text": prompt}],
            config=types.GenerateContentConfig(response_mime_type="application/json"),
        )

        raw = ""
        for part in response.parts:
            if part.text:
                raw += part.text.strip()

        print("Raw title generation response:", raw)

        data = json.loads(raw)
        titles = [s["title"] for s in data.get("slides", []) if "title" in s]

        if len(titles) == 5:
            return titles
        
    except Exception as e:
        print("Title generation failed:", e)

    return [
        f"Introduction to {topic}",
        f"Core ideas of {topic}",
        f"How {topic} works",
        f"Use cases of {topic}",
        f"Future of {topic}",
    ]


@csrf_exempt
def generate_slides(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    try:
        body = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    topic = (body.get('topic') or '').strip()

    if not topic:
        topic = "random topic"

    print(f"Topic form client : {topic}")
    titles = _generate_slide_titles(topic)
    print(f"Titles from AI: {titles}")
    
    slides = []

    for idx, title in enumerate(titles):
       #image_url = _generate_slide_image(title, topic)
        slides.append({
            "id": idx,
            "title": title,
            "image":"https://images.unsplash.com/photo-1635070041078-e363dbe005cb?auto=format&fit=crop&w=800&q=80",
        })

    return JsonResponse({"slides": slides})