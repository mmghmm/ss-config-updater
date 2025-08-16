import requests
import os
import sys
import logging

# پیکربندی اولیه برای لاگ‌ها
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

HEADERS = """//profile-title: base64:8J+RvUFub255bW91cyhQcm9qZWN0QWluaXRhKQ==
//profile-update-interval: 24
//subscription-userinfo: upload=0; download=0; total=10737418240000000; expire=2546249531
//support-url: https://t.me/BXAMbot
//profile-web-page-url: https://github.com/4n0nymou3"""

def fetch_configs_from_url(url):
    """
    محتوای کانفیگ را از یک URL مشخص دریافت می‌کند و تمام کانفیگ‌های معتبر ss را استخراج می‌کند.

    Args:
        url (str): آدرس URL برای دریافت محتوا.

    Returns:
        list: لیستی از رشته‌های کانفیگ معتبر ss، یا یک لیست خالی در صورت خطا.
    """
    https_url = url.replace('ssconf://', 'https://')
    logger.info(f"در حال دریافت کانفیگ از: {https_url}")
    
    try:
        response = requests.get(https_url, timeout=10)
        response.raise_for_status()
        content = response.text.strip()
        
        # محتوا را به خطوط جداگانه تقسیم می‌کند.
        lines = content.splitlines()
        
        valid_configs = []
        for line in lines:
            line_stripped = line.strip()
            # بررسی می‌کند که آیا خط با "ss://" شروع می‌شود یا نه.
            if line_stripped.startswith('ss://'):
                valid_configs.append(line_stripped)
        
        if valid_configs:
            logger.info(f"با موفقیت {len(valid_configs)} کانفیگ از {https_url} دریافت شد.")
            return valid_configs
        else:
            logger.error(f"هیچ کانفیگ معتبری در {https_url} یافت نشد.")
            return []
            
    except requests.exceptions.RequestException as e:
        logger.error(f"خطا در دریافت {https_url}: {str(e)}")
        return []

def main():
    """
    تابع اصلی برای دریافت و ذخیره کانفیگ‌ها.
    """
    logger.info("فرآیند دریافت کانفیگ آغاز شد.")

    urls = [
        "ssconf://ainita.s3.eu-north-1.amazonaws.com/AinitaServer-1.csv",
        "ssconf://ainita.s3.eu-north-1.amazonaws.com/AinitaServer-2.csv",
        "ssconf://ainita.s3.eu-north-1.amazonaws.com/AinitaServer-3.csv",
        "ssconf://ainita.s3.eu-north-1.amazonaws.com/AinitaServer-4.csv"
    ]

    all_configs = []
    for url in urls:
        logger.info(f"در حال پردازش URL: {url}")
        configs_from_url = fetch_configs_from_url(url)
        # اضافه کردن لیست کانفیگ‌های دریافت شده به لیست اصلی.
        all_configs.extend(configs_from_url)
    
    if not all_configs:
        logger.error("هیچ کانفیگی با موفقیت دریافت نشد!")
        sys.exit(1)

    try:
        # نوشتن کانفیگ‌ها در فایل configs.txt.
        with open('configs.txt', 'w', encoding='utf-8') as f:
            f.write(HEADERS)
            f.write('\n\n')
            f.write('\n'.join(all_configs))
        logger.info(f"با موفقیت {len(all_configs)} کانفیگ به همراه هدرها در configs.txt نوشته شد.")
    except Exception as e:
        logger.error(f"خطا در نوشتن در فایل: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
