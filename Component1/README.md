## Overview

I implemented Component 1 with **RESTful API** in **Python** and **Flask**.

## API Design Table

| **Capability**                    | **HTTP Verb** | **Endpoint**                                              | **Input**                                               | **Output and Response Codes**                                                                                      |
|------------------------------------|---------------|----------------------------------------------------------|---------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------|
| **1. Get repository default view**| GET           | `/repositories/{id}`                                      | `{id}` (repository ID)                                  | `302 Found`: Redirects to `/repositories/{id}/branches/main/commits/latest`. <br> `404 Not Found`: Repository not found. |
| **2. List all branches**          | GET           | `/repositories/{id}/branches`                            | `{id}`                                                  | `200 OK`: Returns a list of branches. <br> `404 Not Found`: Repository not found.                                  |
| **3. List all tags**              | GET           | `/repositories/{id}/tags`                                | `{id}`                                                  | `200 OK`: Returns a list of tags. <br> `404 Not Found`: Repository not found.                                      |
| **4. List all commits in a branch**| GET          | `/repositories/{id}/branches/{branch}/commits`           | `{id}, {branch}`                                        | `200 OK`: Returns a list of commits. <br> `404 Not Found`: Repository or branch not found.                         |
| **5. Get top-level tree in a commit**| GET        | `/repositories/{id}/branches/{branch}/commits/{hash}/tree`| `{id}, {branch}, {hash}`                                | `200 OK`: Returns the directory tree structure. <br> `404 Not Found`: Repository, branch, or commit not found.     |
| **6. View file or sub-tree**      | GET           | `/repositories/{id}/branches/{branch}/commits/{hash}/tree/{path}`| `{id}, {branch}, {hash}, {path}`                       | `200 OK`: Returns file content or directory structure. <br> `404 Not Found`: File or directory not found.          |
| **7. List repository issues**     | GET           | `/repositories/{id}/issues`                              | `{id} (required), {status}, {page}, {size} (optional)`  | `200 OK`: Returns a list of issues with status and submitter ID. <br> `404 Not Found`: Repository not found.       |
| **8. View a specific issue details**| GET         | `/repositories/{id}/issues/{issue_id}`                   | `{id}, {issue_id}`                                      | `200 OK`: Returns issue details and one page of comments. <br> `404 Not Found`: Repository or issue not found.     |
| **9. Report a new issue**         | POST          | `/repositories/{id}/issues`                              | `{id}, {description}, {submitterId}`                   | `201 Created`: Issue created successfully. <br> `400 Bad Request`: Invalid input. <br> `404 Not Found`: Repository not found. |
| **10. Paginate comments for an issue**| GET       | `/repositories/{id}/issues/{issue_id}/comments`          | `{id}, {issue_id}, {page}, {size}`                      | `200 OK`: Returns a paginated list of comments. <br> `400 Bad Request`: Invalid input. <br> `404 Not Found`: Repository or issue not found. |
| **11. Submit a new comment**      | POST          | `/repositories/{id}/issues/{issue_id}/comments`          | `{id}, {issue_id}, {comment}`                           | `201 Created`: Comment added successfully. <br> `400 Bad Request`: Invalid input. <br> `404 Not Found`: Repository or issue not found. |

---

## Testing

For each API functionality, I implemented **unit tests** using `pytest`. Each test includes a **happy path test** and an **error test**.

All tests have successfully passed, as shown below:
![test](https://github.com/user-attachments/assets/c55d5cd6-835e-45a2-a16c-9b154f5dc0ac)
