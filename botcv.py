import os
import pandas as pd
import vobject
from telegram import ReplyKeyboardRemove
from telegram import ReplyKeyboardMarkup
from telegram import Update, InputFile
from telegram.ext import Application, ConversationHandler, CommandHandler, MessageHandler, filters, CallbackContext
import logging
import re

def format_phone_number(phone_number: str) -> str:
    # Hapus semua karakter spasi, tanda hubung, dan tanda "+"
    phone_number = phone_number.replace(" ", "").replace("-", "").replace("+", "")
    
    # Pengecekan berdasarkan awalan kode negara
    if phone_number.startswith('1'):  # USA & Canada
        return f"+1 ({phone_number[1:4]}) {phone_number[4:7]}-{phone_number[7:]}"
    
    elif phone_number.startswith('44'):  # UK
        return f"+44 {phone_number[2:5]} {phone_number[5:9]} {phone_number[9:]}"
    
    elif phone_number.startswith('62'):  # Indonesia
        return f"+62 {phone_number[2:6]}-{phone_number[6:]}"
    
    elif phone_number.startswith('91'):  # India
        return f"+91 {phone_number[2:7]} {phone_number[7:]}"
    
    elif phone_number.startswith('7'):  # Russia
        return f"+7 ({phone_number[1:4]}) {phone_number[4:7]}-{phone_number[7:]}"
    
    elif phone_number.startswith('81'):  # Japan
        return f"+81 {phone_number[2:5]}-{phone_number[5:8]}-{phone_number[8:]}"
    
    elif phone_number.startswith('86'):  # China
        return f"+86 {phone_number[2:5]} {phone_number[5:8]} {phone_number[8:]}"
    
    elif phone_number.startswith('60'):  # Malaysia
        return f"+60 {phone_number[2:4]} {phone_number[4:6]} {phone_number[6:]}"
    
    elif phone_number.startswith('65'):  # Singapore
        return f"+65 {phone_number[2:6]} {phone_number[6:]}"
    
    elif phone_number.startswith('971'):  # UAE
        return f"+971 {phone_number[3:5]} {phone_number[5:8]} {phone_number[8:]}"
    
    elif phone_number.startswith('852'):  # Hong Kong
        return f"+852 {phone_number[3:7]}-{phone_number[7:]}"
    
    elif phone_number.startswith('93'):  # Afghanistan
        return f"+93 {phone_number[2:5]} {phone_number[5:]}"
    
    elif phone_number.startswith('55'):  # Brazil
        return f"+55 {phone_number[2:4]} {phone_number[4:8]}-{phone_number[8:]}"
    
    elif phone_number.startswith('54'):  # Argentina
        return f"+54 {phone_number[2:6]}-{phone_number[6:]}"
    
    elif phone_number.startswith('61'):  # Australia
        return f"+61 {phone_number[2:5]} {phone_number[5:8]} {phone_number[8:]}"
    
    elif phone_number.startswith('33'):  # France
        return f"+33 {phone_number[2:4]} {phone_number[4:6]} {phone_number[6:]}"
    
    elif phone_number.startswith('49'):  # Germany
        return f"+49 {phone_number[2:5]} {phone_number[5:8]} {phone_number[8:]}"
    
    elif phone_number.startswith('39'):  # Italy
        return f"+39 {phone_number[2:5]} {phone_number[5:8]} {phone_number[8:]}"
    
    elif phone_number.startswith('34'):  # Spain
        return f"+34 {phone_number[2:5]} {phone_number[5:]}"
    
    elif phone_number.startswith('52'):  # Mexico
        return f"+52 {phone_number[2:4]} {phone_number[4:7]}-{phone_number[7:]}"
    
    elif phone_number.startswith('27'):  # South Africa
        return f"+27 {phone_number[2:5]} {phone_number[5:8]} {phone_number[8:]}"
    
    elif phone_number.startswith('66'):  # Thailand
        return f"+66 {phone_number[2:5]} {phone_number[5:7]} {phone_number[7:]}"
    
    elif phone_number.startswith('90'):  # Turkey
        return f"+90 {phone_number[2:5]} {phone_number[5:8]} {phone_number[8:]}"
    
    elif phone_number.startswith('82'):  # South Korea
        return f"+82 {phone_number[2:5]} {phone_number[5:8]} {phone_number[8:]}"
    
    elif phone_number.startswith('63'):  # Philippines
        return f"+63 {phone_number[2:5]} {phone_number[5:]}"
    
    elif phone_number.startswith('31'):  # Netherlands
        return f"+31 {phone_number[2:5]} {phone_number[5:]}"
    
    elif phone_number.startswith('234'):  # Nigeria
        return f"+234 {phone_number[3:6]} {phone_number[6:]}"
    
    elif phone_number.startswith('254'):  # Kenya
        return f"+254 {phone_number[3:6]} {phone_number[6:]}"
    
    elif phone_number.startswith('256'):  # Uganda
        return f"+256 {phone_number[3:6]} {phone_number[6:]}"
    
    elif phone_number.startswith('92'):  # Pakistan
        return f"+92 {phone_number[2:5]} {phone_number[5:]}"
    
    elif phone_number.startswith('258'):  # Mozambique
        return f"+258 {phone_number[3:6]} {phone_number[6:]}"
    
    elif phone_number.startswith('249'):  # Sudan
        return f"+249 {phone_number[3:6]} {phone_number[6:]}"
    
    elif phone_number.startswith('213'):  # Algeria
        return f"+213 {phone_number[3:6]} {phone_number[6:]}"
    
    elif phone_number.startswith('27'):  # South Africa
        return f"+27 {phone_number[2:5]} {phone_number[5:8]} {phone_number[8:]}"
    
    elif phone_number.startswith('212'):  # Morocco
        return f"+212 {phone_number[3:6]} {phone_number[6:]}"
    
    elif phone_number.startswith('216'):  # Tunisia
        return f"+216 {phone_number[3:6]} {phone_number[6:]}"
    
    elif phone_number.startswith('234'):  # Nigeria
        return f"+234 {phone_number[3:6]} {phone_number[6:]}"
    
    elif phone_number.startswith('256'):  # Uganda
        return f"+256 {phone_number[3:6]} {phone_number[6:]}"
    
    elif phone_number.startswith('260'):  # Zambia
        return f"+260 {phone_number[3:6]} {phone_number[6:]}"
    
    elif phone_number.startswith('91'):  # India
        return f"+91 {phone_number[2:5]} {phone_number[5:]}"
    
    elif phone_number.startswith('92'):  # Pakistan
        return f"+92 {phone_number[2:5]} {phone_number[5:]}"
    
    elif phone_number.startswith('966'):  # Saudi Arabia
        return f"+966 {phone_number[3:6]} {phone_number[6:]}"
    
    elif phone_number.startswith('971'):  # UAE
        return f"+971 {phone_number[3:6]} {phone_number[6:]}"
    
    elif phone_number.startswith('98'):  # Iran
        return f"+98 {phone_number[2:5]} {phone_number[5:]}"
    
    elif phone_number.startswith('20'):  # Egypt
        return f"+20 {phone_number[2:5]} {phone_number[5:]}"
    
    elif phone_number.startswith('968'):  # Oman
        return f"+968 {phone_number[3:6]} {phone_number[6:]}"
    
    elif phone_number.startswith('84'):  # Vietnam
        return f"+84 {phone_number[2:5]} {phone_number[5:]}"
    
    elif phone_number.startswith('880'):  # Bangladesh
        return f"+880 {phone_number[3:6]} {phone_number[6:]}"
    
    elif phone_number.startswith('977'):  # Nepal
        return f"+977 {phone_number[3:6]} {phone_number[6:]}"
    
    else:  # Jika kode negara tidak terdaftar, kembalikan dengan tanda "+"
        return f"+{phone_number}"




# Konfigurasi logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ID pengguna yang diizinkan
ALLOWED_USER_IDS = [6870143948]

# Folder untuk menyimpan unggahan dan hasil VCF
UPLOAD_FOLDER = 'uploads'
VCF_FOLDER = 'vcf_results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(VCF_FOLDER, exist_ok=True)

# Dekorator untuk memeriksa izin pengguna
def check_user_permission(func):
    async def wrapper(update: Update, context: CallbackContext):
        user_id = update.effective_user.id
        if user_id in ALLOWED_USER_IDS:
            await func(update, context)
        else:
            await update.message.reply_text("Anda tidak memiliki izin untuk akses ke bot ini.")
            logger.warning(f"Unauthorized access attempt by user ID: {user_id}")
    return wrapper

@check_user_permission
async def add_user(update: Update, context: CallbackContext):
    if len(context.args) < 1:
        await update.message.reply_text("Silakan berikan ID pengguna yang ingin ditambahkan. Contoh: /adduser 123456789 987654321")
        return

    added_users = []
    already_added_users = []
    
    for arg in context.args:
        try:
            new_user_id = int(arg)
            global ALLOWED_USER_IDS
            
            if new_user_id not in ALLOWED_USER_IDS:
                ALLOWED_USER_IDS.append(new_user_id)
                added_users.append(new_user_id)
            else:
                already_added_users.append(new_user_id)
        except ValueError:
            await update.message.reply_text(f"ID pengguna '{arg}' harus berupa angka. Contoh: /adduser 123456789 987654321")

    if added_users:
        await update.message.reply_text(f"ID pengguna {', '.join(map(str, added_users))} telah ditambahkan ke daftar pengguna yang diizinkan.")
    
    if already_added_users:
        await update.message.reply_text(f"ID pengguna {', '.join(map(str, already_added_users))} sudah ada dalam daftar pengguna yang diizinkan.")

@check_user_permission
async def remove_user(update: Update, context: CallbackContext):
    if len(context.args) != 1:
        await update.message.reply_text("Silakan berikan ID pengguna yang ingin dihapus. Contoh: /removeuser 123456789")
        return

    try:
        remove_user_id = int(context.args[0])
        if remove_user_id in ALLOWED_USER_IDS:
            ALLOWED_USER_IDS.remove(remove_user_id)
            await update.message.reply_text(f"ID pengguna {remove_user_id} telah dihapus dari daftar pengguna yang diizinkan.")
        else:
            await update.message.reply_text(f"ID pengguna {remove_user_id} tidak ditemukan dalam daftar pengguna yang diizinkan.")
    except ValueError:
        await update.message.reply_text("ID pengguna harus berupa angka. Contoh: /removeuser 123456789")


@check_user_permission
async def remove_user(update: Update, context: CallbackContext):
    if len(context.args) != 1:
        await update.message.reply_text("Silakan berikan ID pengguna yang ingin dihapus. Contoh: /removeuser 123456789")
        return

    try:
        remove_user_id = int(context.args[0])
        if remove_user_id in ALLOWED_USER_IDS:
            ALLOWED_USER_IDS.remove(remove_user_id)
            await update.message.reply_text(f"ID pengguna {remove_user_id} telah dihapus dari daftar pengguna yang diizinkan.")
        else:
            await update.message.reply_text(f"ID pengguna {remove_user_id} tidak ditemukan dalam daftar pengguna yang diizinkan.")
    except ValueError:
        await update.message.reply_text("ID pengguna harus berupa angka. Contoh: /removeuser 123456789")

@check_user_permission
async def list_users(update: Update, context: CallbackContext):
    if ALLOWED_USER_IDS:
        user_list = "\n".join(str(user_id) for user_id in ALLOWED_USER_IDS)
        await update.message.reply_text(f"Daftar pengguna yang diizinkan:\n{user_list}")
    else:
        await update.message.reply_text("Tidak ada pengguna yang diizinkan.")



# Fungsi untuk mereset pengaturan
@check_user_permission
async def reset_settings(update: Update, context: CallbackContext):
    context.user_data.clear()
    await update.message.reply_text("Pengaturan telah direset ke default.")
    logger.info("User  settings have been reset to default.")

# Fungsi untuk memulai bot
@check_user_permission
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Halo! Selamat menggunakan bot ini.\n"
                                    "Kirimkan File yang akan di konversi.")
    logger.info("Bot started by user.")


@check_user_permission
async def handle_file(update: Update, context: CallbackContext):
    if update.message.document:
        document = update.message.document
        file_id = document.file_id
        file = await context.bot.get_file(file_id)
        file_path = os.path.join(UPLOAD_FOLDER, document.file_name)

        try:
            # Mengunduh file ke direktori unggahan
            await file.download_to_drive(file_path)
            logger.info(f"File downloaded to {file_path}")

            # Simpan informasi file ke user_data
            if 'files' not in context.user_data:
                context.user_data['files'] = []

            context.user_data['files'].append({
                'file_path': file_path,
                'file_name': document.file_name
            })

            # Hitung jumlah baris dalam file TXT
            if document.file_name.endswith('.txt'):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        line_count = sum(1 for line in f)
                    await update.message.reply_text(
                        f"File '{document.file_name}' telah diunggah. Jumlah Kontak: {line_count}. "
                        f"Silakan reply file ini dengan format: <nama kontak>,<nama file vcf>,<jumlah kontak>,<jumlah file>,<angka untuk nama file>"
                    )
                except UnicodeDecodeError:
                    # Jika terjadi kesalahan decoding, coba dengan encoding lain
                    try:
                        with open(file_path, 'r', encoding='ISO-8859-1') as f:
                            line_count = sum(1 for line in f)
                        await update.message.reply_text(
                            f"File '{document.file_name}' telah diunggah. Jumlah Kontak: {line_count}. "
                            f"Silakan reply file ini dengan format: <nama kontak>,<nama file vcf>,<jumlah kontak>,<jumlah file>,<angka untuk nama file>"
                        )
                    except Exception as e:
                        await update.message.reply_text(f"Error membaca file: {str(e)}")
                        logger.error(f"Error reading file {file_path}: {str(e)}")
            else:
                await update.message.reply_text(
                    f"File '{document.file_name}' telah diunggah. "
                    f"Silakan reply file ini dengan format: <nama kontak>,<nama file vcf>,<jumlah kontak>,<jumlah file>,<angka untuk nama file>"
                )

        except Exception as e:
            await update.message.reply_text(f"Error mengunduh file: {str(e)}")
            logger.error(f"Error downloading file {file_path}: {str(e)}")
            
@check_user_permission
async def process_file_command(update: Update, context: CallbackContext):
    if update.message.reply_to_message and update.message.reply_to_message.document:
        user_id = update.effective_user.id
        if 'files' not in context.user_data or not context.user_data['files']:
            await update.message.reply_text("Tidak dapat menemukan file yang diunggah. Silakan unggah ulang file dan coba lagi.")
            return

        # Ambil file berdasarkan nama dokumen dari pesan balasan
        reply_file_name = update.message.reply_to_message.document.file_name
        selected_file = next((f for f in context.user_data['files'] if f['file_name'] == reply_file_name), None)

        if not selected_file:
            await update.message.reply_text("File yang Anda referensikan tidak ditemukan.")
            return

        try:
            # Mengambil parameter dari pesan pengguna
            args = update.message.text.split(',')
            if len(args) != 5:  # Memastikan ada lima argumen
                await update.message.reply_text("Format tidak valid. Contoh yang benar: Nama Kontak, nama file.vcf, jumlah kontak, jumlah file, angka nama file")
                return

            contact_name = args[0].strip()
            vcf_file_name = args[1].strip()
            split_size = int(args[2].strip())
            num_files = int(args[3].strip())
            start_number = int(args[4].strip())  # Nomor awal untuk penamaan file

            file_path = selected_file['file_path']
            file_extension = os.path.splitext(file_path)[1].lower()

          # Proses file berdasarkan tipe file
            dataframe = None
            if file_extension == '.txt':
                encodings = ['utf-8', 'utf-16', 'latin-1']
                lines = None
                for encoding in encodings:
                    try:
                        with open(file_path, 'r', encoding=encoding) as f:
                            lines = f.readlines()
                            break
                    except (UnicodeDecodeError, FileNotFoundError):
                        continue

                if lines is None:
                    raise ValueError("Gagal membaca file dengan encoding yang dikenal.")

                contacts = []
                current_category = None
                counter = 1
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    if line.isalpha():
                        current_category = line
                        counter = 1
                    else:
                        if current_category is not None:
                            contacts.append({'name': f"{current_category} {counter}", 'phonenumber': line})
                            counter += 1
                        else:
                            contacts.append({'name': f"Contact {counter}", 'phonenumber': line})
                            counter += 1

                dataframe = pd.DataFrame(contacts)
            elif file_extension == '. csv':
                dataframe = pd.read_csv(file_path)
            elif file_extension in ['.xls', '.xlsx']:
                dataframe = pd.read_excel(file_path)
            else:
                await update.message.reply_text("Format file tidak didukung. Harap unggah file dalam format TXT, CSV, atau Excel.")
                logger.warning(f"Unsupported file format: {file_extension}")
                return

            if dataframe is not None:
                logger.info(f"Processed file into dataframe with {len(dataframe)} entries")

                # Bagi dataframe menjadi beberapa bagian sesuai instruksi
                start_idx = 0
                for idx in range(num_files):
                    if start_idx >= len(dataframe):
                        break
                    end_idx = start_idx + split_size
                    df_chunk = dataframe.iloc[start_idx:end_idx]

                    if df_chunk.empty:
                        break

                    vcf_data = convert_to_vcf(df_chunk, contact_name)
                    vcf_file_chunk_name = f"{vcf_file_name.rsplit('.', 1)[0]}{start_number + idx}.vcf"  # Ganti penomoran
                    vcf_file_path = os.path.join(VCF_FOLDER, vcf_file_chunk_name)

                    # Membuat path file agar sesuai dengan sistem operasi
                    vcf_file_path = os.path.normpath(vcf_file_path)

                    with open(vcf_file_path, 'w', encoding='utf-8') as vcf_file:
                        vcf_file.write(vcf_data)

                    with open(vcf_file_path, 'rb') as vcf_file:
                        await update.message.reply_document(document=InputFile(vcf_file), filename=vcf_file_chunk_name)
                        logger.info(f"Sent file: {vcf_file_chunk_name}")

                    start_idx = end_idx

        except ValueError as ve:
            await update.message.reply_text(f"Error: {str(ve)}")
            logger.error(f"Value error: {str(ve)}")
        except Exception as e:
            await update.message.reply_text(f"Error membaca file: {str(e)}")
            logger.error(f"Error reading file {file_path}: {str(e)}")
        finally:
            # Bersihkan setelah memproses
            if os.path.exists(selected_file['file_path']):
                os.remove(selected_file['file_path'])
            context.user_data['files'].remove(selected_file)
            for file_name in os.listdir(VCF_FOLDER):
                file_path = os.path.join(VCF_FOLDER, file_name)
                if os.path.isfile(file_path):
                    os.remove(file_path) 
                    
# Fungsi untuk mengonversi dataframe ke format VCF
def convert_to_vcf(dataframe, contact_name_prefix=''):
    vcf_list = []
    for idx, row in dataframe.iterrows():
        vcard = vobject.vCard()
        contact_name = str(row['name']).strip()
        phone_number = format_phone_number(str(row['phonenumber']).strip())

        # Menyusun nama kontak sesuai dengan prefiks yang diberikan
        if contact_name_prefix:
            match = re.match(r"^(.*?)(\d+)?$", contact_name_prefix)
            base_name = match.group(1)
            number = match.group(2)
            if number:
                contact_name = f"{base_name}{number}"
                contact_name_prefix = f"{base_name}{int(number) + idx + 1:03d}"
            else:
                contact_name = f"{contact_name_prefix}-{idx + 1:03d}".strip()

        vcard.add('fn').value = contact_name
        
        if phone_number:
            tel = vcard.add('tel')
            tel.value = phone_number
            tel.type_param = 'CELL'
        
        vcf_list.append(vcard.serialize())
    return "\n".join(vcf_list)
    
# Fungsi untuk memecah file VCF
def split_vcf_file(file_path, num_contacts_per_file):
    with open(file_path, 'r') as f:
        vcf_content = f.read()

    vcf_cards = vcf_content.strip().split("END:VCARD")
    vcf_cards = [card + "\nEND:VCARD" for card in vcf_cards if card.strip()]

    split_files = [vcf_cards[i:i + num_contacts_per_file] for i in range(0, len(vcf_cards), num_contacts_per_file)]

    return ["\n".join(split_file) for split_file in split_files]

@check_user_permission
async def handle_split_vcf_command(update: Update, context: CallbackContext):
    if not context.args:
        await update.message.reply_text("Harap berikan jumlah kontak per file. Contoh: /pecahvcf 100")
        return

    try:
        num_contacts_per_file = int(context.args[0])
        
        if 'files' not in context.user_data or not context.user_data['files']:
            await update.message.reply_text("Tidak ada file VCF yang diunggah. Silakan unggah file VCF terlebih dahulu.")
            return

        # Ambil file terakhir yang diunggah
        selected_file = context.user_data['files'][-1]
        file_path = selected_file['file_path']
        file_name = selected_file['file_name']

        # Memecah file VCF berdasarkan jumlah kontak per file
        split_files = split_vcf_file(file_path, num_contacts_per_file)

        for idx, split_file in enumerate(split_files):
            split_file_path = os.path.join(VCF_FOLDER, f"{os.path.splitext(file_name)[0]}_{idx + 1}.vcf")
            with open(split_file_path, 'w') as f:
                f.write(split_file)

            # Mengirimkan file yang sudah dipecah ke pengguna
            with open(split_file_path, 'rb') as vcf_file:
                await update.message.reply_document(document=InputFile(vcf_file), filename=os.path.basename(split_file_path))

        await update.message.reply_text(f"File VCF telah dipecah menjadi {len(split_files)} file.")

    except ValueError:
        await update.message.reply_text("Jumlah kontak per file harus berupa angka. Contoh: /pecahvcf 100")
    except Exception as e:
        await update.message.reply_text(f"Terjadi kesalahan: {str(e)}")
    finally:
        # Menghapus file setelah dikirim
        if os.path.exists(file_path):
            os.remove(file_path)
        for file_name in os.listdir(VCF_FOLDER):
            file_path = os.path.join(VCF_FOLDER, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
            

# Fungsi untuk memproses perintah /admin
@check_user_permission
async def admin_command(update: Update, context: CallbackContext):
    await update.message.reply_text("Silakan masukkan nomor telepon admin (Berikan nomor telp berurut ke bawah):")
    context.user_data['admin_step'] = 'awaiting_admin_phone'


# Fungsi untuk menangani langkah-langkah /admin
@check_user_permission
async def handle_admin_steps(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if 'admin_step' not in context.user_data:
        return

    step = context.user_data['admin_step']
    text = update.message.text.strip()

    if step == 'awaiting_admin_phone':
        admin_phones = [phone.strip() for phone in re.split(r'[\s,]+', text) if re.match (r"^\+?\d{7,15}$", phone.strip())]
        if not admin_phones:
            await update.message.reply_text("Nomor telepon tidak valid. Harap masukkan nomor telepon yang benar (Berikan no telp berurut ke bawah):")
            return
        context.user_data['admin_phones'] = admin_phones
        context.user_data['admin_step'] = 'awaiting_navy_phone'
        await update.message.reply_text("Silakan masukkan nomor telepon navy (Berikan no telp berurut ke bawah):")

    elif step == 'awaiting_navy_phone':
        navy_phones = [phone.strip() for phone in re.split(r'[\s,]+', text) if re.match(r"^\+?\d{7,15}$", phone.strip())]
        if not navy_phones:
            await update.message.reply_text("Nomor telepon tidak valid. Harap masukkan nomor telepon yang benar (Berikan no telp berurut ke bawah):")
            return
        context.user_data['navy_phones'] = navy_phones
        context.user_data['admin_step'] = 'awaiting_admin_name'
        await update.message.reply_text("Silakan masukkan nama kontak untuk admin:")

    elif step == 'awaiting_admin_name':
        context.user_data['admin_name'] = text
        context.user_data['admin_step'] = 'awaiting_navy_name'
        await update.message.reply_text("Silakan masukkan nama kontak untuk navy:")

    elif step == 'awaiting_navy_name':
        context.user_data['navy_name'] = text
        context.user_data['admin_step'] = 'awaiting_vcf_file_name'
        await update.message.reply_text("Silakan masukkan nama untuk file VCF:")

    elif step == 'awaiting_vcf_file_name':
        vcf_file_name = text
        if not vcf_file_name.endswith('.vcf'):
            vcf_file_name += '.vcf'
        context.user_data['vcf_file_name'] = vcf_file_name
        
        admin_contacts = [{
            'name': f"{context.user_data['admin_name']} {i+1}",
            'phonenumber': phone
        } for i, phone in enumerate(context.user_data['admin_phones'])]
        
        navy_contacts = [{
            'name': f"{context.user_data['navy_name']} {i+1}",
            'phonenumber': phone
        } for i, phone in enumerate(context.user_data['navy_phones'])]
        
        contacts = admin_contacts + navy_contacts
        dataframe = pd.DataFrame(contacts)
        vcf_data = convert_to_vcf(dataframe)
        vcf_file_path = os.path.join(VCF_FOLDER, vcf_file_name)

        with open(vcf_file_path, 'w', encoding='utf-8') as vcf_file:
            vcf_file.write(vcf_data)

        with open(vcf_file_path, 'rb') as vcf_file:
            await update.message.reply_document(document=InputFile(vcf_file), filename=vcf_file_name)
            # Menghapus file setelah dikirim
            if os.path.exists(vcf_file_path):
                os.remove(vcf_file_path)
        
        # Reset admin step
        context.user_data.pop('admin_step', None)
        await update.message.reply_text("File VCF telah dibuat dan dikirim.", reply_markup=ReplyKeyboardRemove())
        


@check_user_permission
async def vcf_to_txt(update: Update, context: CallbackContext):
    if 'files' not in context.user_data or not context.user_data['files']:
        await update.message.reply_text("Tidak ada file VCF yang diunggah. Silakan unggah file VCF terlebih dahulu.")
        return

    # Ambil semua file yang diunggah
    vcf_files = context.user_data['files']
    txt_files = []

    for selected_file in vcf_files:
        file_path = selected_file['file_path']
        file_extension = os.path.splitext(file_path)[1].lower()

        if file_extension != '.vcf':
            await update.message.reply_text(f"Format file tidak valid untuk {file_path}. Harap unggah file VCF.")
            continue

        try:
            phone_numbers = []
            with open(file_path, 'r', encoding='utf-8') as vcf_file:
                for line in vcf_file:
                    if line.startswith("TEL"):
                        phone_number = line.split(":")[1].strip()
                        phone_numbers.append(phone_number)

            txt_file_name = f"{os.path.splitext(os.path.basename(file_path))[0]}.txt"
            txt_file_path = os.path.join(UPLOAD_FOLDER, txt_file_name)

            with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
                for number in phone_numbers:
                    txt_file.write(number + '\n')

            txt_files.append(txt_file_path)

        except Exception as e:
            await update.message.reply_text(f"Klik /reset jika Gagal mengkonversi file VCF ke TXT: {str(e)}")
            continue

    # Kirim semua file TXT yang dihasilkan
    for txt_file_path in txt_files:
        with open(txt_file_path, 'rb') as txt_file:
            await update.message.reply_document(document=InputFile(txt_file), filename=os.path.basename(txt_file_path))

    # Pembersihan file
    for selected_file in vcf_files:
        if os.path.exists(selected_file['file_path']):
            os.remove(selected_file['file_path'])
    for txt_file_path in txt_files:
        if os.path.exists(txt_file_path):
            os.remove(txt_file_path)



@check_user_permission
async def merge_txt_files(update: Update, context: CallbackContext):
    if update.message.reply_to_message and update.message.reply_to_message.document:
        user_id = update.effective_user.id
        if 'files' not in context.user_data or not context.user_data['files']:
            await update.message.reply_text("Tidak dapat menemukan file yang diunggah. Silakan unggah ulang file dan coba lagi.")
            return

        reply_file_name = update.message.reply_to_message.document.file_name
        selected_files = [f for f in context.user_data['files'] if f['file_name'].endswith('.txt')]

        if not selected_files:
            await update.message.reply_text("Tidak ada file TXT yang diunggah. Silakan unggah file TXT dan coba lagi.")
            return

        try:
            output_file_path = os.path.join(UPLOAD_FOLDER, 'file gabungan.txt')
            with open(output_file_path, 'w') as output_file:
                for file in selected_files:
                    file_path = file['file_path']
                    with open(file_path, 'r') as input_file:
                        output_file.write(input_file.read())

            with open(output_file_path, 'rb') as output_file:
                await update.message.reply_document(document=InputFile(output_file), filename='output.txt')
                logger.info(f"Sent file: output.txt")

        except Exception as e:
            await update.message.reply_text(f"Klik /reset jika Error menggabungkan file: {str(e)}")
            logger.error(f"Error merging files: {str(e)}")
        finally:
            for file in selected_files:
                if os.path.exists(file['file_path']):
                    os.remove(file['file_path'])
            if os.path.exists(output_file_path):
                os.remove(output_file_path)



# Fungsi untuk menggabungkan file VCF
def merge_vcf_files(file_paths):
    vcf_content = []
    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as f:
            vcf_content.append(f.read().strip())
    return "\n".join(vcf_content)

# Fungsi untuk menangani perintah /gabungvcf
@check_user_permission
async def handle_merge_vcf_command(update: Update, context: CallbackContext):
    if 'files' not in context.user_data or len(context.user_data['files']) < 2:
        await update.message.reply_text("Silakan unggah setidaknya 2 file VCF untuk digabungkan.")
        return

    # Ambil file VCF dari user_data
    file_paths = [f['file_path'] for f in context.user_data['files'] if f['file_name'].endswith('.vcf')]

    if len(file_paths) < 2:
        await update.message.reply_text("Anda harus mengunggah setidaknya 2 file VCF untuk digabungkan.")
        return

    try:
        merged_vcf_data = merge_vcf_files(file_paths)
        merged_vcf_file_name = "File gabungan.vcf"
        merged_vcf_file_path = os.path.join(VCF_FOLDER, merged_vcf_file_name)

        # Simpan file VCF yang digabungkan
        with open(merged_vcf_file_path, 'w', encoding='utf-8') as merged_file:
            merged_file.write(merged_vcf_data)

        # Kirim file hasil gabungan ke pengguna
        with open(merged_vcf_file_path, 'rb') as merged_file:
            await update.message.reply_document(document=InputFile(merged_file), filename=merged_vcf_file_name)

        await update.message.reply_text("File VCF telah berhasil digabungkan dan dikirim.")
    
    except Exception as e:
        await update.message.reply_text(f"Klik /reset jika Terjadi kesalahan saat menggabungkan file: {str(e)}")



@check_user_permission
async def rename_vcf_file(update: Update, context: CallbackContext):
    if not context.args:
        await update.message.reply_text("Harap berikan nama file baru. Contoh: /rename nama_file_baru.vcf")
        return

    new_file_name = ' '.join(context.args)
    if not new_file_name.endswith('.vcf'):
        new_file_name += '.vcf'

    if 'files' not in context.user_data or not context.user_data['files']:
        await update.message.reply_text("Tidak ada file VCF yang diunggah. Silakan unggah file VCF terlebih dahulu.")
        return

    # Ambil file VCF terakhir yang diunggah
    selected_file = context.user_data['files'][-1]
    original_file_path = selected_file['file_path']
    
    try:
        # Ubah nama file
        new_file_path = os.path.join(VCF_FOLDER, new_file_name)
        os.rename(original_file_path, new_file_path)

        # Kirim file dengan nama baru
        with open(new_file_path, 'rb') as vcf_file:
            await update.message.reply_document(document=InputFile(vcf_file), filename=new_file_name)

        await update.message.reply_text(f"File VCF telah diubah namanya menjadi: {new_file_name}")

    except Exception as e:
        await update.message.reply_text(f"Terjadi kesalahan saat mengubah nama file: {str(e)}")
        logger.error(f"Error renaming file {original_file_path} to {new_file_path}: {str(e)}")
    finally:
        # Jika file baru berhasil dibuat, hapus file lama
        if os.path.exists(original_file_path):
            os.remove(original_file_path)


@check_user_permission
async def split_txt_file(update: Update, context: CallbackContext):
    if not context.args:
        await update.message.reply_text("Harap berikan ukuran pecahan. Contoh: /pecahtxt 500")
        return

    try:
        split_size = int(context.args[0])
        
        if 'files' not in context.user_data or not context.user_data['files']:
            await update.message.reply_text("Tidak ada file TXT yang diunggah. Silakan unggah file TXT terlebih dahulu.")
            return

        # Ambil file terakhir yang diunggah
        selected_file = context.user_data['files'][-1]
        file_path = selected_file['file_path']
        file_name = selected_file['file_name']

        if not file_name.endswith('.txt'):
            await update.message.reply_text("File yang diunggah bukan file TXT. Harap unggah file TXT.")
            return

        # Membaca file TXT dan memecahnya
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # Memecah file menjadi bagian-bagian
        for i in range(0, len(lines), split_size):
            chunk = lines[i:i + split_size]
            chunk_file_name = f"{os.path.splitext(file_name)[0]}-{i // split_size + 1}.txt"
            chunk_file_path = os.path.join(UPLOAD_FOLDER, chunk_file_name)

            with open(chunk_file_path, 'w', encoding='utf-8') as chunk_file:
                chunk_file.writelines(chunk)

            # Mengirimkan file pecahan ke pengguna
            with open(chunk_file_path, 'rb') as chunk_file:
                await update.message.reply_document(document=InputFile(chunk_file), filename=chunk_file_name)

        await update.message.reply_text(f"File TXT telah dipecah menjadi {len(lines) // split_size + 1} file.")

    except ValueError:
        await update.message.reply_text("Ukuran pecahan harus berupa angka. Contoh: /pecahtxt 500")
    except Exception as e:
        await update.message.reply_text(f"Terjadi kesalahan: {str(e)}")


@check_user_permission
async def xlsx_to_txt(update: Update, context: CallbackContext):
    if 'files' not in context.user_data or not context.user_data['files']:
        await update.message.reply_text("Tidak ada file XLSX yang diunggah. Silakan unggah file XLSX terlebih dahulu.")
        return

    # Ambil file terakhir yang diunggah
    selected_file = context.user_data['files'][-1]
    file_path = selected_file['file_path']
    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension not in ['.xls', '.xlsx']:
        await update.message.reply_text("Format file tidak valid. Harap unggah file XLSX.")
        return

    try:
        # Membaca file XLSX
        dataframe = pd.read_excel(file_path)

        # Mencari kolom yang berisi nomor telepon
        phone_numbers = []
        for column in dataframe.columns:
            # Menggunakan regex untuk mendeteksi nomor telepon
            potential_numbers = dataframe[column].dropna().astype(str).tolist()
            for number in potential_numbers:
                if re.match(r'^\+?\d{7,15}$', number):  # Pola nomor telepon
                    phone_numbers.append(number)

        if not phone_numbers:
            await update.message.reply_text("Tidak ada nomor telepon yang ditemukan dalam file.")
            return

        # Simpan ke file TXT
        txt_file_name = f"{os.path.splitext(os.path.basename(file_path))[0]}.txt"
        txt_file_path = os.path.join(UPLOAD_FOLDER, txt_file_name)

        with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
            for number in phone_numbers:
                txt_file.write(str(number) + '\n')

        # Kirim file TXT ke pengguna
        with open(txt_file_path, 'rb') as txt_file:
            await update.message.reply_document(document=InputFile(txt_file), filename=txt_file_name)

    except Exception as e:
        await update.message.reply_text(f"Error mengkonversi file XLSX ke TXT: {str(e)}")
    finally:
        # Menghapus file setelah dikirim
        if os.path.exists(file_path):
            os.remove(file_path)
        if os.path.exists(txt_file_path):
            os.remove(txt_file_path)
               

# Menambahkan handler untuk perintah /admin dan proses langkah-langkah
def main():
    application = Application.builder().token('7943963188:AAFuC4RO_iuqzr5-04MjlLQWi2JZLWKi8X8').build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("reset", reset_settings))
    application.add_handler(CommandHandler("pecahvcf", handle_split_vcf_command))  # Handler untuk perintah /pecahvcf
    application.add_handler(CommandHandler("admin", admin_command))  # Handler untuk perintah /admin
    application.add_handler(CommandHandler("vcftotxt", vcf_to_txt))
    application.add_handler(CommandHandler("merge", merge_txt_files))
    application.add_handler(CommandHandler("gabungvcf", handle_merge_vcf_command))
    application.add_handler(CommandHandler("rename", rename_vcf_file))
    application.add_handler(CommandHandler("pecahtxt", split_txt_file))
    application.add_handler(CommandHandler("xlsxtotxt", xlsx_to_txt))
    application.add_handler(CommandHandler("adduser", add_user))
    application.add_handler(CommandHandler("removeuser", remove_user))
    application.add_handler(CommandHandler("listusers", list_users))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_file))
    application.add_handler(MessageHandler(filters.TEXT & filters.REPLY, process_file_command))
    application.add_handler(MessageHandler(filters.TEXT, handle_admin_steps))  # Handler untuk proses langkah-langkah /admin
    

    application.run_polling()

if __name__ == "__main__":
    main()
