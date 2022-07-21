from django.shortcuts import render, redirect

# Create your views here.
from bot.models import UserInformation
from telegram.ext import CallbackContext
from telegram import Update, Bot, update

CHANNEL_TO_SEND_MESSAGE = -1001610436325


def index(requests):
    info = UserInformation()
    if requests.POST and requests.FILES:
        info.full_name = requests.POST.get('full_name', '')
        info.region = requests.POST.get('region', '')
        info.birthday = requests.POST.get('birthday', '')
        info.location = requests.POST.get('location', '')
        info.phone_number = requests.POST.get('phone_number', '')
        info.education = requests.POST.get('education', '')
        info.project_name = requests.POST.get('project_name', '')
        info.description = requests.POST.get('description', '')
        info.file = requests.FILES.get('file', '')
        info.save()
        bot = Bot('5028779716:AAEWI_822MoMa8GKg2wADRNKkTBvI0eujA4')
        result = f"""
🌐Viloyat: {info.region}\n\n
👤F.I.O: {info.full_name}\n\n
📞Telefon raqam: {info.phone_number}\n\n
🔗Tug'ilgan sana: {info.birthday}\n\n
📍Yashash manzili: {info.location}\n\n
🏢Talim muassasasi: {info.education}\n\n
💼Loyiha nomi: {info.project_name}\n\n"""
        bot.send_document(chat_id=CHANNEL_TO_SEND_MESSAGE, document=open(f'media/{info.file}', 'rb'), caption=result)
        return redirect('succes')
    return render(requests, 'index.html', {'info': info})


def succes(requests):
    return render(requests, 'success.html')


def send_message(update: Update, context: CallbackContext):
    result = """Salom"""
    context.bot.send_message(chat_id=CHANNEL_TO_SEND_MESSAGE, text=result)