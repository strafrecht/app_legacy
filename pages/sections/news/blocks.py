from wagtail.core import blocks

class NewsListAll(blocks.StructBlock):
    class Meta:
        template = 'blocks/widgets/news_list.html'

    def get_context(self, *a, **kw):
        ctx = super().get_context(*a, **kw)
        ctx['articles'] = NewsItem.objects.all()
        return ctx

class NewsNewsletterBlock(blocks.StructBlock):
    class Meta:
        template = 'blocks/widgets/news_newsletter.html'

    def get_context(self, *a, **kw):
        context = super().get_context(*a, **kw)
        newsletters = Document.objects.filter(tags__name='newsletter')
        semesters = []
        keys = []

        for key, group in groupby(newsletters, get_semester):
            semesters.append({"semester": key["title"], "year": key["year"], "newsletters": list(group)})

        semesters = sorted(semesters, key=lambda x: x['year'], reverse=True)
        context['semesters'] = semesters
        return context


    def get_semester(doc):
        date_string = doc.filename.split("Lehrstuhlnewsletter20vom20")[-1].split(".pdf")[0]
        d = datetime.datetime.strptime(date_string, '%d.%m.%Y')

        if d.month in [4, 5, 6, 7, 8, 9]:
            title = "SS {}".format(d.year)
            return {"title": title, "year": d.year}
        else:
            if d.month in [1, 2, 3]:
                title = "WS {}".format(d.year - 1)
                return {"title": title, "year": d.year - 1}
            else:
                title = "WS {}".format(d.year)
                return {"title": title, "year": d.year}