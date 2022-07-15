from telegram.ext import CallbackContext
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from .models import *
# Create your views here.

import xlwt
CHANNEL_TO_SEND_MESSAGE = -1001677490075
CHANNELS = [("Innovatsiyalar Milliy ofisi", -1001296579695, 'https://t.me/milliyofis'), ("INNO Technopark", -1001530051962, "https://t.me/innotechnopark")]
# CHANNELS = [("Test 1", -1001610436325, 'https://t.me/teeessttttt_1'), ("Test 2", -1001737589089, "https://t.me/test_22222222221")]


def start(update: Update, context: CallbackContext):
    user = update.effective_user
    log = Log.objects.filter(user_id=user.id).first()
    if log is None:
        log = Log()
        count = 0
        btn = []
        for i in CHANNELS:
            chat = context.bot.getChatMember(user_id=user.id, chat_id=i[1])
            if chat['status'] == 'member':
                btn.append([InlineKeyboardButton(f"✅{i[0]}", callback_data=f"{i[1]}", url=f'{i[2]}')])
                count += 1
            else:
                btn.append([InlineKeyboardButton(f"{i[0]}", callback_data=f"{i[1]}", url=f'{i[2]}')])

        btn.append([InlineKeyboardButton("✅Tekshirish", callback_data='checking')])
        if count == 2:
            log.user_id = user.id
            log.state = {'state': 0}
            update.message.reply_text("Kerakli viloyatni tanlang", reply_markup=keyboard_buttons(type='region'))
            log.save()
            return 0
        else:
            chnl_msg_id = update.message.reply_text(f"Assalomu alaykum {user.first_name}, botdan foydalanishdan oldin kanalarimizga obuna bo'lishingizni so'raymiz", reply_markup=InlineKeyboardMarkup(btn))
            log.user_id = user.id
            log.state = {'state': 0, 'chnl_msg_id': chnl_msg_id.message_id}
    else:
        log.state['state'] = 0
        update.message.reply_text("Kerakli viloyatni tanlang", reply_markup=keyboard_buttons(type='region'))
    log.save()


def received_message(update: Update, context: CallbackContext):
    user = update.effective_user
    msg = update.message.text
    log = Log.objects.filter(user_id=user.id).first()
    count = 0
    btn = []
    for i in CHANNELS:
        chat = context.bot.getChatMember(user_id=user.id, chat_id=i[1])
        if chat['status'] == 'member':
            btn.append([InlineKeyboardButton(f"✅{i[0]}", callback_data=f"{i[1]}", url=f'{i[2]}')])
            count += 1
        else:
            btn.append([InlineKeyboardButton(f"{i[0]}", callback_data=f"{i[1]}", url=f'{i[2]}')])

    btn.append([InlineKeyboardButton("✅Tekshirish", callback_data='checking')])
    if count == 2:
        pass
    else:
        chnl_msg_id = update.message.reply_text(
            f"Assalomu alaykum {user.first_name}, botdan foydalanishdan oldin kanalarimizga obuna bo'lishingizni so'raymiz", reply_markup=InlineKeyboardMarkup(btn))
        log.user_id = user.id
        main = log.state['state']
        log.state['state'] = main
        log.state['chnl_msg_id'] = chnl_msg_id.message_id
        log.save()
        return 0
    # For admin to download file
    if msg == "admin":
        update.message.reply_text("Parolni kriting")
        log.state['state'] = 21
    elif msg == "parol" and log.state['state'] == 21:
        update.message.reply_text("Parol to'g'ri kritildi✅")
        log.state['state'] = 22
        file = export_users_xls(msg)
        context.bot.send_document(chat_id=user.id, document=open(f'{file}', 'rb'))
    elif log.state['state'] == 21 and msg != "parol":
        update.message.reply_text("Parol noto'gri❌, qayatadan urinib ko'ring")
    # End of admin panel

    if msg == "⬅️Orqaga":
        log.state['state'] -= 2

    log.save()
    # main part for registration
    if log.state['state'] == 0:
        update.message.reply_text("Familiya, ism, Sharifingizni kriting", reply_markup=ReplyKeyboardRemove())
        if msg != "⬅️Orqaga":
            log.state['region'] = msg
        log.state['state'] = 1

    elif log.state['state'] == 1:
        update.message.reply_text("Tug'ilgan sanangizni kriting\n\nMasalan: 01/01/2001", reply_markup=keyboard_buttons(type='orqaga'))
        if msg != "⬅️Orqaga":
            log.state['full_name'] = msg
        log.state['state'] = 2
    elif log.state['state'] == 2:
        update.message.reply_text("Yashash manzilingizni kriting", reply_markup=keyboard_buttons(type='orqaga'))
        log.state['state'] = 3
        if msg != "⬅️Orqaga":
            log.state['birthday'] = msg
    elif log.state['state'] == 3:
        update.message.reply_text("Telefon raqamingizni kriting\n\nMasalan: +99899123456789", reply_markup=keyboard_buttons(type='phone'))
        log.state['state'] = 4
        if msg != "⬅️Orqaga":
            log.state['location'] = msg
    elif log.state['state'] == 4:
        update.message.reply_text("Talim muassasasini kriting", reply_markup=keyboard_buttons(type='orqaga'))
        log.state['state'] = 5
        if msg != "⬅️Orqaga":
            log.state['phone_number'] = msg
    elif log.state['state'] == 5:
        update.message.reply_text("Loyihani qisqacha mazmuni")
        log.state['state'] = 6
        if msg != "⬅️Orqaga":
            log.state['education'] = msg
    elif log.state['state'] == 6:
        update.message.reply_text("Loyiha nomini kriting")
        if msg != "⬅️Orqaga":
            log.state['description'] = msg
        log.state['state'] = 7
    elif log.state['state'] == 7:
        update.message.reply_text("Faylni jo'nating, hajmi 20 mb dan oshmasligi kerak")
        log.state['state'] = 8
        if msg != "⬅️Orqaga":
            log.state['project_name'] = msg
    elif log.state['state'] == 8:
        update.message.reply_text("Faylni jo'nating❌")
    elif log.state['state'] == 9 and msg == "Ha":
        info = UserInformation.objects.filter(user_id=user.id).first()
        info.region = log.state['region']
        info.full_name = log.state['full_name']
        info.birthday = log.state['birthday']
        info.location = log.state['location']
        info.phone_number = log.state['phone_number']
        info.education = log.state['education']
        info.project_name = log.state['project_name']
        info.description = log.state['description']
        info.save()
        update.message.reply_text("Barcha malumotlar yozib olindi✅", reply_markup=ReplyKeyboardRemove())

    elif log.state['state'] == 9 and msg == "Yo'q":
        log.state = {'state': 0}
        update.message.reply_text("Bekor qlindi❌")
        update.message.reply_text("Boshqatan boshlash uchun /start buyrug'ini bosing", reply_markup=ReplyKeyboardRemove())
    log.save()


def received_contact(update: Update, context: CallbackContext):
    contact = update.message.contact.phone_number
    user = update.effective_user
    log = Log.objects.filter(user_id=user.id).first()
    if log.state['state'] == 4:
        if contact.startswith('+'):
            log.state['phone_number'] = contact
        else:
            log.state['phone_number'] = f"+{contact}"
        update.message.reply_text("Ta'lim muassasasini kriting", reply_markup=keyboard_buttons(type='orqaga'))
        log.state['state'] = 5
    log.save()


def received_file(update: Update, context: CallbackContext):
    user = update.effective_user
    file = context.bot.get_file(update.message.document).download(timeout=100000)
    f = update.message.document.file_name
    print(f)
    log = Log.objects.filter(user_id=user.id).first()
    context.bot.send_document(chat_id=CHANNEL_TO_SEND_MESSAGE, document=open(f"{file}", 'rb'), caption=f"Viloyat: {log.state['region']}\n👤F.I.O: {log.state['full_name']}\n📞Raqami: {log.state['phone_number']}\n🔗Tug'ilgan sana: {log.state['birthday']}\n📍Yashash manzili: {log.state['location']}\n🏢Talim muassasasi: {log.state['education']}\n💼Loyiha nomi: {log.state['project_name']}")

    info = UserInformation.objects.filter(user_id=user.id).first()
    if info is None:
        info = UserInformation()
    if log.state['state'] == 8:
        result = f"""
Viloyat: {log.state['region']}\n
👤F.I.O: {log.state['full_name']}\n
🔗Tug'ilgan sana: {log.state['birthday']}\n
📍Yashash manzili: {log.state['location']}\n
📞Telefon raqam: {log.state['phone_number']}\n
🏢Talim muassasasi: {log.state['education']}\n
💼Loyiha nomi: {log.state['project_name']}\n
"""
        update.message.reply_text(result)
        info.file = file
        info.user_id = user.id
        info.save()
        log.state['state'] = 9
        btn = [[KeyboardButton("Ha"), KeyboardButton("Yo'q")]]
        update.message.reply_text("Barcha malumotlar to'g'rimi", reply_markup=ReplyKeyboardMarkup(btn, resize_keyboard=True))
    log.save()


def inline_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    user = query.from_user
    log = Log.objects.filter(user_id=user.id).first()
    count = 0
    btn = []
    for i in CHANNELS:
        chat = context.bot.getChatMember(user_id=user.id, chat_id=i[1])
        if chat['status'] != 'member':
            btn.append([InlineKeyboardButton(f"{i[0]}", callback_data=f"{i[1]}", url=f'{i[2]}')])
        else:
            btn.append([InlineKeyboardButton(f"✅{i[0]}", callback_data=f"{i[1]}", url=f'{i[2]}')])
            count += 1
    btn.append([InlineKeyboardButton("✅Tekshirish", callback_data='checking')])
    log.state['count'] = count
    if log.state['count'] == 2 and log.state['state'] == 0:
        context.bot.deleteMessage(chat_id=user.id, message_id=log.state['chnl_msg_id'])
        query.message.reply_text("Kerakli viloyatni tanlang", reply_markup=keyboard_buttons(type='region'))
    elif log.state['state'] != 0 and log.state['count'] == 2:
        context.bot.deleteMessage(chat_id=user.id, message_id=log.state['chnl_msg_id'])
    else:
        print("x")
        context.bot.deleteMessage(chat_id=user.id, message_id=log.state['chnl_msg_id'])
        chnl_msg_id = query.message.reply_text(f"Assalomu alaykum {user.first_name}, botdan foydalanishdan oldin kanalarimizga obuna bo'lishingizni so'raymiz", reply_markup=InlineKeyboardMarkup(btn))
        log.state['chnl_msg_id'] = chnl_msg_id.message_id
    log.save()


def keyboard_buttons(type=None):
    btn = []
    if type == 'region':
        btn = [
            [KeyboardButton("Andijon 18-19 iyul"), KeyboardButton("Namangan 20-21 iyul")],
            [KeyboardButton("Farg'ona 22-23 iyul"), KeyboardButton("Qoraqalpag'iston")],
            [KeyboardButton("Xorazm 28-29 iyul"), KeyboardButton("Buxoro 7-8 avgust")],
            [KeyboardButton("Navoiy 4-5 avgust"), KeyboardButton("Samarqand 8-9 avgust")],
            [KeyboardButton("Jizzax 11-12 avgust"), KeyboardButton("Qashqadaryo 8-9 sentabr")],
            [KeyboardButton("Surxondaryo 11-12 sentabr"), KeyboardButton("Sirdaryo 15-16 sentabr")],
            [KeyboardButton("Toshkent viloyat 18-19 sentabr")]
        ]
    elif type == "phone":
        btn = [[KeyboardButton("📞Telefon raqamni kritish", request_contact=True)], [KeyboardButton("⬅️Orqaga")]]
    elif type == "orqaga":
        btn = [[KeyboardButton("⬅️Orqaga")]]

    return ReplyKeyboardMarkup(btn, resize_keyboard=True)


def export_users_xls(request):
    # response = HttpResponse(content_type='application/ms-excel')
    # response['Content-Disposition'] = 'attachment; filename="users.xls"'

    response = 'filename: users.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Info')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Full_name', 'Birthday', 'Location', 'Phone_number', 'Education', 'Project_name', 'Description', 'File', 'Region']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = UserInformation.objects.all().values_list('full_name', 'birthday', 'location', 'phone_number', 'education', 'project_name', 'description', 'file', 'region')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response
