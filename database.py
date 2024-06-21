from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
import asyncio

DATABASE_URL = "mysql+aiomysql://root@localhost/pashabd"

class workwithbd:
    def __init__(self) -> None:
        self.engine = create_async_engine(DATABASE_URL, echo=True, future=True)
        self.async_session = sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )
        self.Base = declarative_base()

    async def check_connection(self):
        try:
            async with self.async_session() as session:
                result = await session.execute(text("SELECT 1"))
                print("Подключение к базе данных успешно!")
        except SQLAlchemyError as e:
            print(f"Ошибка подключения к базе данных: {e}")

    async def get_courses(self):
        async with self.async_session() as session:
            stmt = text("SELECT CourseId, Name, Description, Url, ProfileId FROM Courses;")
            result = await session.execute(stmt)
            rows = result.all()
            await session.commit()
            return rows

    async def get_users(self):
        async with self.async_session() as session:
            stmt = text("SELECT UserId, Username, Password, Email, Surname, Name, Lastname, Created_at, CourseId FROM Users;")
            result = await session.execute(stmt)
            rows = result.all()
            await session.commit()
            return rows

    async def get_profiles(self):
        async with self.async_session() as session:
            stmt = text("SELECT ProfileId, NameProfile, Url FROM Profile;")
            result = await session.execute(stmt)
            rows = result.all()
            await session.commit()
            return rows

    async def post_course(self, name, description, url, profile_id):
        try:
            async with self.async_session() as session:
                stmt = text(
                    "INSERT INTO Courses (Name, Description, Url, ProfileId) VALUES (:name, :description, :url, :profile_id);"
                )
                params = {
                    "name": name,
                    "description": description,
                    "url": url,
                    "profile_id": profile_id,
                }
                result = await session.execute(stmt, params)
                await session.commit()
                return result.lastrowid
        except SQLAlchemyError as e:
            print(f"Ошибка при добавлении курса: {e}")

    async def post_user(self, username, password, email, surname, name, lastname, course_id):
        try:
            async with self.async_session() as session:
                stmt = text(
                    "INSERT INTO Users (Username, Password, Email, Surname, Name, Lastname, CourseId) VALUES (:username, :password, :email, :surname, :name, :lastname, :course_id);"
                )
                params = {
                    "username": username,
                    "password": password,
                    "email": email,
                    "surname": surname,
                    "name": name,
                    "lastname": lastname,
                    "course_id": course_id,
                }
                result = await session.execute(stmt, params)
                await session.commit()
                return result.lastrowid
        except SQLAlchemyError as e:
            print(f"Ошибка при добавлении пользователя: {e}")

    async def post_profile(self, name_profile, url):
        try:
            async with self.async_session() as session:
                stmt = text(
                    "INSERT INTO Profile (NameProfile, Url) VALUES (:name_profile, :url);"
                )
                params = {
                    "name_profile": name_profile,
                    "url": url,
                }
                result = await session.execute(stmt, params)
                await session.commit()
                return result.lastrowid
        except SQLAlchemyError as e:
            print(f"Ошибка при добавлении профиля: {e}")

    async def update_course(self, course_id, name, description, url, profile_id):
        try:
            async with self.async_session() as session:
                stmt = text(
                    "UPDATE Courses SET Name = :name, Description = :description, Url = :url, ProfileId = :profile_id WHERE CourseId = :course_id;"
                )
                params = {
                    "course_id": course_id,
                    "name": name,
                    "description": description,
                    "url": url,
                    "profile_id": profile_id,
                }
                result = await session.execute(stmt, params)
                await session.commit()
        except SQLAlchemyError as e:
            print(f"Ошибка при обновлении курса: {e}")

    async def post_anketas(self, fio, telephone, email, soobsh):
        try:
            async with self.async_session() as session:
                stmt = text(
                    "INSERT INTO anketa (fio, telephone, email, soobsh) VALUES (:fio, :telephone, :email, :soobsh);"
                )
                params = {
                    "fio": fio,
                    "telephone": telephone,
                    "email": email,
                    "soobsh": soobsh,
                }
                result = await session.execute(stmt, params)
                await session.commit()
                return result.lastrowid
        except SQLAlchemyError as e:
            print(f"Ошибка при добавлении анкеты: {e}")

    async def update_user(self, user_id, username, password, email, surname, name, lastname, course_id):
        try:
            async with self.async_session() as session:
                stmt = text(
                    "UPDATE Users SET Username = :username, Password = :password, Email = :email, Surname = :surname, Name = :name, Lastname = :lastname, CourseId = :course_id WHERE UserId = :user_id;"
                )
                params = {
                    "user_id": user_id,
                    "username": username,
                    "password": password,
                    "email": email,
                    "surname": surname,
                    "name": name,
                    "lastname": lastname,
                    "course_id": course_id,
                }
                result = await session.execute(stmt, params)
                await session.commit()
        except SQLAlchemyError as e:
            print(f"Ошибка при обновлении пользователя: {e}")

    async def update_profile(self, profile_id, name_profile, url):
        try:
            async with self.async_session() as session:
                stmt = text(
                    "UPDATE Profile SET NameProfile = :name_profile, Url = :url WHERE ProfileId = :profile_id;"
                )
                params = {
                    "profile_id": profile_id,
                    "name_profile": name_profile,
                    "url": url,
                }
                result = await session.execute(stmt, params)
                await session.commit()
        except SQLAlchemyError as e:
            print(f"Ошибка при обновлении профиля: {e}")