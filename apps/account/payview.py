from core import settings
from paymentwall.base import Paymentwall
from paymentwall.widget import Widget

Paymentwall.set_api_type(Paymentwall.API_VC)
Paymentwall.set_app_key(settings.PAYMENTWALL_PUBLIC_KEY) # available in your merchant area
Paymentwall.set_secret_key(settings.PAYMENTWALL_PRIVATE_KEY) # available in your merchant area

def PayWidget(usuario,email):
    widget = Widget(
        usuario,
        'p1_3',
        [],
        {
            'email':email,
            'ps':'all'
        }
    )
    return widget.get_url()

def ProcessPay(request):
    pingback = Pingback({x:y for x, y in request.args.iteritems()}, request.remote_addr)
    if pingback.validate():
        virtual_currency = pingback.get_vc_amount()
        if pingback.is_deliverable():
            # deliver the virtual currency
            print(virtual_currency)
            
        elif pingback.is_cancelable():
            # withdraw the virtual currency
            pass
        print('OK') # Paymentwall expects response to be OK, otherwise the pingback will be resent
    else:
        print(pingback.get_error_summary())
