from core import settings
from paymentwall.base import Paymentwall
from paymentwall.widget import Widget
from paymentwall.pingback import Pingback
from django.utils.decorators import method_decorator
#from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.http import HttpResponse
from apps.account.models import Account

Paymentwall.set_api_type(Paymentwall.API_VC)
Paymentwall.set_app_key(settings.PAYMENTWALL_PUBLIC_KEY) # available in your merchant area
Paymentwall.set_secret_key(settings.PAYMENTWALL_PRIVATE_KEY) # available in your merchant area

def PayWidget(usuario,email):
    widget = Widget(
        usuario,
        'p1_4',
        [],
        {
            'email':email,
            'ps':'all',
        },
    )
    return widget.get_url()


#@method_decorator(csrf_exempt, name='dispatch')
class PaymentwallCallbackView(View):

    def __get_request_ip(self):
        return self.request.META.get('HTTP_X_FORWARDED_FOR')

    def get(self, request, *args, **kwargs):
        pingback = Pingback(request.GET.copy(), self.__get_request_ip())

        if pingback.validate():
            virtual_currency = pingback.get_vc_amount()
            if pingback.is_deliverable():
                try:
                    a = Account.objects.get(login=pingback.get_user_id())
                except:
                    pass

                a.coins = int(a.coins) + int(virtual_currency)
                a.save()

            elif pingback.is_cancelable():
                if int(virtual_currency) < 0:
                    try:
                        a = Account.objects.get(login=pingback.get_user_id())
                    except:
                        pass

                    a.coins = int(a.coins) - abs(int(virtual_currency))
                    a.save()

            else:
                print('Paymentwall pingback: Unknown pingback type, Paymentwall sent this data: {}'.format(request.GET.copy()))

            return HttpResponse('OK', status=200)
        else:
            print('Paymentwall pingback: Cant validate pingback, error: {} Paymentwall sent this data: {}'.format(pingback.get_error_summary(), request.GET.copy()))
