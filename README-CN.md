# README-Updater-Action

这是一个基于 GitHub Actions 的 Python 脚本，用于自动在指定的一个或多个仓库的 `README.md` 文件末尾追加当前日期。

这个项目对于需要展示项目持续活跃、或者有自动化更新需求的场景非常有用，例如个人作品集、项目状态面板等，也用于避免github actions在60天未更新仓库时自动关闭workflows。

## 功能特性

- **自动化更新**：通过 GitHub Actions 实现定时或手动触发，无需人工干预。
- **批量处理**：支持一次性更新多个目标仓库。
- **时区感知**：默认使用北京时间（`Asia/Shanghai`）生成日期戳，确保时间准确性。
- **格式统一**：自动处理 `README.md` 文件末尾的空行，确保每次追加的格式一致。
- **灵活配置**：通过环境变量配置 GitHub 个人访问令牌和目标仓库列表，保护敏感信息。

## 如何使用

要使用此脚本，您需要将其设置为一个 GitHub Actions 工作流程。以下是详细步骤：

### 1. 准备个人访问令牌 (PAT)

此脚本需要一个具有 `repo` 范围权限的 GitHub 个人访问令牌 (PAT) 才能修改您的仓库文件。

1.  前往您的 GitHub **Settings** > **Developer settings** > **Personal access tokens** > **Tokens (classic)**。
2.  点击 **Generate new token** 并选择 **Generate new token (classic)**。
3.  为令牌添加一个描述性的备注（例如 `README_UPDATER_TOKEN`）。
4.  在 **Select scopes** 中，勾选 `repo` 权限。
5.  点击 **Generate token**。
6.  **立即复制生成的令牌**，您将无法再次看到它。

### 2. 在仓库中设置 Secrets

为了安全地使用令牌和配置仓库列表，您需要将它们设置为 GitHub Actions 的加密机密 (Secrets)。

1.  在将要运行此 Action 的仓库中，进入 **Settings** > **Secrets and variables** > **Actions**。
2.  点击 **New repository secret**，创建以下两个机密：
    *   **`GH_PAT`**:
        *   **Name**: `GH_PAT`
        *   **Secret**: 粘贴您在上一步中生成的个人访问令牌。
    *   **`TARGET_REPOS`**:
        *   **Name**: `TARGET_REPOS`
        *   **Secret**: 输入您想要更新的仓库列表，格式为 `用户名/仓库名`，多个仓库之间用逗号分隔。
          例如：`your-username/repo1,your-username/repo2`

### 3. 创建 GitHub Actions 工作流

1.  在您的仓库根目录下，创建一个名为 `.github/workflows` 的文件夹（如果尚不存在）。
2.  在该文件夹中，创建一个 `.yml` 文件，例如 `update_readme.yml`。
3.  将以下工作流配置粘贴到文件中：

    ```yaml
    name: Auto Update README

    on:
      # 1. 定时触发：使用 Cron 表达式，例如每天的北京时间早上 8 点触发
      schedule:
        - cron: '0 0 * * *' # UTC 时间午夜，即北京时间早上 8 点

      # 2. 手动触发：允许在 Actions 页面手动运行此工作流
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
            run: python your_script_name.py # 将 "your_script_name.py" 替换为您的脚本文件名
    ```


### 4. 提交并验证

将 Python 脚本和 `.github/workflows/update_readme.yml` 文件提交到您的仓库。

- **定时触发**：工作流将根据您设置的 `cron` 表达式自动运行。
- **手动触发**：您可以前往仓库的 **Actions** 标签页，找到 "Auto Update README" 工作流，然后点击 **Run workflow** 手动触发一次以进行测试。

运行成功后，您可以看到目标仓库的 `README.md` 文件末尾被追加了更新日期。

## 脚本依赖

- **PyGithub**: 用于与 GitHub API 进行交互。
- **pytz**: 用于处理时区，确保日期时间准确。

这些依赖项会在 GitHub Actions 工作流中通过 `pip install` 命令自动安装。

## 贡献

欢迎通过 Pull Requests 或 Issues 对此项目做出贡献。

## 许可证

本项目采用 MIT 许可证。详情请参阅 [LICENSE](LICENSE) 文件。

