from django.shortcuts import render
from email_campaign_manager.models import Subscriber, Campaign
from email_campaign_manager.tasks import send_campaign_emails
import datetime

def create_campaign(request):
    if request.method == "POST":
        subject = request.POST["subject"]
        pre_text = request.POST["pre-text"]
        article_url = request.POST["article-url"]
        html_content = request.POST["html-content"]
        plain_text = request.POST["plain-text"]
        pub_date = request.POST["pub-date"]
        pub_date = datetime.datetime.strptime(pub_date, '%Y-%M-%d').date()
        campaign = Campaign(subject=subject, pre_text=pre_text, article_url=article_url, html_content=html_content,
                            plain_text=plain_text, pub_date=pub_date)
        campaign.save()
        return render(request, 'success.html', {"msg": "Campaign created successfully"})

    return render(request, 'base.html')


def send_email(request):
    if request.method == "POST":
        send_campaign_emails.delay()
        return render(request, 'success.html', {"msg": "Emails queued successfully"})

    return render(request, 'send.html')


def unsub(request):
    if request.method == "POST":
        user_email = request.POST["email"]
        user = Subscriber.objects.filter(email=user_email)
        if user:
            print(user[0])
            user[0].is_active = False
            user[0].save()
            return render(request, "success.html", {"msg": " You have been successfully unsubscribed!"})
        return render(request, "error.html", {"msg": "User not in the mailing list"})
    return render(request, "unsub.html")
