import logging
import os
from django.http import JsonResponse
from django.views.decorators.http import require_POST

logger = logging.getLogger(__name__)

@require_POST
def chatbot_response(request):
    message = request.POST.get("message", "").strip()
    if not message:
        return JsonResponse({"error": "Please enter a message."}, status=400)
    if len(message) > 1500:
        return JsonResponse({"error": "Message is too long."}, status=400)
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return JsonResponse({"error": "Gemini API key is not configured on the server."}, status=503)
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
           model=os.getenv("GEMINI_MODEL", "gemini-3.8-flash"),
            contents=message,
            config={"system_instruction": (
                "You are the Smart Parking Assistant for a Smart Car Parking System website. "
                "Answer questions about parking, booking and site navigation concisely. "
                "Do not invent live parking availability, prices, reservations or site features. "
                "Tell users to check the appropriate portal for live information."
            )},
        )
        return JsonResponse({"reply": response.text or "Sorry, I couldn't generate an answer."})
    except Exception:
        logger.exception("Gemini chatbot request failed")
        return JsonResponse({"error": "AI service unavailable. Check the Django server logs."}, status=502)
