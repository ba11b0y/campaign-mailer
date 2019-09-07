from django.conf.urls import url
from email_campaign_manager.views import send_email, unsub, create_campaign

urlpatterns = [
    url(r'send-email/', send_email, name='send_email'),
    url(r'create-campaign/', create_campaign, name='create_campaign'),
    url(r'unsubscribe/', unsub, name='unsub'),
]
