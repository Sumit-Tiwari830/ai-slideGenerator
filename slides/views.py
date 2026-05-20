from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def slide_builder(request):
    return render(request, 'slide_builder.html')


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

    titles = [
        f"Introduction to {topic}",
        f"Core ideas of {topic}",
        f"How {topic} works",
        f"Use cases of {topic}",
        f"Future of {topic}",
    ]

    slides = []

    for idx, title in enumerate(titles):
        image_url = _generate_slide_image(title, topic)

        if image_url is None:
            image_url = (
                "https://images.unsplash.com/photo-1635070041078-e363dbe005cb"
                "?auto=format&fit=crop&w=800&q=80"
            )

        slides.append({
            "id": idx,
            "title": title,
            "image": image_url,
        })

    return JsonResponse({"slides": slides})