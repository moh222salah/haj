"""
Hajj & Umrah Analytics Platform
================================
منصة تحليل بيانات الحج والعمرة للسوق السعودي

Features:
- Privacy-compliant decorators
- Efficient data processing with generators
- Parallel analysis with multithreading
- Real-time analytics and reporting

Author: Your Name
License: MIT
"""

import functools
import time
import hashlib
import logging
from datetime import datetime, timedelta
from typing import Generator, Callable, Any, Dict, List
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from enum import Enum
import random
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ==================== DECORATORS ====================

def privacy_compliance(func: Callable) -> Callable:
    """
    Decorator: تطبيق سياسات الخصوصية على البيانات الحساسة
    يقوم بتشفير المعلومات الشخصية قبل المعالجة
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"🔒 Privacy check: {func.__name__}")
        
        # تشفير البيانات الحساسة
        if args and isinstance(args[0], dict):
            data = args[0].copy()
            sensitive_fields = ['national_id', 'passport_number', 'phone']
            
            for field in sensitive_fields:
                if field in data:
                    original = data[field]
                    data[field] = hashlib.sha256(str(original).encode()).hexdigest()[:16]
            
            return func(data, *args[1:], **kwargs)
        
        return func(*args, **kwargs)
    
    return wrapper


def performance_monitor(func: Callable) -> Callable:
    """
    Decorator: مراقبة أداء الدوال وتسجيل الوقت المستغرق
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        elapsed_time = time.time() - start_time
        
        logger.info(f"⏱️  {func.__name__} took {elapsed_time:.4f} seconds")
        return result
    
    return wrapper


def retry_on_failure(max_retries: int = 3, delay: float = 1.0):
    """
    Decorator: إعادة المحاولة عند الفشل (للعمليات الحرجة)
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        logger.error(f"❌ Failed after {max_retries} attempts: {e}")
                        raise
                    logger.warning(f"⚠️  Attempt {attempt + 1} failed, retrying...")
                    time.sleep(delay)
            return None
        return wrapper
    return decorator


def cache_results(ttl_seconds: int = 300):
    """
    Decorator: تخزين مؤقت للنتائج لتحسين الأداء
    """
    cache = {}
    
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = str(args) + str(kwargs)
            current_time = time.time()
            
            if key in cache:
                result, timestamp = cache[key]
                if current_time - timestamp < ttl_seconds:
                    logger.info(f"📦 Cache hit for {func.__name__}")
                    return result
            
            result = func(*args, **kwargs)
            cache[key] = (result, current_time)
            return result
        
        return wrapper
    return decorator


# ==================== ENUMS & DATA CLASSES ====================

class PilgrimType(Enum):
    """نوع الزائر"""
    HAJJ = "حج"
    UMRAH = "عمرة"


class Nationality(Enum):
    """الجنسيات الشائعة"""
    SAUDI = "سعودي"
    EGYPTIAN = "مصري"
    PAKISTANI = "باكستاني"
    INDONESIAN = "إندونيسي"
    INDIAN = "هندي"
    BANGLADESHI = "بنجلاديشي"
    TURKISH = "تركي"
    OTHER = "أخرى"


@dataclass
class PilgrimRecord:
    """سجل حاج أو معتمر"""
    id: str
    national_id: str
    passport_number: str
    name: str
    age: int
    gender: str
    nationality: Nationality
    phone: str
    pilgrim_type: PilgrimType
    arrival_date: datetime
    departure_date: datetime
    accommodation_id: str
    transport_id: str
    health_status: str
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'national_id': self.national_id,
            'passport_number': self.passport_number,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'nationality': self.nationality.value,
            'phone': self.phone,
            'pilgrim_type': self.pilgrim_type.value,
            'arrival_date': self.arrival_date.isoformat(),
            'departure_date': self.departure_date.isoformat(),
            'accommodation_id': self.accommodation_id,
            'transport_id': self.transport_id,
            'health_status': self.health_status
        }


# ==================== GENERATORS ====================

def generate_synthetic_pilgrims(count: int) -> Generator[PilgrimRecord, None, None]:
    """
    Generator: توليد بيانات تجريبية للحجاج والمعتمرين
    يستخدم Generator لتوفير الذاكرة عند معالجة ملايين السجلات
    """
    logger.info(f"🔄 Generating {count} synthetic pilgrim records...")
    
    names = ["محمد", "أحمد", "فاطمة", "عائشة", "عبدالله", "سارة", "خالد", "مريم"]
    
    for i in range(count):
        arrival = datetime.now() - timedelta(days=random.randint(1, 30))
        departure = arrival + timedelta(days=random.randint(5, 15))
        
        record = PilgrimRecord(
            id=f"PIL{i:08d}",
            national_id=f"{random.randint(1000000000, 9999999999)}",
            passport_number=f"P{random.randint(10000000, 99999999)}",
            name=random.choice(names),
            age=random.randint(18, 80),
            gender=random.choice(["ذكر", "أنثى"]),
            nationality=random.choice(list(Nationality)),
            phone=f"+966{random.randint(500000000, 599999999)}",
            pilgrim_type=random.choice(list(PilgrimType)),
            arrival_date=arrival,
            departure_date=departure,
            accommodation_id=f"ACC{random.randint(1000, 9999)}",
            transport_id=f"TRN{random.randint(100, 999)}",
            health_status=random.choice(["جيد", "ممتاز", "يحتاج متابعة"])
        )
        
        yield record
        
        # عرض التقدم كل 10000 سجل
        if (i + 1) % 10000 == 0:
            logger.info(f"  Generated {i + 1:,} records...")


def stream_time_series_analysis(
    records: List[PilgrimRecord],
    chunk_size: int = 1000
) -> Generator[Dict[str, Any], None, None]:
    """
    Generator: تحليل البيانات الزمنية بشكل متدفق
    معالجة البيانات على دفعات لتجنب استهلاك الذاكرة
    """
    logger.info("📊 Starting time-series analysis...")
    
    for i in range(0, len(records), chunk_size):
        chunk = records[i:i + chunk_size]
        
        # تحليل الدفعة
        analysis = {
            'chunk_id': i // chunk_size + 1,
            'chunk_size': len(chunk),
            'date_range': {
                'start': min(r.arrival_date for r in chunk).isoformat(),
                'end': max(r.departure_date for r in chunk).isoformat()
            },
            'statistics': {
                'total_pilgrims': len(chunk),
                'avg_age': sum(r.age for r in chunk) / len(chunk),
                'male_count': sum(1 for r in chunk if r.gender == "ذكر"),
                'female_count': sum(1 for r in chunk if r.gender == "أنثى"),
                'hajj_count': sum(1 for r in chunk if r.pilgrim_type == PilgrimType.HAJJ),
                'umrah_count': sum(1 for r in chunk if r.pilgrim_type == PilgrimType.UMRAH),
            }
        }
        
        yield analysis


def filter_by_criteria(
    records: Generator[PilgrimRecord, None, None],
    criteria: Dict[str, Any]
) -> Generator[PilgrimRecord, None, None]:
    """
    Generator: تصفية السجلات حسب معايير محددة
    """
    logger.info(f"🔍 Filtering records with criteria: {criteria}")
    
    for record in records:
        match = True
        
        if 'nationality' in criteria:
            match = match and record.nationality == criteria['nationality']
        
        if 'min_age' in criteria:
            match = match and record.age >= criteria['min_age']
        
        if 'max_age' in criteria:
            match = match and record.age <= criteria['max_age']
        
        if 'pilgrim_type' in criteria:
            match = match and record.pilgrim_type == criteria['pilgrim_type']
        
        if match:
            yield record


# ==================== MULTITHREADING ====================

class DataAnalyzer:
    """محلل البيانات مع دعم المعالجة المتوازية"""
    
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
    
    @performance_monitor
    def analyze_by_nationality(self, records: List[PilgrimRecord]) -> Dict[str, int]:
        """تحليل التوزيع حسب الجنسية"""
        logger.info("🌍 Analyzing nationality distribution...")
        
        nationality_count = {}
        for record in records:
            nat = record.nationality.value
            nationality_count[nat] = nationality_count.get(nat, 0) + 1
        
        return nationality_count
    
    @performance_monitor
    def analyze_age_groups(self, records: List[PilgrimRecord]) -> Dict[str, int]:
        """تحليل التوزيع العمري"""
        logger.info("👥 Analyzing age group distribution...")
        
        age_groups = {
            '18-30': 0,
            '31-45': 0,
            '46-60': 0,
            '60+': 0
        }
        
        for record in records:
            if record.age <= 30:
                age_groups['18-30'] += 1
            elif record.age <= 45:
                age_groups['31-45'] += 1
            elif record.age <= 60:
                age_groups['46-60'] += 1
            else:
                age_groups['60+'] += 1
        
        return age_groups
    
    @performance_monitor
    def analyze_peak_periods(self, records: List[PilgrimRecord]) -> Dict[str, int]:
        """تحليل فترات الذروة"""
        logger.info("📅 Analyzing peak periods...")
        
        daily_arrivals = {}
        for record in records:
            date_key = record.arrival_date.strftime('%Y-%m-%d')
            daily_arrivals[date_key] = daily_arrivals.get(date_key, 0) + 1
        
        return daily_arrivals
    
    @performance_monitor
    @privacy_compliance
    def analyze_health_status(self, record: Dict) -> Dict[str, Any]:
        """تحليل الحالة الصحية (مع حماية الخصوصية)"""
        return {
            'status': record.get('health_status', 'غير محدد'),
            'requires_attention': record.get('health_status') == 'يحتاج متابعة'
        }
    
    @performance_monitor
    def parallel_comprehensive_analysis(
        self,
        records: List[PilgrimRecord]
    ) -> Dict[str, Any]:
        """
        تحليل شامل متوازي باستخدام Multithreading
        يقوم بتشغيل عدة تحليلات في نفس الوقت
        """
        logger.info(f"🚀 Starting parallel analysis with {self.max_workers} workers...")
        
        futures = {
            'nationality': self.executor.submit(self.analyze_by_nationality, records),
            'age_groups': self.executor.submit(self.analyze_age_groups, records),
            'peak_periods': self.executor.submit(self.analyze_peak_periods, records)
        }
        
        results = {}
        for name, future in futures.items():
            try:
                results[name] = future.result()
                logger.info(f"  ✅ {name} analysis completed")
            except Exception as e:
                logger.error(f"  ❌ {name} analysis failed: {e}")
                results[name] = None
        
        return results
    
    def shutdown(self):
        """إيقاف executor"""
        self.executor.shutdown(wait=True)


# ==================== MAIN APPLICATION ====================

class HajjUmrahAnalyticsPlatform:
    """المنصة الرئيسية لتحليل بيانات الحج والعمرة"""
    
    def __init__(self):
        self.analyzer = DataAnalyzer(max_workers=4)
        self.records: List[PilgrimRecord] = []
    
    @retry_on_failure(max_retries=3, delay=1.0)
    @performance_monitor
    def load_data(self, count: int = 50000):
        """تحميل البيانات باستخدام Generator"""
        logger.info(f"📥 Loading {count:,} pilgrim records...")
        
        # استخدام Generator لتوليد البيانات
        generator = generate_synthetic_pilgrims(count)
        self.records = list(generator)
        
        logger.info(f"✅ Successfully loaded {len(self.records):,} records")
    
    @cache_results(ttl_seconds=300)
    @performance_monitor
    def get_summary_statistics(self) -> Dict[str, Any]:
        """الحصول على إحصائيات ملخصة"""
        logger.info("📈 Calculating summary statistics...")
        
        total = len(self.records)
        
        return {
            'total_pilgrims': total,
            'hajj_pilgrims': sum(1 for r in self.records if r.pilgrim_type == PilgrimType.HAJJ),
            'umrah_pilgrims': sum(1 for r in self.records if r.pilgrim_type == PilgrimType.UMRAH),
            'average_age': sum(r.age for r in self.records) / total if total > 0 else 0,
            'male_percentage': (sum(1 for r in self.records if r.gender == "ذكر") / total * 100) if total > 0 else 0,
            'female_percentage': (sum(1 for r in self.records if r.gender == "أنثى") / total * 100) if total > 0 else 0,
        }
    
    def stream_analysis(self, chunk_size: int = 5000):
        """تحليل متدفق للبيانات الزمنية"""
        logger.info("🌊 Starting streaming analysis...")
        
        for chunk_analysis in stream_time_series_analysis(self.records, chunk_size):
            logger.info(f"  Chunk {chunk_analysis['chunk_id']}: {chunk_analysis['statistics']['total_pilgrims']} records")
            yield chunk_analysis
    
    @performance_monitor
    def run_comprehensive_analysis(self) -> Dict[str, Any]:
        """تشغيل التحليل الشامل"""
        logger.info("🎯 Running comprehensive analysis...")
        
        # التحليل المتوازي
        parallel_results = self.analyzer.parallel_comprehensive_analysis(self.records)
        
        # الإحصائيات الملخصة
        summary = self.get_summary_statistics()
        
        # دمج النتائج
        report = {
            'generated_at': datetime.now().isoformat(),
            'summary': summary,
            'detailed_analysis': parallel_results,
            'top_nationalities': dict(
                sorted(
                    parallel_results.get('nationality', {}).items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:5]
            ) if parallel_results.get('nationality') else {}
        }
        
        return report
    
    def export_report(self, report: Dict[str, Any], filename: str = 'report.json'):
        """تصدير التقرير"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        logger.info(f"📄 Report exported to {filename}")
    
    def cleanup(self):
        """تنظيف الموارد"""
        self.analyzer.shutdown()


# ==================== DEMO ====================

def main():
    """
    التطبيق الرئيسي - عرض توضيحي
    """
    print("=" * 60)
    print("🕋 منصة تحليل بيانات الحج والعمرة")
    print("   Hajj & Umrah Analytics Platform")
    print("=" * 60)
    print()
    
    # إنشاء المنصة
    platform = HajjUmrahAnalyticsPlatform()
    
    try:
        # 1. تحميل البيانات (Generator)
        print("📊 Step 1: Loading data using Generators...")
        platform.load_data(count=50000)
        print()
        
        # 2. الإحصائيات الملخصة (Cached Decorator)
        print("📈 Step 2: Getting summary statistics (with caching)...")
        summary = platform.get_summary_statistics()
        print(f"   Total Pilgrims: {summary['total_pilgrims']:,}")
        print(f"   Hajj: {summary['hajj_pilgrims']:,} | Umrah: {summary['umrah_pilgrims']:,}")
        print(f"   Average Age: {summary['average_age']:.1f} years")
        print(f"   Gender: {summary['male_percentage']:.1f}% Male, {summary['female_percentage']:.1f}% Female")
        print()
        
        # 3. التحليل المتدفق (Generator)
        print("🌊 Step 3: Streaming analysis (first 3 chunks)...")
        for i, chunk in enumerate(platform.stream_analysis(chunk_size=10000)):
            if i >= 3:
                break
            print(f"   Chunk {chunk['chunk_id']}: {chunk['statistics']['total_pilgrims']} pilgrims analyzed")
        print()
        
        # 4. التحليل الشامل المتوازي (Multithreading)
        print("🚀 Step 4: Running comprehensive parallel analysis...")
        report = platform.run_comprehensive_analysis()
        print()
        
        # 5. عرض أهم النتائج
        print("🏆 Top 5 Nationalities:")
        for nat, count in report['top_nationalities'].items():
            percentage = (count / summary['total_pilgrims'] * 100)
            print(f"   {nat}: {count:,} ({percentage:.1f}%)")
        print()
        
        # 6. حفظ التقرير
        print("💾 Step 5: Exporting report...")
        platform.export_report(report, '/home/claude/hajj_analysis_report.json')
        print()
        
        print("=" * 60)
        print("✅ Analysis completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        logger.error(f"❌ Error during execution: {e}")
        raise
    
    finally:
        platform.cleanup()


if __name__ == "__main__":
    main()
