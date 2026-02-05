"""
Unit tests for Hajj & Umrah Analytics Platform
"""

import unittest
import sys
import os
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from hajj_umrah_analytics import (
    PilgrimRecord,
    PilgrimType,
    Nationality,
    DataAnalyzer,
    HajjUmrahAnalyticsPlatform,
    generate_synthetic_pilgrims,
    privacy_compliance,
    performance_monitor,
    cache_results,
)


class TestDecorators(unittest.TestCase):
    """اختبارات الـ Decorators"""
    
    def test_privacy_compliance_decorator(self):
        """اختبار decorator حماية الخصوصية"""
        
        @privacy_compliance
        def process_data(data):
            return data
        
        # بيانات حساسة
        sensitive_data = {
            'national_id': '1234567890',
            'passport_number': 'P12345678',
            'phone': '+966501234567',
            'name': 'Test User'
        }
        
        result = process_data(sensitive_data)
        
        # التأكد من تشفير البيانات الحساسة
        self.assertNotEqual(result['national_id'], '1234567890')
        self.assertNotEqual(result['passport_number'], 'P12345678')
        self.assertNotEqual(result['phone'], '+966501234567')
        # الاسم لا يُشفّر
        self.assertEqual(result['name'], 'Test User')
    
    def test_performance_monitor_decorator(self):
        """اختبار decorator مراقبة الأداء"""
        
        @performance_monitor
        def slow_function():
            import time
            time.sleep(0.1)
            return "done"
        
        result = slow_function()
        self.assertEqual(result, "done")
    
    def test_cache_decorator(self):
        """اختبار decorator التخزين المؤقت"""
        call_count = [0]
        
        @cache_results(ttl_seconds=5)
        def expensive_function(x):
            call_count[0] += 1
            return x * 2
        
        # أول استدعاء
        result1 = expensive_function(5)
        self.assertEqual(result1, 10)
        self.assertEqual(call_count[0], 1)
        
        # استدعاء ثاني - يجب أن يستخدم الـ cache
        result2 = expensive_function(5)
        self.assertEqual(result2, 10)
        self.assertEqual(call_count[0], 1)  # لم يزد


class TestGenerators(unittest.TestCase):
    """اختبارات الـ Generators"""
    
    def test_generate_synthetic_pilgrims(self):
        """اختبار توليد البيانات التجريبية"""
        count = 1000
        generator = generate_synthetic_pilgrims(count)
        
        # التأكد من أنه generator
        self.assertTrue(hasattr(generator, '__iter__'))
        self.assertTrue(hasattr(generator, '__next__'))
        
        # تحويل إلى قائمة
        records = list(generator)
        
        self.assertEqual(len(records), count)
        
        # التأكد من صحة البيانات
        for record in records[:10]:
            self.assertIsInstance(record, PilgrimRecord)
            self.assertIsInstance(record.id, str)
            self.assertIsInstance(record.age, int)
            self.assertGreater(record.age, 0)
            self.assertLess(record.age, 120)
    
    def test_generator_memory_efficiency(self):
        """اختبار كفاءة الذاكرة للـ Generator"""
        import sys
        
        # إنشاء generator لعدد كبير
        gen = generate_synthetic_pilgrims(100000)
        gen_size = sys.getsizeof(gen)
        
        # حجم الـ generator يجب أن يكون صغير جداً
        self.assertLess(gen_size, 1000)  # أقل من 1KB


class TestDataAnalyzer(unittest.TestCase):
    """اختبارات محلل البيانات"""
    
    def setUp(self):
        """إعداد بيانات الاختبار"""
        self.analyzer = DataAnalyzer(max_workers=2)
        
        # إنشاء بيانات تجريبية
        self.test_records = list(generate_synthetic_pilgrims(100))
    
    def tearDown(self):
        """تنظيف الموارد"""
        self.analyzer.shutdown()
    
    def test_analyze_by_nationality(self):
        """اختبار التحليل حسب الجنسية"""
        result = self.analyzer.analyze_by_nationality(self.test_records)
        
        self.assertIsInstance(result, dict)
        self.assertGreater(len(result), 0)
        
        # التأكد من أن المجموع يساوي عدد السجلات
        total = sum(result.values())
        self.assertEqual(total, len(self.test_records))
    
    def test_analyze_age_groups(self):
        """اختبار التحليل العمري"""
        result = self.analyzer.analyze_age_groups(self.test_records)
        
        self.assertIsInstance(result, dict)
        self.assertIn('18-30', result)
        self.assertIn('31-45', result)
        self.assertIn('46-60', result)
        self.assertIn('60+', result)
        
        # المجموع يجب أن يساوي عدد السجلات
        total = sum(result.values())
        self.assertEqual(total, len(self.test_records))
    
    def test_parallel_analysis(self):
        """اختبار التحليل المتوازي"""
        result = self.analyzer.parallel_comprehensive_analysis(self.test_records)
        
        self.assertIsInstance(result, dict)
        self.assertIn('nationality', result)
        self.assertIn('age_groups', result)
        self.assertIn('peak_periods', result)
    
    def test_health_status_privacy(self):
        """اختبار حماية البيانات الصحية"""
        test_record = {
            'national_id': '1234567890',
            'health_status': 'جيد'
        }
        
        result = self.analyzer.analyze_health_status(test_record)
        
        # التأكد من عدم تسريب الرقم الوطني
        self.assertNotIn('1234567890', str(result))


class TestPlatform(unittest.TestCase):
    """اختبارات المنصة الرئيسية"""
    
    def setUp(self):
        """إعداد المنصة"""
        self.platform = HajjUmrahAnalyticsPlatform()
    
    def tearDown(self):
        """تنظيف"""
        self.platform.cleanup()
    
    def test_load_data(self):
        """اختبار تحميل البيانات"""
        count = 1000
        self.platform.load_data(count=count)
        
        self.assertEqual(len(self.platform.records), count)
    
    def test_summary_statistics(self):
        """اختبار الإحصائيات الملخصة"""
        self.platform.load_data(count=500)
        summary = self.platform.get_summary_statistics()
        
        self.assertIsInstance(summary, dict)
        self.assertIn('total_pilgrims', summary)
        self.assertEqual(summary['total_pilgrims'], 500)
        self.assertIn('average_age', summary)
        self.assertGreater(summary['average_age'], 0)
    
    def test_comprehensive_analysis(self):
        """اختبار التحليل الشامل"""
        self.platform.load_data(count=1000)
        report = self.platform.run_comprehensive_analysis()
        
        self.assertIsInstance(report, dict)
        self.assertIn('summary', report)
        self.assertIn('detailed_analysis', report)
        self.assertIn('top_nationalities', report)
        self.assertIn('generated_at', report)
    
    def test_stream_analysis(self):
        """اختبار التحليل المتدفق"""
        self.platform.load_data(count=5000)
        
        chunks_processed = 0
        for chunk in self.platform.stream_analysis(chunk_size=1000):
            chunks_processed += 1
            self.assertIn('chunk_id', chunk)
            self.assertIn('statistics', chunk)
        
        self.assertEqual(chunks_processed, 5)


class TestDataModels(unittest.TestCase):
    """اختبارات نماذج البيانات"""
    
    def test_pilgrim_record_creation(self):
        """اختبار إنشاء سجل حاج"""
        record = PilgrimRecord(
            id="PIL00000001",
            national_id="1234567890",
            passport_number="P12345678",
            name="Test Pilgrim",
            age=35,
            gender="ذكر",
            nationality=Nationality.SAUDI,
            phone="+966501234567",
            pilgrim_type=PilgrimType.HAJJ,
            arrival_date=datetime.now(),
            departure_date=datetime.now() + timedelta(days=10),
            accommodation_id="ACC1234",
            transport_id="TRN123",
            health_status="جيد"
        )
        
        self.assertEqual(record.id, "PIL00000001")
        self.assertEqual(record.age, 35)
        self.assertEqual(record.nationality, Nationality.SAUDI)
        self.assertEqual(record.pilgrim_type, PilgrimType.HAJJ)
    
    def test_pilgrim_to_dict(self):
        """اختبار تحويل السجل إلى قاموس"""
        record = PilgrimRecord(
            id="PIL00000001",
            national_id="1234567890",
            passport_number="P12345678",
            name="Test",
            age=30,
            gender="ذكر",
            nationality=Nationality.EGYPTIAN,
            phone="+20123456789",
            pilgrim_type=PilgrimType.UMRAH,
            arrival_date=datetime.now(),
            departure_date=datetime.now() + timedelta(days=5),
            accommodation_id="ACC1234",
            transport_id="TRN123",
            health_status="ممتاز"
        )
        
        record_dict = record.to_dict()
        
        self.assertIsInstance(record_dict, dict)
        self.assertEqual(record_dict['id'], "PIL00000001")
        self.assertEqual(record_dict['nationality'], "مصري")
        self.assertEqual(record_dict['pilgrim_type'], "عمرة")


def run_tests():
    """تشغيل جميع الاختبارات"""
    # إنشاء test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # إضافة جميع الاختبارات
    suite.addTests(loader.loadTestsFromTestCase(TestDecorators))
    suite.addTests(loader.loadTestsFromTestCase(TestGenerators))
    suite.addTests(loader.loadTestsFromTestCase(TestDataAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestPlatform))
    suite.addTests(loader.loadTestsFromTestCase(TestDataModels))
    
    # تشغيل الاختبارات
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # عرض النتائج
    print("\n" + "="*60)
    print("📊 Test Results Summary")
    print("="*60)
    print(f"✅ Tests run: {result.testsRun}")
    print(f"✅ Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Failures: {len(result.failures)}")
    print(f"⚠️  Errors: {len(result.errors)}")
    print("="*60)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
