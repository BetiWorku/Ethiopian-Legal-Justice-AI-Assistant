## Task 2 Deliverables
 ## GitHub Repository Setup and Branch Workflow

The project was connected to GitHub using Git version control. A separate development branch was created to follow team collaboration practices and avoid direct changes to the main branch.

### 1. Initialize Git Repository

Initialize Git inside the project folder:

git init

### 2. Add Project Files

Add all project files to Git staging:
git add .

### 3. Create Initial Commit

Commit the project files:

git commit -m "Add development environment setup"

### 4. Create Development Branch

A separate branch was created for development work:

git checkout -b betelhemdevelopment

Verify current branch:
git branch

### 5. Connect Local Repository with GitHub

Add the remote GitHub repository:
git remote add origin https://github.com/BetiWorku/Ethiopian-Legal-Justice-AI-Assistant.git

### 6. Push Development Branch to GitHub

Push the created branch:
git push -u origin betelhemdevelopment

The development branch was successfully pushed to the GitHub repository.

### 7. Create Pull Request

After pushing the branch:

1. Open the GitHub repository.
2. Navigate to **Pull Requests**.
3. Click **New Pull Request**.
4. Select:
   - Base branch: `main`
   - Compare branch: `betelhem-development-setup`
5. Create the Pull Request for review or merged sucessfully.