from sqlalchemy.orm import Session
from prompt_toolkit import prompt
from database import init_db, get_db
from models import User, Post, Comment

def hash_password(password):
    return password

def authenticate_user(db: Session, username: str, password: str):
    user = User.get_user(db, username)
    if user and user.password == hash_password(password):
        return user
    return None

def user_menu(db: Session, user: User):
    while True:
        action = prompt("Enter 'Create post', 'Delete post', 'Comment', 'Delete comment', 'Logout': ").strip().lower()
        if action == "create post":
            title = prompt("Title: ")
            content = prompt("Content: ")
            Post.create_post(db, title, content, user.id)
            print("Post created successfully!")
        elif action == "delete post":
            post_id = prompt("Post ID: ")
            if Post.delete_post(db, int(post_id), user.id):
                print("Post deleted successfully!")
            else:
                print("Post not found or you don't have permission to delete it.")
        elif action == "comment":
            post_id = prompt("Post ID: ")
            content = prompt("Comment: ")
            Comment.create_comment(db, content, int(post_id), user.id)
            print("Comment added successfully!")
        elif action == "delete comment":
            post_id = prompt("Post ID: ")
            author_id = prompt("Author ID: ")
            if Comment.delete_comment(db, int(post_id), int(author_id)):
                print("Comment deleted successfully!")
            else:
                print("Comment not found.")
        elif action == "logout":
            break
        else:
            print("Invalid action, please try again.")

def main():
    init_db()
    db = next(get_db())
    print("Welcome to My blog CLI. Enjoy!")
    while True:
        action = prompt("Enter 'Login', 'Register', or 'Exit': ").strip().lower()
        if action == "register":
            username = prompt("Username: ")
            password = prompt("Password: ", is_password=True)
            User.create_user(db, username, hash_password(password))
            print(f"User {username} registered successfully!")
        elif action == "login":
            username = prompt("Username: ")
            password = prompt("Password: ", is_password=True)
            user = authenticate_user(db, username, password)
            if user:
                print(f"Welcome back, {user.username}!")
                user_menu(db, user)
            else:
                print("Invalid credentials, please try again.")
        elif action == "exit":
            break
        else:
            print("Invalid action, please try again.")

if __name__ == "__main__":
    main()
