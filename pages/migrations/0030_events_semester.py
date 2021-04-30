# Generated by Django 3.1.8 on 2021-04-19 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0029_auto_20210419_1543'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='semester',
            field=models.CharField(blank=True, choices=[('ws2024', 'Wintersemester 2024/2025'), ('ss2024', 'Sommersemester 2024'), ('ws2023', 'Wintersemester 2023/2024'), ('ss2023', 'Sommersemester 2023'), ('ws2022', 'Wintersemester 2022/2023'), ('ss2022', 'Sommersemester 2022'), ('ws2021', 'Wintersemester 2021/2022'), ('ss2021', 'Sommersemester 2021'), ('ws2020', 'Wintersemester 2020/2021'), ('ss2020', 'Sommersemester 2020'), ('ws2019', 'Wintersemester 2019/2020'), ('ss2019', 'Sommersemester 2019'), ('ws2018', 'Wintersemester 2018/2019'), ('ss2018', 'Sommersemester 2018'), ('ws2017', 'Wintersemester 2017/2018'), ('ss2017', 'Sommersemester 2017'), ('ws2016', 'Wintersemester 2016/2017'), ('ss2016', 'Sommersemester 2016'), ('ws2015', 'Wintersemester 2015/2016'), ('ss2015', 'Sommersemester 2015'), ('ws2014', 'Wintersemester 2014/2015'), ('ss2014', 'Sommersemester 2014'), ('ws2013', 'Wintersemester 2013/2014'), ('ss2013', 'Sommersemester 2013'), ('ws2012', 'Wintersemester 2012/2013'), ('ss2012', 'Sommersemester 2012'), ('ws2011', 'Wintersemester 2011/2012'), ('ss2011', 'Sommersemester 2011'), ('ws2010', 'Wintersemester 2010/2011'), ('ss2010', 'Sommersemester 2010')], default='ss2021', max_length=255),
        ),
    ]