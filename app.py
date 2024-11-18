import streamlit as st
from RedditManager import RedditManager  # Ensure this file is in the same directory or adjust the import path
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize RedditManager
try:
    reddit_manager = RedditManager()
except Exception as e:
    st.error(f"Failed to initialize RedditManager: {e}")

# Sidebar for selecting platform and CRUD operation
platform = st.sidebar.selectbox("Select Social Media Platform", ["Reddit", "YouTube", "Facebook", "Instagram", "Twitter", "LinkedIn"])
operation = st.sidebar.selectbox("Select Operation", ["Create Post", "Read Post", "Update Post", "Delete Post"])

# Function to fetch and display recent posts in a dropdown
def get_recent_posts_dropdown():
    # Fetch recent posts (limit can be adjusted as needed)
    recent_posts = reddit_manager.get_recent_posts(limit=10)  # Ensure get_recent_posts is defined in RedditManager
    if recent_posts:
        post_titles = {post['title']: post['id'] for post in recent_posts}
        selected_title = st.selectbox("Select a Post", list(post_titles.keys()))
        selected_post_id = post_titles[selected_title]
        return selected_post_id
    else:
        st.warning("No recent posts found.")
        return None

# Check if the platform is Reddit before proceeding
if platform == "Reddit":

    if operation == "Create Post":
        st.header("Create a New Reddit Post")

        # Get user inputs for post creation
        subreddit_name = st.text_input("Subreddit Name (without 'r/')", "")
        title = st.text_input("Post Title", "")
        content = st.text_area("Post Content", "")
        post_type = st.selectbox("Post Type", ["text", "link", "image"])

        if st.button("Create Post"):
            post_id = reddit_manager.create_post(subreddit_name, title, content, post_type)
            if post_id:
                st.success(f"Post created successfully! Post ID: {post_id}")
                post_url = f"https://www.reddit.com/r/{subreddit_name}/comments/{post_id}/"
                st.markdown(f"[View Post on Reddit]({post_url})", unsafe_allow_html=True)
            else:
                st.error("Failed to create the post.")



    elif operation == "Read Post":
        st.header("Read a Reddit Post")

        # Display dropdown for recent posts
        post_id = get_recent_posts_dropdown()
        if post_id and st.button("Fetch Post"):
            post_data = reddit_manager.read_post(post_id)
            if post_data:
                st.write("Post details:")
                st.write(post_data)
            else:
                st.error("Failed to fetch the post.")


    elif operation == "Update Post":
        st.header("Update an Existing Reddit Post")

        # Display dropdown for recent posts
        post_id = get_recent_posts_dropdown()
        new_content = st.text_area("New Content", "")
        
        if post_id and st.button("Update Post"):
            update_success = reddit_manager.update_post(post_id, new_content)
            if update_success:
                st.success("Post updated successfully!")
                # Display the link to view the updated post
                post_data = reddit_manager.read_post(post_id)
                subreddit_name = post_data.get('subreddit', 'unknown')  # Ensure subreddit name is retrieved correctly
                post_url = f"https://www.reddit.com/r/{subreddit_name}/comments/{post_id}/"
                st.markdown(f"[View Updated Post on Reddit]({post_url})", unsafe_allow_html=True)
            else:
                st.error("Failed to update the post.")

    elif operation == "Delete Post":
        st.header("Delete a Reddit Post")

        # Display dropdown for recent posts
        post_id = get_recent_posts_dropdown()
        
        if post_id and st.button("Delete Post"):
            delete_success = reddit_manager.delete_post(post_id)
            if delete_success:
                st.success("Post deleted successfully!")
                # Inform the user that the post is deleted and cannot be viewed
                st.info("Note: The post has been deleted, so it is no longer available on Reddit.")
            else:
                st.error("Failed to delete the post.")

# Placeholder for other platforms
else:
    st.write(f"{platform} integration coming soon!")
