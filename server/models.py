from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name', 'phone_number')
    def validate_author(self, key, value):
        if key == 'name':
            if not value or value.strip() == "":
                raise ValueError("Author must have a non-empty name")
            existing_author = Author.query.filter(Author.name == value).first()
            if existing_author:
                raise ValueError(f"Author with name '{value}' already exists")
        
            return value

        if key == 'phone_number':
            if not value.isdigit() or len(value) != 10:
                raise ValueError("Phone number must be exactly 10 digits")
            return value


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

    # Add validators  
    @validates("content", "summary", "category", "title")
    def validate_posts(self, key, value):
        if key == "content":
            if len(value) < 250:
                raise ValueError("Post must be at least 250 characters long.")
        elif key == "summary":
            if len(value) > 250:
                raise ValueError("Summary must be more than 250 characters long.")
        elif key == "category":
            if value not in ["Fiction", "Non-Fiction"]:
                raise ValueError("Category must be either Fiction or Non-Fiction.")
        elif key == "title":
            titles = ["Won't Believe", "Secret", "Top", "Guess"]
            if not any(title in value for title in titles):
                raise ValueError("Title must be one of the Titles: 'Won't Believe", "Secret", "Top", "Guess'")
        return value



    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
