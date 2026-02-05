"""
مثال 1: الاستخدام الأساسي
Example 1: Basic Usage

يوضح هذا المثال كيفية:
- تحميل البيانات
- الحصول على الإحصائيات الأساسية
- عرض النتائج
"""

import sys
import os

# إضافة المسار الرئيسي
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from hajj_umrah_analytics import HajjUmrahAnalyticsPlatform


def main():
    print("=" * 70)
    print("🕋 مثال 1: الاستخدام الأساسي - Basic Usage Example")
    print("=" * 70)
    print()
    
    # 1. إنشاء المنصة
    print("📦 Step 1: Creating platform instance...")
    platform = HajjUmrahAnalyticsPlatform()
    print("   ✅ Platform created successfully!")
    print()
    
    # 2. تحميل البيانات
    print("📥 Step 2: Loading pilgrim data...")
    platform.load_data(count=10000)  # 10,000 سجل
    print(f"   ✅ Loaded {len(platform.records):,} records")
    print()
    
    # 3. الحصول على الإحصائيات الأساسية
    print("📊 Step 3: Calculating statistics...")
    summary = platform.get_summary_statistics()
    print()
    
    # 4. عرض النتائج
    print("📈 Results:")
    print("-" * 70)
    print(f"   إجمالي الزوار | Total Pilgrims:        {summary['total_pilgrims']:,}")
    print(f"   حجاج | Hajj Pilgrims:                    {summary['hajj_pilgrims']:,}")
    print(f"   معتمرون | Umrah Pilgrims:                {summary['umrah_pilgrims']:,}")
    print()
    print(f"   متوسط العمر | Average Age:              {summary['average_age']:.1f} سنة")
    print()
    print(f"   نسبة الذكور | Male Percentage:          {summary['male_percentage']:.1f}%")
    print(f"   نسبة الإناث | Female Percentage:        {summary['female_percentage']:.1f}%")
    print("-" * 70)
    print()
    
    # 5. عرض بعض السجلات كأمثلة
    print("📋 Sample Records (first 3):")
    print("-" * 70)
    for i, record in enumerate(platform.records[:3], 1):
        print(f"\n   Record {i}:")
        print(f"      ID: {record.id}")
        print(f"      Name: {record.name}")
        print(f"      Age: {record.age}")
        print(f"      Nationality: {record.nationality.value}")
        print(f"      Type: {record.pilgrim_type.value}")
        print(f"      Health: {record.health_status}")
    print("-" * 70)
    print()
    
    # 6. التنظيف
    print("🧹 Step 4: Cleanup...")
    platform.cleanup()
    print("   ✅ Cleanup completed!")
    print()
    
    print("=" * 70)
    print("✅ Example completed successfully!")
    print("=" * 70)


if __name__ == "__main__":
    main()
