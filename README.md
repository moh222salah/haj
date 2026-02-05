# Hajj and Umrah data analysis platform🕋 


[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

منصة متقدمة لتحليل بيانات الحجاج والمعتمرين في السوق السعودي، مع التركيز على الخصوصية والأداء العالي.

An analytics platform for Hajj and Umrah pilgrim data in the Saudi market, focusing on privacy and high performance.

## 🎯 المميزات الرئيسية | Key Features

### 🔒 **Privacy & Security**
- تشفير البيانات الحساسة باستخدام SHA-256
- الامتثال الكامل لمعايير حماية البيانات
- Privacy-compliant decorators for sensitive data handling

### ⚡ **High Performance**
- معالجة ملايين السجلات بكفاءة عالية
- تحليل متوازي باستخدام Multithreading
- استهلاك ذاكرة محسّن مع Generators

### 📊 **Advanced Analytics**
- تحليل التوزيع الجغرافي والعمري
- كشف فترات الذروة والازدحام
- تقارير شاملة قابلة للتخصيص

## 🔧 التقنيات المستخدمة | Technologies Used

### **1. Advanced Decorators**
```python
@privacy_compliance       # حماية البيانات الشخصية
@performance_monitor      # مراقبة الأداء
@retry_on_failure        # إعادة المحاولة التلقائية
@cache_results           # التخزين المؤقت الذكي
```

### **2. Generators for Memory Efficiency**
```python
def generate_synthetic_pilgrims(count: int) -> Generator:
    """معالجة ملايين السجلات دون استهلاك الذاكرة"""
    for i in range(count):
        yield PilgrimRecord(...)
```

### **3. Multithreading for Parallel Processing**
```python
def parallel_comprehensive_analysis(self, records):
    """تحليل متوازي لعدة مجموعات بيانات في نفس الوقت"""
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {...}
```

## 📦 التثبيت | Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/hajj-umrah-analytics.git
cd hajj-umrah-analytics

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 🚀 الاستخدام السريع | Quick Start

```bash
# تشغيل التحليل الكامل
python hajj_umrah_analytics.py

# تشغيل الاختبارات
python tests/test_analytics.py

# عرض الأمثلة
python examples/basic_usage.py
python examples/advanced_filtering.py
python examples/custom_analysis.py
```

## 📖 أمثلة الاستخدام | Usage Examples

### مثال 1: التحليل الأساسي
```python
from hajj_umrah_analytics import HajjUmrahAnalyticsPlatform

# إنشاء المنصة
platform = HajjUmrahAnalyticsPlatform()

# تحميل البيانات
platform.load_data(count=50000)

# الحصول على الإحصائيات
summary = platform.get_summary_statistics()
print(f"Total pilgrims: {summary['total_pilgrims']:,}")
```

### مثال 2: التحليل المتدفق
```python
# تحليل البيانات على دفعات
for chunk_analysis in platform.stream_analysis(chunk_size=10000):
    print(f"Chunk {chunk_analysis['chunk_id']}: Processed")
```

### مثال 3: التحليل المتوازي
```python
# تشغيل تحليلات متعددة بالتوازي
report = platform.run_comprehensive_analysis()

# عرض النتائج
print(report['top_nationalities'])
print(report['detailed_analysis'])
```

## 📊 هيكل المشروع | Project Structure

```
hajj-umrah-analytics/
├── hajj_umrah_analytics.py    # الملف الرئيسي
├── README.md                   # التوثيق
├── requirements.txt            # المكتبات المطلوبة
├── setup.py                    # إعدادات التثبيت
├── tests/                      # الاختبارات
│   ├── __init__.py
│   ├── test_analytics.py
│   ├── test_decorators.py
│   └── test_generators.py
├── examples/                   # أمثلة الاستخدام
│   ├── basic_usage.py
│   ├── advanced_filtering.py
│   └── custom_analysis.py
├── docs/                       # التوثيق الكامل
│   ├── architecture.md
│   ├── api_reference.md
│   └── deployment.md
└── data/                       # بيانات تجريبية
    └── sample_data.json
```

## 🎓 المفاهيم المتقدمة الموضحة | Advanced Concepts Demonstrated

### **Decorators**
1. **Privacy Compliance Decorator**: حماية البيانات الحساسة تلقائياً
2. **Performance Monitor Decorator**: قياس وقت التنفيذ
3. **Retry Decorator**: إعادة المحاولة عند الفشل
4. **Cache Decorator**: تخزين مؤقت ذكي للنتائج

### **Generators**
1. **Data Generation**: توليد ملايين السجلات بكفاءة
2. **Streaming Analysis**: تحليل البيانات الزمنية بشكل متدفق
3. **Lazy Evaluation**: تقليل استهلاك الذاكرة
4. **Pipeline Processing**: معالجة البيانات على مراحل

### **Multithreading**
1. **Parallel Analysis**: تحليل عدة مجموعات بيانات بالتوازي
2. **Thread Pool Executor**: إدارة فعالة للخيوط
3. **Future Objects**: التعامل مع النتائج اللامتزامنة
4. **Thread Safety**: معالجة آمنة للبيانات المشتركة

## 🔬 الاختبارات | Testing

```bash
# تشغيل جميع الاختبارات
python -m pytest tests/ -v

# تشغيل اختبار محدد
python -m pytest tests/test_decorators.py -v

# قياس التغطية
python -m pytest --cov=hajj_umrah_analytics tests/
```

## 📈 الأداء | Performance

- **معالجة**: 50,000 سجل في أقل من 5 ثوانٍ
- **استهلاك الذاكرة**: أقل من 200 MB لمليون سجل
- **التوازي**: تسريع يصل إلى 3x مع 4 خيوط

## 🎯 حالات الاستخدام | Use Cases

### 1. شركات السياحة الدينية
- تحليل أنماط الحجاج
- تحسين الخدمات المقدمة
- التنبؤ بالطلب

### 2. الجهات الحكومية
- تخطيط البنية التحتية
- إدارة الحشود
- الأمن والسلامة

### 3. مقدمو الخدمات
- تحسين عمليات النقل
- إدارة الفنادق والسكن
- الخدمات الصحية

## 🤝 المساهمة | Contributing

نرحب بمساهماتكم! يرجى اتباع الخطوات التالية:

1. Fork المشروع
2. إنشاء فرع للميزة الجديدة (`git checkout -b feature/AmazingFeature`)
3. Commit التغييرات (`git commit -m 'Add some AmazingFeature'`)
4. Push للفرع (`git push origin feature/AmazingFeature`)
5. فتح Pull Request

## 📝 الترخيص | License

هذا المشروع مرخص تحت رخصة MIT - انظر ملف [LICENSE](LICENSE) للتفاصيل.

## 👤 المؤلف | Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your Profile](https://linkedin.com/in/yourprofile)
- Email: your.email@example.com

## 🙏 شكر وتقدير | Acknowledgments

- وزارة الحج والعمرة السعودية
- Python Community
- Open Source Contributors

## 📞 الدعم | Support

للأسئلة والدعم:
- فتح Issue على GitHub
- التواصل عبر البريد الإلكتروني
- مراجعة التوثيق الكامل في مجلد `docs/`

---

<div align="center">

**صُنع بـ ❤️ للسوق السعودي**

Made with ❤️ for the Saudi Market

[التوثيق](docs/) • [الأمثلة](examples/) • [الاختبارات](tests/)

</div>
