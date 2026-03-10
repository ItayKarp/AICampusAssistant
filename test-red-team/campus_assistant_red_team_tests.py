import json
import os
import sys
from dataclasses import dataclass, asdict
from datetime import date, time
from pathlib import Path


@dataclass
class TestResult:
    id: str
    name: str
    status: str
    observed: str
    expected: str
    risk: str


def run() -> list[TestResult]:
    project_path = Path(r"C:\Users\badonke\PycharmProjects\CampusAssistantAI")
    if not project_path.exists():
        raise FileNotFoundError(f'Project path not found: {project_path}')

    os.environ['PYTHONPATH'] = str(project_path)
    os.environ['DATABASE_URL'] = r"C:\Users\badonke\PycharmProjects\CampusAssistantAI\test-red-team"
    os.environ['GEMINI_API_KEY'] = 'test-key'
    sys.path.insert(0, str(project_path))

    from infrastructure.db import Base, engine, Session
    from infrastructure.db import Course, Exam, Office, OfficeOpeningHour
    from infrastructure.repositories import SqlAlchemyCoursesRepo, SqlAlchemyExamRepo, SqlAlchemyOfficeRepo
    import services.ai_handler_service as assistant_service_module
    from services import AssistantService
    from fastapi.testclient import TestClient
    from app import app

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    with Session() as s:
        c1 = Course(class_code='20451', class_name='Database Systems', lecturer='Dr. Ada', semester='A')
        c2 = Course(class_code='30001', class_name='Calculus I', lecturer='Dr. Euler', semester='B')
        s.add_all([c1, c2])
        s.flush()
        s.add_all([
            Exam(course_id=c1.id, exam_date=date(2026, 6, 1), exam_time=time(9, 0), room='B201', type='final'),
            Exam(course_id=c2.id, exam_date=date(2026, 6, 2), exam_time=time(10, 0), room='A101', type='midterm'),
        ])
        office = Office(
            office_name='Finance Office',
            room_number=12,
            phone='123',
            email='finance@campus.edu',
            building='Main',
            staff_name='Dana',
        )
        s.add(office)
        s.flush()
        s.add_all([
            OfficeOpeningHour(office_id=office.id, day_of_week='Sunday', open_time=time(8, 0), close_time=time(12, 0)),
            OfficeOpeningHour(office_id=office.id, day_of_week='Monday', open_time=time(9, 0), close_time=time(13, 0)),
        ])
        s.commit()

    course_repo = SqlAlchemyCoursesRepo()
    exam_repo = SqlAlchemyExamRepo()
    office_repo = SqlAlchemyOfficeRepo()
    service = AssistantService(exam_repo=exam_repo, office_repo=office_repo, courses_repo=course_repo)
    client = TestClient(app, raise_server_exceptions=False)

    results: list[TestResult] = []

    def add(test_id: str, name: str, ok: bool, observed: str, expected: str, risk: str):
        results.append(
            TestResult(
                id=test_id,
                name=name,
                status='PASS' if ok else 'FAIL',
                observed=observed,
                expected=expected,
                risk=risk,
            )
        )

    # Repository contract tests
    res = course_repo.get_results({'relevant_columns': ['class_name', 'class_code'], 'filters': {'course_name': 'Database Systems'}}, '', None)
    add('T01', 'Course lookup by course_name', res['count'] == 1, json.dumps(res), 'Exactly 1 matching course', 'Low')

    res = course_repo.get_results({'relevant_columns': ['class_name', 'class_code'], 'filters': {'class_code': 20451}}, '', None)
    add('T02', 'Course lookup by class_code filter from classifier contract', res['count'] == 1, json.dumps(res), 'Exactly 1 matching course', 'High')

    res = exam_repo.get_results({'relevant_columns': ['exam_date', 'room'], 'filters': {'room': 'B201'}}, '', None)
    add('T03', 'Exam lookup by room', res['count'] == 1, json.dumps(res), 'Exactly 1 matching exam', 'Low')

    res = exam_repo.get_results({'relevant_columns': ['exam_date', 'room'], 'filters': {'course_name': 'Database Systems'}}, '', None)
    add('T04', 'Exam lookup by course_name from classifier contract', res['count'] == 1, json.dumps(res), 'Exactly 1 matching exam', 'Critical')

    res = office_repo.get_results({'relevant_columns': ['day_of_week', 'open_time', 'close_time', 'office_name'], 'filters': {'office_name': 'Finance Office', 'day': 'Sunday'}}, '', None)
    add('T05', 'Office hours lookup by internal day key', res['count'] == 1, json.dumps(res), 'Exactly 1 matching office-hours row', 'Low')

    res = office_repo.get_results({'relevant_columns': ['day_of_week', 'open_time', 'close_time', 'office_name'], 'filters': {'office_name': 'Finance Office', 'day_of_week': 'Sunday'}}, '', None)
    add('T06', 'Office hours lookup by day_of_week from classifier contract', res['count'] == 1, json.dumps(res), 'Exactly 1 matching office-hours row', 'High')

    res = office_repo.get_results({'relevant_columns': ['day_of_week'], 'filters': {'office_name': 'Finance Office', 'day': 'notaday'}}, '', None)
    add('T07', 'Invalid office day rejected', res['count'] == 0 and res['message'] == 'Invalid day filter.', json.dumps(res), 'Validation error message', 'Low')

    # Service-layer tests
    assistant_service_module.respond = lambda uq, cls, data: 'ok'
    assistant_service_module.classify_prompt = lambda q: json.dumps({
        'category': 'faq',
        'table': 'faq_items',
        'relevant_columns': ['question', 'answer'],
        'related_tables': [],
        'filters': {},
        'confidence': 0.9,
    })
    res = service.handle_question('How do I reset my password?')
    add('T08', 'Unsupported category returned by classifier', bool(res.get('data')), json.dumps(res), 'Supported handler or explicit unsupported-category error', 'High')

    assistant_service_module.classify_prompt = lambda q: 'not json at all'
    res = service.handle_question('bad json please')
    add('T09', 'Malformed classifier JSON handled', res['classification'] is None and 'couldn’t understand' in res['answer'].lower(), json.dumps(res), 'Graceful classification failure', 'Medium')

    assistant_service_module.classify_prompt = lambda q: (_ for _ in ()).throw(RuntimeError('quota detail should not leak'))
    res = service.handle_question('trigger classifier exception')
    add('T10', 'Classifier exception sanitization', 'quota detail should not leak' not in res['answer'], json.dumps(res), 'Sanitized public error message', 'High')

    assistant_service_module.classify_prompt = lambda q: json.dumps({
        'category': 'courses',
        'table': 'courses',
        'relevant_columns': ['class_name'],
        'related_tables': [],
        'filters': {},
        'confidence': 0.9,
    })
    assistant_service_module.respond = lambda uq, cls, data: (_ for _ in ()).throw(RuntimeError('responder boom'))
    resp = client.post('/ai-prompt', json={'question': 'trigger responder crash'})
    add('T11', 'Responder exception HTTP behavior', resp.status_code != 500, f'{resp.status_code} {resp.text}', 'Non-500 controlled error response', 'Critical')

    assistant_service_module.classify_prompt = lambda q: json.dumps({
        'category': 'exams',
        'table': 'exams',
        'relevant_columns': ['exam_date', 'room'],
        'related_tables': ['courses'],
        'filters': {},
        'confidence': 0.9,
    })
    assistant_service_module.respond = lambda uq, cls, data: 'ok'
    res = service.handle_question('When is my exam?', user_id=999)
    add('T12', 'Identity-aware "my" query isolation', res['data'].get('count') == 1, json.dumps(res), 'User-scoped result, not all exams', 'Critical')

    classifier_txt = (project_path / 'app' / 'infrastructure' / 'ai' / 'classifier_system_instructions.txt').read_text(encoding='utf-8')
    malformed = classifier_txt.lstrip().startswith('[') or '"""' in classifier_txt
    add('T13', 'Classifier instruction file formatting', not malformed, 'Instruction file is stored as a Python-style list/string literal, not clean plain text', 'Clean plain-text instruction content only', 'Medium')

    return results


if __name__ == '__main__':
    results = run()
    summary = {
        'passed': sum(1 for r in results if r.status == 'PASS'),
        'failed': sum(1 for r in results if r.status == 'FAIL'),
        'results': [asdict(r) for r in results],
    }
    print(json.dumps(summary, indent=2))
