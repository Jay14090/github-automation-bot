from github import Github, Auth
from dotenv import load_dotenv
import os
import datetime


def run_bot():
    load_dotenv()

    TOKEN = os.getenv("GITHUB_TOKEN")

    if not TOKEN:
        raise Exception("GitHub token not found.")

    # Authenticate
    auth = Auth.Token(TOKEN)
    g = Github(auth=auth)

    user = g.get_user()

    # 🔹 CHANGE THIS IF YOUR REPO NAME IS DIFFERENT
    repo_name = "auto-repo-20260218112957"
    repo = user.get_repo(repo_name)

    file_name = "activity.txt"

    # ===============================
    # 1️⃣ Commit to MAIN branch
    # ===============================

    contents = repo.get_contents(file_name)
    existing_content = contents.decoded_content.decode()

    new_line = "\nAutomated update at " + str(datetime.datetime.now())
    updated_content = existing_content + new_line

    repo.update_file(
        path=file_name,
        message="Automated daily log update",
        content=updated_content,
        sha=contents.sha,
    )

    print("Main branch commit successful!")

    # ===============================
    # 2️⃣ Create Issue
    # ===============================

    issue_title = "Automated Issue - " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    issue_body = "This issue was created automatically by the bot."

    repo.create_issue(title=issue_title, body=issue_body)

    print("Issue created successfully!")

    # ===============================
    # 3️⃣ Create New Branch
    # ===============================

    base_branch = repo.get_branch("main")
    new_branch_name = "auto-branch-" + datetime.datetime.now().strftime("%H%M%S")

    repo.create_git_ref(
        ref="refs/heads/" + new_branch_name,
        sha=base_branch.commit.sha,
    )

    print("New branch created:", new_branch_name)

    # ===============================
    # 4️⃣ Commit inside New Branch
    # ===============================

    contents = repo.get_contents(file_name)

    branch_updated_content = (
        contents.decoded_content.decode()
        + "\nBranch change at "
        + str(datetime.datetime.now())
    )

    repo.update_file(
        path=file_name,
        message="Automated branch update",
        content=branch_updated_content,
        sha=contents.sha,
        branch=new_branch_name,
    )

    print("Branch commit successful!")

    # ===============================
    # 5️⃣ Create Pull Request
    # ===============================

    pr_title = "Automated PR - " + datetime.datetime.now().strftime("%H:%M:%S")
    pr_body = "This PR was created automatically by the bot."

    pull_request = repo.create_pull(
        title=pr_title,
        body=pr_body,
        head=new_branch_name,
        base="main",
    )

    print("Pull Request created successfully!")

    # ===============================
    # 6️⃣ Merge Pull Request
    # ===============================

    pull_request.merge()
    print("Pull Request merged successfully!")

    # ===============================
    # 7️⃣ Delete Branch After Merge
    # ===============================

    repo.get_git_ref(f"heads/{new_branch_name}").delete()
    print("Branch deleted successfully!")


if __name__ == "__main__":
    run_bot()
