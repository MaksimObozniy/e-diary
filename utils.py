from datacenter.models import Schoolkid, Mark, Chastisement, Commendation, Teacher, Subject, Lesson
import random 


def fix_marks(schoolkid_name):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_name)
        bad_marks = Mark.objects.filter(schoolkid=schoolkid, points__in=[2,3])
        
        for mark in bad_marks:
            mark.points = 5
            mark.save()
            
        print(f"Все оценки {schoolkid_name} были изменены :)")
        
    except Schoolkid.DoesNotExist:
        print(f"Ученик с именем {schoolkid_name} не найден")
        
        
def fix_chastisements(schoolkid_name):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_name)
        chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
        
        for chastisement in chastisements:
            chastisement.delete()
        print(f"Все замечания {schoolkid_name} были удалены :)")
        
    except Schoolkid.DoesNotExist:
        print(f"Ученик с именем {schoolkid_name} не найден")
        

def create_commendation(schoolkid_name, subject_title):
    try:
        commendations = [
            "Молодец",
            "Хорошая активность на уроке!",
            "Хвалю",
            "Отличная работа!"
        ]
        schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_name)
        subject = Subject.objects.filter(title=subject_title, year_of_study=schoolkid.year_of_study).first()
    
        lesson = Lesson.objects.filter(
            year_of_study=schoolkid.year_of_study,
            group_letter=schoolkid.group_letter,
            subject=subject 
        ).first()
    
        commendation_text = random.choice(commendations)
    
        Commendation.objects.create(
            text=commendation_text,
            created=lesson.date,
            schoolkid=schoolkid,
            subject=subject,
            teacher=lesson.teacher
        )
    
        print(f"Похвала {schoolkid_name} по уроку {subject_title} была добавлена")
    
    except Schoolkid.DoesNotExist:
        print(f"Ученик с именем {schoolkid_name} не найден")
    except Schoolkid.MultipleObjectsReturned:
        print(f"Найдено несколько учеников с именем {schoolkid_name}. Уточните запрос")   
    except ValueError as e:
        print(e)
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    
