# Bithub API Design Project

## Overview

This repository contains the implementation of three independent API components for **Bithub**, a code-hosting platform. The project explores and implements different API paradigms (REST, GraphQL, gRPC) to address various use cases, ensuring efficient, extensible, and user-friendly designs.

### Components

1. **Basic Website Display API (REST)**: Allows viewing repositories, commits, branches, tags, and repository issues.
2. **Third-Party Integration API (GraphQL)**: Supports a robust pull request system, including comments, reactions, and merge functionalities.
3. **AI Assistant API (gRPC)**: Provides intelligent features such as generating pull request descriptions, code completions, and conversational debugging.

---

## Features and Use Cases

### 1. Basic Website Display API (REST)

- **Repository Viewer**:
  - Retrieve repository details, list branches, tags, and commits.
  - Display file structure and content at any commit.
- **Issue Browser**:
  - List, filter, and paginate issues.
  - View issue details and comments.
  - Submit new issues and comments.

### 2. Third-Party Integration API (GraphQL)

- **Pull Request Management**:
  - Create, merge, and reject pull requests.
  - Add, delete, and react to comments (inline or general).
  - List pull requests with filters and pagination.
- **Comment Reactions**:
  - Add or remove reactions to comments.
  - Supports multiple reaction types, ensuring user interaction.

### 3. AI Assistant API (gRPC)

- **Features**:
  - Generate draft pull request descriptions.
  - Provide smart code completions based on context.
  - Act as a conversational assistant for debugging and pair programming.

---

## Technology Stack

- **Programming Languages**: TypeScript, Python
- **API Frameworks**: Express (REST), Apollo GraphQL, gRPC
- **Testing Tools**: Jest, Postman, gRPC Python libraries
- **Version Control**: Git, GitHub Classroom

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/bithub-api-design.git
   cd bithub-api-design
2. Navigate to the desired component folder:
- **Component 1/**: RESTful API  
- **Component 2/**: GraphQL  
- **Component 3/**: gRPC  
