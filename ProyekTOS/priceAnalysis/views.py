from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
#from django.views import generic
from .models import Cabe, Bulan, Harga
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import components
from urllib2 import Request, urlopen, URLError, HTTPError
import subprocess

def index(request):
#ini handle request yang masuk
    if request.method == 'POST':
        print 'Masuk Post'
        jenis = int(request.POST.get('cabe'))
        m = int(request.POST.get('m'))
        y = int(request.POST.get('y'))
#else ini berarti default awal (input bukan merupakan pilihan user)
    else:
        jenis = 1
        m = 11
        y = 2016
#last dan lyear untuk perhitungan SMA dari bulan bulan sebelumnya
    last = m - 1
    lyear = y
    if last <= 0:
        last = 12
        lyear = y - 1
#download source sesuai request jenis cabe, bulan dan tahun
    sourceUrl = "http://infopangan.jakarta.go.id/api/price/series_by_location?public=1&type=city&lid=2&m="
    finalUrl = sourceUrl + str(m) + "&y=" + str(y)
    lastUrl = sourceUrl + str(last) + "&y=" + str(lyear)
    req = Request(finalUrl)
    req2 = Request(lastUrl)
#persiapan file untuk menampung hasil source download
    file = open('./priceAnalysis/data/source.txt','w')
    file2 = open('./priceAnalysis/data/last.txt','w')
    try:
        response = urlopen(req)
        response2 = urlopen(req2)
    except HTTPError as e:
        print 'The server couldn\'t fulfill the request.'
        print 'Error code: ', e.code
    except URLError as e:
        print 'We failed to reach a server.'
        print 'Reason: ', e.reason
    else:
        string = response.read()
        string2 = response2.read()
        file.write(string)
        file2.write(string2)
        print 'everthing is fine'
        file.close()
        file2.close()
#menjalankan shell script untuk grep dan sed (pengolahan data)
    subprocess.call('./priceAnalysis/processing.sh ./priceAnalysis/data/source',shell=True)
    subprocess.call('./priceAnalysis/processing.sh ./priceAnalysis/data/last', shell=True)
#mempersiapkan data untuk grafik dalam list
    x = [x for x in range(1,32)]
    if jenis == 1:
        f = open('./priceAnalysis/data/source1.txt','r')
        l = open('./priceAnalysis/data/last1.txt','r')
        data = f.read().split('\n')
        last = l.read().split('\n')
        f.close()
        l.close()
        y0 = [int(i) for i in data if i != data[-1]]
        late = [int(i) for i in last[-6:-1]]
    elif jenis == 2:
        f = open('./priceAnalysis/data/source2.txt','r')
        l = open('./priceAnalysis/data/last2.txt','r')
        data = f.read().split('\n')
        last = l.read().split('\n')
        f.close()
        l.close()
        y0 = [int(i) for i in data if i != data[-1]]
        late = [int(i) for i in last[-6:-1]]
#   perhitungan SMA
    late.extend(y0)
    isi = len(late)
    sma = 0
    y1 = []

    for i in range(5,isi+1):
        sma = 0
        for j in late[i-5:i]:
            sma += j
        sma /= 5
        y1.append(sma)
    y0.append(sma)
    print y0, len(y0)
    print y1, len(y1)
#mempersiapkan grafik menggunakan bokeh
    plot = figure(tools="pan,wheel_zoom,reset",
    plot_width=1000, plot_height=600,
    title="Kurva Cabe",
    x_axis_label='Tanggal', y_axis_label='Harga Cabe')
    plot.line(x, y0, legend="Harga Cabe Asli",line_color="blue")
    plot.line(x, y1, legend="Harga Cabe Perkiraan", line_color="red")
    script, div = components(plot,CDN)
    context = {'the_script':script, 'the_div':div, 'last':sma, 'jenis':jenis, 'mon':m, 'year':y}
    return render(request, 'priceAnalysis/index.html',context)

def detail(request, cabe_id):
    cabe = get_object_or_404(Cabe, pk=cabe_id)
    context = {'cabe' : cabe}
    return render(request, 'priceAnalysis/detail.html', context)

def list(request):
    all_cabe = Cabe.objects.all()
    context = {'all_cabe': all_cabe}
    return render(request,'priceAnalysis/listdata.html',context)
#class IndexView(generic.ListView):
#    template_name = 'priceAnalysis/index.html'
#    context_object_name = 'all_cabe'

#    def get_queryset(self):
#        return Cabe.objects.all()

#class DetailView(generic.DetailView):
#    model = Cabe
#    template_name = 'priceAnalysis/detail.html'

#class ListView(generic.ListView):
#    template_name = 'priceAnalysis/listdata.html'
#    context_object_name = 'all_cabe'

#    def get_queryset(self):
#        return Cabe.objects.all()
