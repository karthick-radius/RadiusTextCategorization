from dashboard.models import Business

from django.template import RequestContext

from alchemyapi.alchemyapi import AlchemyAPI

from django.shortcuts import render_to_response, get_object_or_404

alchemyapi = AlchemyAPI()


def index(request):
    context = RequestContext(request)
    return render_to_response('dashboard/index.html', {}, context)


def endpoint(request):
    global response_taxonomy, response_str
    business_name = request.POST.get('b_name')
    business_address = request.POST.get('b_address')
    business_url = request.POST.get('b_url')
    business_name = str(business_name)
    business_address = str(business_address)
    business_url = str(business_url)
    print 'business_name: '
    print business_name
    print 'business_address: '
    print business_address
    print 'business_url: '
    print business_url
    # business_url = 'http://www.romaspizzacarmichael.com/'
    """
    :type request: django.core.handlers.wsgi.wsgirequest
    """
    business_list = get_object_or_404(Business, name=business_name)

    if business_list:
        response_str = ''
        name = business_name
        category = business_list.category
        #response_keyword = alchemyapi.keywords('url', business_url)
        response_taxonomy = alchemyapi.taxonomy('text', business_name)
        response_img_extraction = alchemyapi.imageExtraction('url', business_url)
        #print response_keyword
        #print response_taxonomy
        print response_img_extraction
        #  label = ''
        label_list = ''

    if response_taxonomy['status'] == 'OK':
        for taxonomy in response_taxonomy['taxonomy']:
            print taxonomy
            score = float(taxonomy['score'])
            if score > .5 and 'label' in taxonomy:
                label = taxonomy['label'].encode('utf-8') + '(' + taxonomy['score'].encode('utf-8') + ')'
                label_list += str('''<pre><blockquote><li>%s</li></blockquote></pre>''' % label)
                print 'label_list- '
                print label_list
        response_str += str('''<pre><b>Business Name=</b> %s<br><b>Current Category=</b> %s<br><b>New Categorization using Business Name Keywords(Score)=</b> %s<br></pre>''' % (name, category, label_list))
    else:
        print('Error in taxonomy extraction call: ', response_taxonomy['statusInfo'])

    context = RequestContext(request, {
        'business_list': business_list,
    })
    return render_to_response('dashboard/results.html', {'response_str': response_str}, context)