import os
from github import Github
from datetime import datetime
import pytz

def update_readme():
    """
    Updates the README.md of specified GitHub repositories by appending the current date.
    """
    try:
        # 从环境变量中获取GitHub个人访问令牌和目标仓库列表
        github_token = os.environ['GH_PAT']
        repo_list_str = os.environ['TARGET_REPOS']
        target_repos = [repo.strip() for repo in repo_list_str.split(',')]

        # 使用令牌进行认证
        g = Github(github_token)

        # 设置时区为北京时间
        tz = pytz.timezone('Asia/Shanghai')
        current_date = datetime.now(tz).strftime("%Y年%m月%d日更新")
        update_line = f"\n{current_date}\n"

        commit_message = f"docs: auto update README.md on {datetime.now(tz).strftime('%Y-%m-%d, %H:%M:%S')}"

        for repo_name in target_repos:
            try:
                print(f"Processing repository: {repo_name}")
                # 获取仓库对象
                repo = g.get_repo(repo_name)

                # 获取README.md文件的内容
                readme_file = repo.get_contents("README.md")
                original_content = readme_file.decoded_content.decode("utf-8")

                # 追加更新日期
                new_content = original_content.rstrip() + update_line

                # 更新README.md文件
                repo.update_file(
                    path="README.md",
                    message=commit_message,
                    content=new_content,
                    sha=readme_file.sha,
                    branch="main"  # 或者您的主分支名称
                )
                print(f"Successfully updated README.md in {repo_name}")

            except Exception as e:
                print(f"Error updating repository {repo_name}: {e}")

    except KeyError as e:
        print(f"Error: Environment variable {e} not set.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    update_readme()