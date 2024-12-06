# Component 2: Integration for Third-Party Tools

## Overview

**Component 2** focuses on enabling native integration of code review tools with the platform. This component provides a seamless way for developers to interact with pull requests (PRs) and their associated metadata, files, and comments.

The implementation includes:

- Displaying PR metadata, such as status, description, and associated commits.
- Displaying a list of PRs, filtering them by status, with some notion of pagination.
- Showing a list of changed files and their inline changes.
- Supporting comments (general and inline) with reactions.
- Supporting merging a pending PR or reject a pending PR or a PR causing a merge conflict.
- Providing GraphQL APIs for querying and mutating PR data.

------

## Features

### 1. Pull Request Metadata

When a PR is viewed, its metadata is displayed, including:

- PR description
- Source commit
- Target commit
- PR status (e.g., PENDING, MERGED, REJECTED, or CONFLICT)

### 2. Changed Files and Inline Comments

- PRs include a list of changed files with detailed line-level changes.
- Developers can add inline comments to specific lines in a file.
- Each inline comment supports reactions like 👍 (`+1`) and ❤️.

### 3. General Comments

- Developers can add general comments to a PR that are not tied to a specific file or line.
- Reactions can also be added to general comments.

### 4. Merge and Reject Pull Requests

- Support for merging a **pending PR**.
- Support for rejecting:
  - A **pending PR**.
  - A PR that is causing a **merge conflict**.

------

## API Design

GraphQL was chosen because it aligns perfectly with the requirements for integrating third-party tools, particularly for a code review system.

### UML Class Diagram

![img](https://lh7-rt.googleusercontent.com/docsz/AD_4nXfk-GJMc1jwcYPvWx482-qBf5kHyGFwBD2aOum18b3BjVS5ofXpjsYHNnV_Wf9JOs3OJsPMLEWgIXPQdVCSitZuwsBpppemGA8eXRgjTepcOXo_3hjujJJ38G2h8VXyaXcwBflbYQ?key=zsE13pF0u-pKyMtg6HUMGxjt)

### Queries Supported by the API

| **Query Name** | **Description**                                              | **Inputs**                                                   | **Outputs**                                                  |
| -------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| pullRequests   | Fetches a list of pull requests with optional filters and pagination. | - status (PullRequestStatus, optional): Filter by pull request status.- page (Int, optional): Page number for pagination.- limit (Int, optional): Number of results per page. | [PullRequest]: List of pull requests.                        |
| pullRequest    | Fetches details of a single pull request by its ID.          | - id (String, required): The ID of the pull request.         | PullRequest: Pull request object with all details, including PR metadata, a list of changed files, and providing anability to see changed lines in these files, with their inline comments. |

### Mutations Supported by the API

| **Mutation Name** | **Description**                                       | **Inputs**                                                   | **Outputs**                                                  |
| ----------------- | ----------------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| createPullRequest | Creates a new pull request.                           | - description (String, required): Description of the pull request.- sourceCommitId (String, required): ID of the source commit.- branchTargetId (String, required): ID of the target branch commit. | PullRequest: Newly created pull request object.              |
| mergePullRequest  | Merges a pull request in PENDING status.              | - id (String, required): ID of the pull request.             | PullRequest: Updated pull request with MERGED status.        |
| rejectPullRequest | Rejects a pull request in PENDING or CONFLICT status. | - id (String, required): ID of the pull request.             | PullRequest: Updated pull request with REJECTED status.      |
| addComment        | Adds a comment to a pull request.                     | - prId (String, required): ID of the pull request.- type (String, required): Type of comment (general or inline).- file (String, optional): Changed file name for inline comments.- line (Int, optional): Line number for inline comments.- content (String, required): Content of the comment. | Comment: Newly added comment object.                         |
| deleteComment     | Deletes a comment from a pull request.                | - prId (String, required): ID of the pull request.- commentId (String, required): ID of the comment to delete. | PullRequest: Updated pull request without the deleted comment. |
| addReaction       | Adds a reaction to a comment.                         | - commentId (String, required): ID of the comment.- type (String, required): Type of reaction (e.g., +1, ❤️). | Comment: Updated comment object with new reaction.           |
| removeReaction    | Removes a reaction from a comment.                    | - commentId (String, required): ID of the comment.- type (String, required): Type of reaction to remove. | Comment: Updated comment object with reaction removed.       |

------

## How to Compile and Run

### Prerequisites

1. **Node.js**: Install [Node.js](https://nodejs.org/) (v16 or higher recommended).
2. **npm**: Ensure `npm` is installed alongside Node.js.

### Steps to Compile and Run

1. Clone the repository:

   ```
   git clone <repository_url>
   cd <repository_directory>
   ```

2. Install dependencies:

   ```
   npm install
   ```

3. Start the server:

   ```
   npm start
   ```

4. The server will run at:

   ```
   http://localhost:4000
   ```

------

## Testing the Application

### Using Apollo Studio

1. Open Apollo Studio.

2. Set the endpoint to:

   ```
   http://localhost:4000
   ```

3. Use the provided queries and mutations below to test the API.

------

## Example Queries and Mutations

### Query: Fetch All Pull Requests

```
query {
  pullRequests {
    id
    description
    status
    comments {
      id
      content
    }
  }
}
```

### Query: Fetch a Single Pull Request

```
query {
  pullRequest(id: "1") {
    id
    description
    sourceCommit {
      id
      message
    }
    branchTarget {
      id
      message
    }
    changedFiles {
      fileName
      changedLines {
        lineNumber
        content
        inlineComments {
          id
          content
          reactions {
            type
            count
          }
        }
      }
    }
  }
}
```

### **Mutation: Create a Pull Request**

```
mutation {
  createPullRequest(
    description: "New Feature PR"
    sourceCommitId: "3"
    branchTargetId: "2"
  ) {
    id
    description
    status
  }
}
```

### **Mutation: Merge a pending PR**

```
mutation {
  mergePullRequest(id: "2") {
    id
    status
  }
}
```

### **Mutation: Reject a pending PR or a PR causing a merge conflict**

```
mutation {
  rejectPullRequest(id: "2") {
    id
    status
  }
}
```

### Mutation: Add a General Comment

```
mutation {
  addComment(
    prId: "1"
    type: "general"
    content: "This is a general comment."
  ) {
    id
    type
    content
  }
}
```

### Mutation: Add an Inline Comment

```
mutation {
  addComment(
    prId: "1"
    type: "inline"
    file: "feature1.js"
    line: 10
    content: "Consider renaming this function."
  ) {
    id
    type
    file
    line
    content
  }
}
```

### **Mutation: Delete a General Comment**

```
mutation {
  deleteComment(prId: "1", commentId: "c1") {
    id
    comments {
      id
      content
    }
  }
}
```

### Mutation: Add a Reaction to a Comment

```
mutation {
  addReaction(commentId: "c1", type: "+1") {
    id
    reactions {
      type
      count
    }
  }
}
```

### Mutation: Remove a Reaction from a Comment

```
mutation {
  removeReaction(commentId: "c1", type: "+1") {
    id
    reactions {
      type
      count
    }
  }
}
```

------

## Example Data

Here is an example of a fully populated PR for testing:

```json
{
  "id": "1",
  "description": "Merge feature branch into main",
  "sourceCommit": {
    "id": "3",
    "message": "Feature branch commit",
    "changedFiles": [
      {
        "fileName": "feature1.js",
        "changedLines": [
          {
            "lineNumber": 10,
            "content": "const feature = () => {};",
            "inlineComments": [
              {
                "id": "ic1",
                "type": "inline",
                "file": "feature1.js",
                "line": 10,
                "content": "Consider renaming this function.",
                "reactions": [
                  { "type": "+1", "count": 3 },
                  { "type": "❤️", "count": 2 }
                ]
              }
            ]
          }
        ]
      }
    ]
  },
  "branchTarget": {
    "id": "2",
    "message": "Second commit"
  },
  "status": "PENDING",
  "comments": [
    {
      "id": "c1",
      "type": "general",
      "content": "Overall, this looks great!",
      "reactions": [
        { "type": "+1", "count": 5 },
        { "type": "❤️", "count": 3 }
      ]
    }
  ]
}
```