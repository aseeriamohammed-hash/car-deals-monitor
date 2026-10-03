# 📘 Facebook Scraper - استخراج البيانات من Facebook

import asyncio
import random
from playwright.async_api import async_playwright
from config import FACEBOOK_EMAIL, FACEBOOK_PASSWORD, FACEBOOK_GROUPS

class FacebookScraper:
    def __init__(self):
        self.posts = []
    
    async def login(self, page):
        """تسجيل الدخول إلى Facebook"""
        print("🔐 جاري تسجيل الدخول...")
        
        try:
            await page.goto('https://www.facebook.com/login', wait_until='networkidle')
            await asyncio.sleep(2)
            
            # ملأ بيانات تسجيل الدخول
            await page.fill('input[name="email"]', FACEBOOK_EMAIL)
            await asyncio.sleep(1)
            await page.fill('input[name="pass"]', FACEBOOK_PASSWORD)
            await asyncio.sleep(1)
            
            # اضغط زر تسجيل الدخول
            await page.click('button[name="login"]')
            await page.wait_for_load_state('networkidle')
            
            print("✅ تم تسجيل الدخول بنجاح!")
            return True
            
        except Exception as e:
            print(f"❌ خطأ في تسجيل الدخول: {e}")
            return False
    
    async def scrape_group(self, page, group_url, group_num):
        """استخراج منشورات من مجموعة واحدة"""
        try:
            print(f"\n📡 المجموعة {group_num}/15...")
            
            await page.goto(group_url, wait_until='networkidle')
            await asyncio.sleep(random.uniform(2, 4))
            
            # التمرير لتحميل منشورات أكثر
            for scroll in range(3):
                await page.evaluate("window.scrollBy(0, window.innerHeight)")
                await asyncio.sleep(random.uniform(2, 3))
                print(f"  ⬇️ تمرير {scroll + 1}/3...")
            
            # استخراج النصوص
            posts = await page.evaluate('''() => {
                const posts = [];
                document.querySelectorAll('[role="article"]').forEach(el => {
                    const text = el.innerText;
                    if (text && text.length > 20) {
                        posts.push(text.substring(0, 500));
                    }
                });
                return posts;
            }''')
            
            print(f"  ✓ تم استخراج {len(posts)} منشور")
            return posts
            
        except Exception as e:
            print(f"  ❌ خطأ: {e}")
            return []
    
    async def scrape_all_groups(self):
        """استخراج من جميع المجموعات"""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            
            try:
                # تسجيل الدخول
                if not await self.login(page):
                    return []
                
                # استخراج من المجموعات
                print("\n" + "="*60)
                print("📊 جاري استخراج من المجموعات...")
                print("="*60)
                
                all_posts = []
                for idx, group_url in enumerate(FACEBOOK_GROUPS, 1):
                    posts = await self.scrape_group(page, group_url, idx)
                    all_posts.extend(posts)
                    
                    # تأخير عشوائي بين المجموعات
                    if idx < len(FACEBOOK_GROUPS):
                        delay = random.uniform(3, 8)
                        print(f"  ⏰ انتظار {delay:.1f} ثانية...")
                        await asyncio.sleep(delay)
                
                print("\n✅ انتهى استخراج البيانات!")
                return all_posts
                
            except Exception as e:
                print(f"❌ خطأ: {e}")
                return []
            
            finally:
                await browser.close()

# اختبار الـ Scraper
async def test():
    scraper = FacebookScraper()
    posts = await scraper.scrape_all_groups()
    print(f"\n📦 إجمالي المنشورات: {len(posts)}")
    return posts

if __name__ == '__main__':
    asyncio.run(test())
