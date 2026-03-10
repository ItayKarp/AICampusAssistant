from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    BigInteger,
    String,
    Text,
    Boolean,
    Date,
    Time,
    DateTime,
    ForeignKey,
    Numeric,
)
from sqlalchemy.orm import relationship

from .database import Base


# =========================================================
# USERS
# =========================================================
class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    password_hash = Column(Text, nullable=False)
    role = Column(String(50), nullable=False)  # student / management / admin
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_login_at = Column(DateTime, nullable=True)
    neon_user_id = Column(Text, nullable=True)

    student_profile = relationship("Student", back_populates="user", uselist=False)
    announcements_created = relationship("Announcement", back_populates="creator")
    question_logs = relationship("QuestionLog", back_populates="user")
    audit_logs = relationship("AuditLog", back_populates="actor")
    notifications = relationship("Notification", back_populates="user")
    assigned_tickets = relationship("SupportTicket", back_populates="assignee")


# =========================================================
# STUDENTS
# =========================================================
class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(Text, nullable=False)
    last_name = Column(Text, nullable=False)
    email = Column(Text, nullable=False, unique=True, index=True)
    student_number = Column(Integer, nullable=False, unique=True, index=True)
    major = Column(Text, nullable=False)
    year = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="SET NULL"), unique=True, nullable=True)

    user = relationship("User", back_populates="student_profile")
    enrollments = relationship("StudentClass", back_populates="student", cascade="all, delete-orphan")
    support_tickets = relationship("SupportTicket", back_populates="student", cascade="all, delete-orphan")


# =========================================================
# COURSES
# =========================================================
class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    class_code = Column(Text, nullable=False, unique=True, index=True)
    class_name = Column(Text, nullable=False)
    lecturer = Column(Text, nullable=False)
    semester = Column(Text, nullable=False)

    exams = relationship("Exam", back_populates="course", cascade="all, delete-orphan")
    student_links = relationship("StudentClass", back_populates="course", cascade="all, delete-orphan")


# =========================================================
# EXAMS
# =========================================================
class Exam(Base):
    __tablename__ = "exams"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    exam_date = Column(Date, nullable=False)
    exam_time = Column(Time, nullable=False)
    room = Column(Text, nullable=False)
    type = Column(Text, nullable=False)

    course = relationship("Course", back_populates="exams")


# =========================================================
# OFFICES
# =========================================================
class Office(Base):
    __tablename__ = "offices"

    id = Column(Integer, primary_key=True, index=True)
    office_name = Column(Text, nullable=False)
    room_number = Column(Integer, nullable=False)
    phone = Column(Text, nullable=False)
    email = Column(Text, nullable=False, unique=True)
    building = Column(Text, nullable=False)
    staff_name = Column(Text, nullable=True)

    opening_hours = relationship("OfficeOpeningHour", back_populates="office", cascade="all, delete-orphan")


# =========================================================
# OFFICE OPENING HOURS
# =========================================================
class OfficeOpeningHour(Base):
    __tablename__ = "office_opening_hours"

    id = Column(Integer, primary_key=True, index=True)
    office_id = Column(Integer, ForeignKey("offices.id", ondelete="CASCADE"), nullable=False)
    day_of_week = Column(Text, nullable=False)
    open_time = Column(Time, nullable=False)
    close_time = Column(Time, nullable=False)

    office = relationship("Office", back_populates="opening_hours")


# =========================================================
# STUDENT_CLASSES
# =========================================================
class StudentClass(Base):
    __tablename__ = "student_classes"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)

    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="student_links")


# =========================================================
# ANNOUNCEMENTS
# =========================================================
class Announcement(Base):
    __tablename__ = "announcements"

    id = Column(BigInteger, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    target_role = Column(String(50), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_by = Column(BigInteger, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True)

    creator = relationship("User", back_populates="announcements_created")


# =========================================================
# FAQ ITEMS
# =========================================================
class FaqItem(Base):
    __tablename__ = "faq_items"

    id = Column(BigInteger, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    category = Column(String(100), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=True)


# =========================================================
# QUESTION LOGS
# =========================================================
class QuestionLog(Base):
    __tablename__ = "question_logs"

    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    question_text = Column(Text, nullable=False)
    answer_text = Column(Text, nullable=True)
    category = Column(String(100), nullable=True)
    confidence_score = Column(Numeric(5, 2), nullable=True)
    status = Column(String(50), nullable=False, default="answered")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    user = relationship("User", back_populates="question_logs")


# =========================================================
# AUDIT LOGS
# =========================================================
class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(BigInteger, primary_key=True, index=True)
    actor_user_id = Column(BigInteger, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    action_type = Column(String(100), nullable=False)
    target_type = Column(String(100), nullable=False)
    target_id = Column(BigInteger, nullable=True)
    details = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    actor = relationship("User", back_populates="audit_logs")


# =========================================================
# NOTIFICATIONS
# =========================================================
class Notification(Base):
    __tablename__ = "notifications"

    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    user = relationship("User", back_populates="notifications")


# =========================================================
# SUPPORT TICKETS
# =========================================================
class SupportTicket(Base):
    __tablename__ = "support_tickets"

    id = Column(BigInteger, primary_key=True, index=True)
    student_id = Column(BigInteger, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    subject = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False, default="open")
    assigned_to = Column(BigInteger, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True)

    student = relationship("Student", back_populates="support_tickets")
    assignee = relationship("User", back_populates="assigned_tickets")