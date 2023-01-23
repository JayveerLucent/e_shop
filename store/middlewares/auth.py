from django.shortcuts import redirect

def auth_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        print(request.session.get('customer_id'))
        returnurl = request.META['PATH_INFO']
        print(returnurl)
        if not request.session.get('customer_id'):
            return redirect(f'login?return_url={returnurl}')
        
        response = get_response(request)
        return response

    return middleware