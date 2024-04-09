from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import func

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Validator for name
    @validates('name')
    def validate_name(self, key, name):
        if len(name) <= 0:
            raise ValueError("Name is required")
        if Author.query.filter(Author.name == name).first():
            raise ValueError("Name must be unique.")
        return name
    
    # Validator for phone_number
    @validates("phone_number")
    def validate_phone_number(self, key, phone_number):
        if len(phone_number) != 10:
            raise ValueError("Phone number must be exactly ten digits.")
        return phone_number
    
    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Validator for content
    @validates('content')
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError("Content must be at least 250 characters long.")
        return content

    # Validator for summary
    @validates('summary')
    def validate_summary(self, key, summary):
        if summary and len(summary) > 250:
            raise ValueError("Summary must be maximum of 250 characters long.")
        return summary

    # Validator for category
    @validates('category')
    def validate_category(self, key, category):
        if category not in ['Fiction', 'Non-Fiction']:
            raise ValueError("Category must be either 'Fiction' or 'Non-Fiction'.")
        return category

    # Validator for title
    @validates('title')
    def validate_title(self, key, title):
        clickbait_keywords = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(keyword in title for keyword in clickbait_keywords):
            raise ValueError("Title must contain at least one clickbait keyword.")
        return title

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title}, content={self.content}, summary={self.summary})'
