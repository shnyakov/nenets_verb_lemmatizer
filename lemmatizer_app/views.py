from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from .core import lemmatize_many
from .forms import LemmatizerInputForm

SAMPLE_FORMS = [
    "тарпыдинзь",
    "тарпыдась",
    "тарпывась",
    "тарпыми’",
    "тарпыра’",
    "тарпыдо’",
]


@require_GET
def home(request):
    form = LemmatizerInputForm(request.GET or None)
    results = []
    submitted_text = ""
    if form.is_valid():
        submitted_text = form.cleaned_data["text"]
        if submitted_text:
            results = lemmatize_many(submitted_text)
    context = {
        "form": form,
        "results": results,
        "submitted_text": submitted_text,
        "result_count": len(results),
        "sample_forms": SAMPLE_FORMS,
        "sample_text": "\n".join(SAMPLE_FORMS[:4]),
    }
    return render(request, "lemmatizer_app/home.html", context)


@require_GET
def api_lemmatize(request):
    text = (request.GET.get("text") or "").strip()
    return JsonResponse(
        {
            "input": text,
            "results": lemmatize_many(text) if text else [],
        }
    )


@require_GET
def health(request):
    return JsonResponse({"ok": True})
