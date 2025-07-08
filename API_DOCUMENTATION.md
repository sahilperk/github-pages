# GitHub Pages Learning Course - API Documentation

## Overview

This repository contains a comprehensive GitHub Skills course for learning GitHub Pages. The course uses automated workflows and step-by-step instructions to guide learners through creating their first GitHub Pages site.

## Repository Structure

### Core Components

#### 1. Educational Content (`/.github/steps/`)

The course content is organized into sequential learning steps:

- **0-welcome.md** - Initial welcome message
- **1-enable-github-pages.md** - Instructions for enabling GitHub Pages
- **2-configure-your-site.md** - Site configuration guidance
- **3-customize-your-homepage.md** - Homepage customization steps
- **4-create-a-blog-post.md** - Blog post creation tutorial
- **5-merge-your-pull-request.md** - Pull request merging instructions
- **X-finish.md** - Course completion message

#### 2. Automation Workflows (`/.github/workflows/`)

Automated GitHub Actions that manage course progression:

- **0-welcome.yml** - Welcome workflow
- **1-enable-github-pages.yml** - Pages enablement automation
- **2-configure-your-site.yml** - Configuration validation
- **3-customize-your-homepage.yml** - Homepage validation
- **4-create-a-blog-post.yml** - Blog post validation
- **5-merge-your-pull-request.yml** - Final step validation

#### 3. Configuration Files

- **dependabot.yml** - Dependency update automation
- **.gitignore** - Git ignore patterns
- **LICENSE** - MIT license
- **README.md** - Main course instructions

## Public APIs and Functions

### Course Navigation API

#### Current Step Tracking
```yaml
# Location: .github/steps/-step.txt
# Purpose: Tracks the current step number for course progression
# Format: Single integer representing current step (0-5)
```

**Usage:**
```bash
# Read current step
cat .github/steps/-step.txt

# Update step (automated by workflows)
echo "1" > .github/steps/-step.txt
```

### Workflow APIs

#### Step Validation Pattern
All workflow files follow a consistent validation pattern:

```yaml
name: Step N - Description
on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: write
  pull-requests: write

jobs:
  get_current_step:
    name: Check current step number
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - id: get_step
        run: |
          echo "current_step=$(cat .github/steps/-step.txt)" >> $GITHUB_OUTPUT
    outputs:
      current_step: ${{ steps.get_step.outputs.current_step }}
```

**Parameters:**
- `branches`: Array of branch names to trigger on
- `permissions`: Required GitHub token permissions
- `current_step`: Output from step detection

### Content Management API

#### Step Content Structure
Each step file follows this markdown structure:

```markdown
<!--
  <<< Author notes: Step N >>>
  Description of what the learner will accomplish
-->

## Step N: Title

_Brief description of the step objective._

### :keyboard: Activity: Specific task description

1. Numbered instructions
2. With specific actions
3. And expected outcomes

**Expected result:** Description of what should happen

_Let's go to the next step._
```

## Usage Instructions

### For Course Administrators

#### Adding a New Step

1. **Create step content file:**
```bash
# Create new step file
touch .github/steps/N-step-name.md
```

2. **Create corresponding workflow:**
```bash
# Create workflow file
touch .github/workflows/N-step-name.yml
```

3. **Update step progression logic:**
```yaml
# In the new workflow file
if: ${{ steps.get_step.outputs.current_step == 'N-1' }}
```

#### Modifying Course Content

```bash
# Edit step content
vim .github/steps/N-step-name.md

# Test workflow locally (requires act)
act -j step-validation
```

### For Learners

#### Starting the Course

1. **Create repository from template:**
```bash
# Using GitHub CLI
gh repo create my-github-pages --template skills/github-pages --public

# Or use the web interface
# Visit: https://github.com/new?template_owner=skills&template_name=github-pages
```

2. **Follow step-by-step instructions:**
```bash
# Check current step
cat .github/steps/-step.txt

# Read current instructions
cat .github/steps/$(cat .github/steps/-step.txt)-*.md
```

#### Progressing Through Steps

The course automatically progresses when you complete each step:

1. **Step 0:** Read welcome message
2. **Step 1:** Enable GitHub Pages in repository settings
3. **Step 2:** Configure your site with `_config.yml`
4. **Step 3:** Customize your homepage (`index.md`)
5. **Step 4:** Create a blog post (`_posts/YYYY-MM-DD-title.md`)
6. **Step 5:** Merge your pull request

## Examples

### Example: Creating a Blog Post (Step 4)

**File Structure:**
```
_posts/
└── 2024-01-15-my-first-post.md
```

**Content Template:**
```markdown
---
title: "My First Blog Post"
date: 2024-01-15
---

# Welcome to my blog

This is my first post using GitHub Pages and Jekyll!

## What I learned

- How to create a GitHub Pages site
- How to write blog posts in Markdown
- How to use Jekyll for static site generation
```

### Example: Site Configuration

**File:** `_config.yml`
```yaml
title: My GitHub Pages Site
description: A site built during the GitHub Pages course
theme: minima
```

**File:** `index.md`
```markdown
---
title: Welcome to my site
---

# Hello World!

This is my GitHub Pages site. You can learn more about me and my projects here.

## Recent Posts

{% for post in site.posts %}
- [{{ post.title }}]({{ post.url }}) - {{ post.date | date: "%B %d, %Y" }}
{% endfor %}
```

## Error Handling

### Common Issues and Solutions

#### 1. Workflow Not Triggering
```yaml
# Ensure proper permissions in workflow
permissions:
  contents: write
  pull-requests: write
```

#### 2. Step Not Progressing
```bash
# Check current step file
cat .github/steps/-step.txt

# Verify step file exists
ls .github/steps/
```

#### 3. GitHub Pages Not Building
```yaml
# Verify _config.yml syntax
theme: minima
title: Your Site Title
```

## Security Considerations

- All workflows use `actions/checkout@v4` for security
- Limited permissions scope: `contents: write, pull-requests: write`
- No external dependencies beyond GitHub Actions marketplace actions

## Contributing

### Workflow Modification Guidelines

1. **Maintain backward compatibility** with existing step structure
2. **Test thoroughly** before merging changes
3. **Update documentation** for any API changes
4. **Follow GitHub Actions best practices**

### Content Guidelines

1. **Use clear, actionable language** in step instructions
2. **Include expected outcomes** for each action
3. **Provide troubleshooting information** for common issues
4. **Maintain consistent formatting** across all steps

## Support and Resources

- **Course Discussion Board:** [GitHub Skills Discussions](https://github.com/orgs/skills/discussions/categories/github-pages)
- **GitHub Status:** [GitHub Status Page](https://www.githubstatus.com/)
- **Jekyll Documentation:** [Jekyll Docs](https://jekyllrb.com/docs/)
- **GitHub Pages Documentation:** [GitHub Pages Docs](https://docs.github.com/en/pages)

---

*This documentation covers all public APIs, functions, and components in the GitHub Pages learning course repository. For additional support, please refer to the resources listed above.*