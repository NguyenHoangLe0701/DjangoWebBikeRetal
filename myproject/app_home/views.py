from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponseServerError
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET"])
def robots_txt(request):
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        "Disallow: /dashboard_admin/",
        "Disallow: /api/",
        "",
        "Sitemap: {}/sitemap.xml".format(request.build_absolute_uri('/')[:-1])
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")

def handler404(request, exception):
    return render(request, 'errors/404.html', status=404)

def handler500(request):
    return render(request, 'errors/500.html', status=500)

def handler403(request, exception):
    return render(request, 'errors/403.html', status=403)
