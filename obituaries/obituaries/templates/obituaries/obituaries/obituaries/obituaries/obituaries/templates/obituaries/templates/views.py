from django.views.generic import DetailView

class ObituaryDetailView(DetailView):
    model = Obituary
    template_name = 'obituaries/obituary_detail.html'
    context_object_name = 'obituary'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obituary = self.get_object()
        
        # SEO meta tags
        context['meta_description'] = f"Obituary for {obituary.name} ({obituary.date_of_birth} - {obituary.date_of_death}). {obituary.content[:160]}..."
        context['meta_keywords'] = f"obituary, {obituary.name}, memorial, remembrance, death notice"
        
        # Open Graph/Twitter meta tags
        context['og_title'] = f"Obituary for {obituary.name}"
        context['og_description'] = f"Remembering {obituary.name} ({obituary.date_of_birth} - {obituary.date_of_death})"
        context['twitter_title'] = f"Obituary for {obituary.name}"
        context['twitter_description'] = f"Remembering {obituary.name} ({obituary.date_of_birth} - {obituary.date_of_death})"
        
        # Structured data (schema.org)
        context['structured_data'] = {
            "@context": "https://schema.org",
            "@type": "Obituary",
            "name": obituary.name,
            "birthDate": obituary.date_of_birth.isoformat(),
            "deathDate": obituary.date_of_death.isoformat(),
            "description": obituary.content,
            "author": {
                "@type": "Person",
                "name": obituary.author
            },
            "datePublished": obituary.submission_date.isoformat()
        }
        
        return context
