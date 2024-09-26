from datacenter.models import Schoolkid, Mark, Chastisement, Commendation, Teacher, Subject, Lesson
import random 


def get_schoolkid(schoolkid_name):
    try:
        return Schoolkid.objects.get(full_name__contains=schoolkid_name)
    except Schoolkid.DoesNotExist:
        raise ValueError(f"Ученик с именем {schoolkid_name} не найден.")
    except Schoolkid.MultipleObjectsReturned:
        raise ValueError(f"Найдено несколько учеников с именем {schoolkid_name}. Уточните запрос.")


def fix_marks(schoolkid_name):
    try:
        schoolkid = get_schoolkid(schoolkid_name)
        bad_marks = Mark.objects.filter(schoolkid=schoolkid, points__in=[2,3])
        
        bad_marks.update(points=5)
            
        print(f"Все оценки {schoolkid_name} были изменены :)")
        
    except ValueError as e:
        print(e)
        
        
def fix_chastisements(schoolkid_name):
    try:
        schoolkid = get_schoolkid(schoolkid_name)
        chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
        
        chastisements.delete()
        
        print(f"Все замечания {schoolkid_name} были удалены :)")

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        

def create_commendation(schoolkid_name, subject_title):
    try:
        commendations = [
            "Молодец",
            "Хорошая активность на уроке!",
            "Хвалю",
            "Отличная работа!"
        ]
        schoolkid = get_schoolkid(schoolkid_name)
        subject = Subject.objects.filter(title=subject_title, year_of_study=schoolkid.year_of_study).first()
        
        if not subject:
            print(f"Предмет '{subject_title}' не найден. Проверьте правильность написания.")
            return
        
        
        lesson = Lesson.objects.filter(
            year_of_study=schoolkid.year_of_study,
            group_letter=schoolkid.group_letter,
            subject=subject 
        ).order_by('-date').first()
    
        commendation_text = random.choice(commendations)
    
        Commendation.objects.create(
            text=commendation_text,
            created=lesson.date,
            schoolkid=schoolkid,
            subject=subject,
            teacher=lesson.teacher
        )
    
        print(f"Похвала {schoolkid_name} по уроку {subject_title} была добавлена")
    
    except ValueError as e:
        print(e)
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    
