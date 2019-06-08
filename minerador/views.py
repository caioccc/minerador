from threading import Thread

from django.views.generic import TemplateView

from minerador.miner.explorer import mineData, syncTracks


class IndexView(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        Thread(target=mineData).start()
        Thread(target=syncTracks).start()
        return super(IndexView, self).get(request, *args, **kwargs)
