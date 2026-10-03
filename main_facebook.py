# 🚗 البرنامج الرئيسي - مع Facebook

import asyncio
import json
from datetime import datetime
from parser import CarParser
from facebook_scraper import FacebookScraper

async def main():
    print("🚗 نظام مراقبة إعلانات السيارات - Facebook Edition")
    print("="*60)
    
    # استخراج من Facebook
    print("\n📘 استخراج من Facebook...")
    scraper = FacebookScraper()
    posts = await scraper.scrape_all_groups()
    
    if not posts:
        print("⚠️ لم يتم استخراج أي منشورات من Facebook")
        print("💡 تجربة البيانات الاختبارية...")
        posts = [
            'كامري 2020 للبيع بـ 75 ألف ريال في محايل',
            'BMW X5 بيع 120 ألف في الرياض',
        ]
    
    # معالجة البيانات
    parser = CarParser()
    deals = []
    
    print("\n" + "="*60)
    print("📊 جاري معالجة الإعلانات...")
    print("="*60 + "\n")
    
    for post in posts:
        deal = parser.parse_deal(post)
        if deal:
            deals.append(deal)
            print(f"✅ إعلان جديد: {deal['text'][:50]}...")
    
    # الإحصائيات
    print("\n" + "="*60)
    print("📊 الإحصائيات")
    print("="*60)
    print(f"📦 إجمالي الإعلانات: {len(deals)}")
    
    prices = [d['price'] for d in deals if d['price']]
    if prices:
        avg = sum(prices) / len(prices)
        print(f"💰 متوسط السعر: {avg:,.0f} ريال")
        print(f"💰 أقل سعر: {min(prices):,} ريال")
        print(f"💰 أعلى سعر: {max(prices):,} ريال")
    
    cities = set(d['location'] for d in deals if d['location'])
    print(f"🏙️ عدد المدن: {len(cities)}")
    if cities:
        print(f"   المدن: {', '.join(cities)}")
    
    # حفظ البيانات
    with open('deals_facebook.json', 'w', encoding='utf-8') as f:
        data = {
            'date': datetime.now().isoformat(),
            'source': 'Facebook',
            'total': len(deals),
            'deals': deals
        }
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("\n✅ تم الحفظ في deals_facebook.json")
    print("="*60)

if __name__ == '__main__':
    asyncio.run(main())
