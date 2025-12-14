import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Animal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='동물명')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='생년월일')),
                ('gender', models.CharField(choices=[('M', '수컷'), ('F', '암컷')], max_length=1, verbose_name='성별')),
                ('is_neutered', models.BooleanField(default=False, verbose_name='중성화 여부')),
            ],
        ),
        migrations.CreateModel(
            name='Breed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='품종명')),
            ],
        ),
        migrations.CreateModel(
            name='MedicalTool',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='기구명')),
                ('code', models.CharField(blank=True, max_length=50, verbose_name='관리코드/일련번호')),
                ('stock', models.IntegerField(default=1, verbose_name='보유 수량')),
                ('manufacturer', models.CharField(blank=True, max_length=100, verbose_name='제조사')),
            ],
        ),
        migrations.CreateModel(
            name='Medicine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='약품명')),
                ('manufacturer', models.CharField(blank=True, max_length=100, verbose_name='제조사')),
                ('stock', models.IntegerField(default=0, verbose_name='재고 수량')),
                ('unit', models.CharField(max_length=10, verbose_name='단위')),
                ('expiry_date', models.DateField(blank=True, null=True, verbose_name='유통기한')),
                ('price', models.IntegerField(default=0, verbose_name='단가')),
            ],
        ),
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='보호자명')),
                ('phone', models.CharField(max_length=20, unique=True, verbose_name='전화번호')),
                ('address', models.TextField(verbose_name='주소')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='이메일')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='TreatmentInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='치료/검사명')),
                ('price', models.IntegerField(verbose_name='기준 비용')),
            ],
        ),
        migrations.CreateModel(
            name='Vaccine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='백신명')),
                ('manufacturer', models.CharField(blank=True, max_length=100, verbose_name='제약회사')),
                ('stock', models.IntegerField(default=0, verbose_name='재고 수량')),
                ('expiry_date', models.DateField(blank=True, null=True, verbose_name='유통기한')),
                ('price', models.IntegerField(verbose_name='접종 비용')),
            ],
        ),
        migrations.CreateModel(
            name='Vet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='수의사명')),
                ('contact', models.CharField(max_length=20, verbose_name='연락처')),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='예약 날짜')),
                ('time', models.TimeField(verbose_name='예약 시간')),
                ('status', models.CharField(choices=[('reserved', '예약중'), ('waiting', '진료대기'), ('in_progress', '진료중'), ('completed', '진료완료'), ('canceled', '취소')], default='reserved', max_length=20, verbose_name='상태')),
                ('reason', models.TextField(verbose_name='내원 사유')),
                ('animal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital.animal', verbose_name='환자')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital.owner', verbose_name='보호자')),
                ('vet', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hospital.vet', verbose_name='담당 수의사')),
            ],
        ),
        migrations.AddField(
            model_name='animal',
            name='breed',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hospital.breed', verbose_name='품종'),
        ),
        migrations.CreateModel(
            name='MedicalRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='진료일시')),
                ('weight', models.FloatField(verbose_name='체중(kg)')),
                ('temperature', models.FloatField(verbose_name='체온')),
                ('symptom', models.TextField(verbose_name='증상 상세')),
                ('diagnosis', models.CharField(max_length=100, verbose_name='진단명')),
                ('test_result', models.TextField(blank=True, help_text='예: 골절, 신장 수치 등', verbose_name='검사 결과')),
                ('appointment', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='medical_record', to='hospital.appointment')),
                ('vet', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='hospital.vet', verbose_name='담당 수의사')),
            ],
        ),
        migrations.AddField(
            model_name='animal',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='animals', to='hospital.owner', verbose_name='보호자'),
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_amount', models.IntegerField(verbose_name='청구 금액')),
                ('paid_amount', models.IntegerField(default=0, verbose_name='실 수납 금액')),
                ('payment_method', models.CharField(choices=[('card', '카드'), ('cash', '현금')], default='card', max_length=10, verbose_name='결제 수단')),
                ('is_paid', models.BooleanField(default=False, verbose_name='수납 완료 여부')),
                ('paid_at', models.DateTimeField(blank=True, null=True, verbose_name='수납 일시')),
                ('record', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='payment', to='hospital.medicalrecord')),
            ],
        ),
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=1, verbose_name='처방 수량')),
                ('description', models.TextField(blank=True, verbose_name='복용법/기간')),
                ('medicine', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='hospital.medicine', verbose_name='처방 약품')),
                ('record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prescriptions', to='hospital.medicalrecord')),
            ],
        ),
        migrations.CreateModel(
            name='ToolUsage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=1, verbose_name='사용 횟수/수량')),
                ('description', models.TextField(blank=True, verbose_name='비고')),
                ('record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tool_usages', to='hospital.medicalrecord')),
                ('tool', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='hospital.medicaltool', verbose_name='사용 기구')),
            ],
        ),
        migrations.CreateModel(
            name='MedicalDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, verbose_name='치료 메모')),
                ('record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='treatments', to='hospital.medicalrecord')),
                ('treatment', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='hospital.treatmentinfo', verbose_name='치료항목')),
            ],
        ),
        migrations.CreateModel(
            name='VaccinationRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, verbose_name='접종 메모')),
                ('next_due_date', models.DateField(blank=True, null=True, verbose_name='다음 접종 예정일')),
                ('record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vaccinations', to='hospital.medicalrecord')),
                ('vaccine', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='hospital.vaccine', verbose_name='백신')),
            ],
        ),
    ]
