import os
import pandas as pd
import vobject
from telegram import ReplyKeyboardRemove
from telegram import ReplyKeyboardMarkup
from telegram import Update, InputFile
from telegram.ext import Application, ConversationHandler, CommandHandler, MessageHandler, filters, CallbackContext
import logging
import re
from flask import Flask
from threading import Thread

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
def convert_to_vcf(data
