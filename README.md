# README-Updater-Action

[中文版](README-CN.md)

This is a Python script powered by GitHub Actions to automatically append the current date to the end of `README.md` files in one or more specified repositories.

This project is useful for scenarios that require demonstrating continuous project activity or need automated updates, such as personal portfolios, project status dashboards, and more, can also used to prevent GitHub actions from automatically shutting down workflows when the repository is not updated for 60 days.

## Features

- **Automated Updates**: Runs on a schedule or manual trigger via GitHub Actions, requiring no manual intervention.
- **Batch Processing**: Supports updating multiple target repositories in a single run.
- **Timezone Aware**: Uses the Beijing timezone (`Asia/Shanghai`) by default to generate accurate date stamps.
- **Consistent Formatting**: Automatically handles trailing blank lines in the `README.md` file to ensure consistent formatting with each update.
- **Flexible Configuration**: Uses environment variables to configure the GitHub Personal Access Token and the list of target repositories, keeping sensitive information secure.

## How to Use

To use this script, you need to set it up as a GitHub Actions workflow. Follow these steps:

### 1. Prepare a Personal Access Token (PAT)

This script requires a GitHub Personal Access Token (PAT) with `repo` scope to modify files in your repositories.

1.  Navigate to your GitHub **Settings** > **Developer settings** > **Personal access tokens** > **Tokens (classic)**.
2.  Click **Generate new token** and select **Generate new token (classic)**.
3.  Add a descriptive note for the token (e.g., `README_UPDATER_TOKEN`).
4.  Under **Select scopes**, check the `repo` box.
5.  Click **Generate token**.
6.  **Copy the generated token immediately**. You will not be able to see it again.

### 2. Set up Repository Secrets

To securely use your token and configure the repository list, you must add them as encrypted secrets in the repository where the Action will run.

1.  In the repository that will run this Action, go to **Settings** > **Secrets and variables** > **Actions**.
2.  Click **New repository secret** to create the following two secrets:
    *   **`GH_PAT`**:
        *   **Name**: `GH_PAT`
        *   **Secret**: Paste the Personal Access Token you generated in the previous step.
    *   **`TARGET_REPOS`**:
        *   **Name**: `TARGET_REPOS`
        *   **Secret**: Enter the list of repositories you want to update, formatted as `username/repo-name`. Separate multiple repositories with a comma.
          Example: `your-username/repo1,your-username/repo2`

### 3. Create a GitHub Actions Workflow

1.  In the root of your repository, create a directory named `.github/workflows` if it doesn't already exist.
2.  Inside this directory, create a new `.yml` file, for example, `update_readme.yml`.
3.  Paste the following workflow configuration into the file:

    ```yaml
    name: Auto Update README

    on:
      # 1. Scheduled trigger: Uses a cron expression. This example runs at midnight UTC (8:00 AM Beijing time) every day.
      schedule:
        - cron: '0 0 * * *'

      # 2. Manual trigger: Allows you to run this workflow manually from the Actions tab.
      workflow_dispatch:

    jobs:
      update:
        runs-on: ubuntu-latest
        steps:
          - name: Checkout repository
            uses: actions/checkout@v4

          - name: Set up Python
            uses: actions/setup-python@v5
            with:
              python-version: '3.10'

          - name: Install dependencies
            run: |
              python -m pip install --upgrade pip
              pip install PyGithub pytz

          - name: Run README update script
            env:
              GH_PAT: ${{ secrets.GH_PAT }}
              TARGET_REPOS: ${{ secrets.TARGET_REPOS }}
            run: python your_script_name.py # Replace "your_script_name.py" with the name of your script file
    ```


### 4. Commit and Verify

Commit the Python script and the `.github/workflows/update_readme.yml` file to your repository.

- **Scheduled Trigger**: The workflow will run automatically according to the `cron` schedule you set.
- **Manual Trigger**: To test it, go to the **Actions** tab of your repository, select the "Auto Update README" workflow, and click the **Run workflow** button.

After a successful run, you will see that the `README.md` files in your target repositories have been updated with the current date at the end.

## Script Dependencies

- **PyGithub**: To interact with the GitHub API.
- **pytz**: To handle timezones for accurate timestamps.

These dependencies are automatically installed by the `pip install` command in the GitHub Actions workflow.

## Contributing

Contributions are welcome via Pull Requests or Issues.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

2025年09月28日更新

2025年09月28日20:37:23更新

2025年10月01日11:42:03更新

2025年11月01日11:42:12更新

2025年12月01日12:10:12更新

