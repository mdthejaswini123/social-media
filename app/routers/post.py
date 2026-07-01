from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
# allow us to define a router for the post endpoints, and we can use the prefix argument to specify that all the endpoints in this router will have the prefix /posts, like this:
router = APIRouter(
    prefix="/posts",
    # the tags argument allows us to group the endpoints in this router under a specific tag in the OpenAPI documentation, which can help organize the documentation and make it easier to navigate. In this case, we are grouping all the post endpoints under the "Posts" tag.
    tags=["Posts"]
)

# mentioned response_model=list[schemas.Post] because we are returning a list of posts, and we want to specify the type of the items in the list using the Post model from the schemas module. This way, FastAPI can automatically validate the response data and generate the appropriate OpenAPI documentation for the endpoint.


@router.get("/", response_model=list[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    # # to fetch post from database we can use the cursor object to execute a SQL query,
    # cursor.execute("SELECT * FROM posts")
    # # and then use the fetchall() method to get all the results, like this:
    # posts = cursor.fetchall()
    return posts


@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, response: Response, db: Session = Depends(get_db)):
    # cursor.execute("SELECT * FROM posts WHERE id = %s", str((id),))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id {id} not found"}
        # we can raise an HTTPException instead of setting the response status code and returning a message, like this:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # to inert a new post into the database, we can use the cursor object to execute an INSERT SQL query like this:
    # hre to get the request body using sanity check we do it by %s and then we pass the values as a tuple in the second argument of the execute() method, like this:
    # cursor.execute("INSERT INTO posts(title,content,published) VALUES(%s,%s,%s)RETURNING *",
    #                (post.title, post.content, post.published))
    new_post = models.Post(**post.model_dump())
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    db.add(new_post)
    db.commit()

    db.refresh(new_post)
    # this is staging the data to be inserted into the database, and then we can use the fetchone() method to get the newly inserted post, like this:
    # new_post = cursor.fetchone()
    # to actually insert the data into the database, we need to call the commit() method on the connection object, like this:
    # conn.commit()
    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", str((id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} doest not exist")

    post.delete(synchronize_session=False)
    db.commit()
    return (Response(status_code=status.HTTP_204_NO_CONTENT))


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("UPDATE posts SET title=%s,content=%s,published=%s WHERE id = %s RETURNING *",
    #                (post.title, post.content, post.published, str((id),)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    print(post_query)
    if post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")
    # post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.query(models.Post).filter(models.Post.id == id).update(
        updated_post.model_dump(), synchronize_session=False)

    db.commit()
    return updated_post
