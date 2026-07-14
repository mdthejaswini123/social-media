from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, text, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
# to create a new table in the database, we need to define a new class that inherits from the Base class, and we need to specify the name of the table using the __tablename__ attribute. We also need to define the columns of the table using the Column class, and we need to specify the data type of each column using the appropriate data type class (e.g., Integer, String, Boolean). Finally, we need to specify any additional constraints on the columns (e.g., primary key, nullable) using the appropriate parameters of the Column class.

# SQLALCHEMY does not update the database automatically when we make changes to the models, we need to use a migration tool like Alembic to manage the database schema changes. Alembic allows us to create migration scripts that can be used to update the database schema when we make changes to the models. We can use the command line interface of Alembic to create and apply migration scripts, and we can also use it to generate new migration scripts based on the changes we have made to the models. This way, we can keep our database schema in sync with our models and avoid any issues that may arise from schema mismatches.


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False,)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User")  # this is to create a relationship between the Post and User models, so that we can access the user who created the post using the owner attribute of the Post model. We can also use this relationship to access all the posts created by a user using the posts attribute of the User model. This is done by specifying the name of the related model (User) as an argument to the relationship() function, and we can also specify any additional parameters (e.g., back_populates) to customize the relationship behavior.


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
