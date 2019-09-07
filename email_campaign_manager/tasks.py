from celery.schedules import crontab

from email_campaign_manager.models import Subscriber, Campaign
from finception.settings import API_BASE_URL, API_KEY
import requests
from finception.celery import app

@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour=10, minute=0), send_campaign_emails.s())

@app.task
def email_helper(receiver: list, subject: str, pre_text: str,article_url: str,plain_text: str, html: str, pub_date: str) -> int:
    body = pre_text+"\n"+article_url+"\n"+plain_text+"\n Published on: "+pub_date
    _body = pre_text + "<br>" + article_url + "<br>" + plain_text + "<br> Published on: " + pub_date
    res = requests.post(
        API_BASE_URL,
        auth=("api", API_KEY),
        data={
            "from": "jprrahultiwari@gmail.com",
            "to": receiver,
            "subject": subject,
            "text": body,
            "html": _body+html
        }
    )
    return res.status_code


@app.task
def send_campaign_emails():
    subs = Subscriber.objects.filter(is_active=True)
    campaigns = Campaign.objects.filter(sent=False)
    for sub in subs:
        for camp in campaigns:
            res = email_helper.delay([sub.email], camp.subject, camp.pre_text, camp.article_url,
                                             camp.plain_text, camp.html_content, str(camp.pub_date))
            camp.sent = True
            camp.save()
    return

@app.task
def test():
    print("Matata")



