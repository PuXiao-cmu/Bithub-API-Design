import { PullRequest, Comment } from "./types";

export const mockPullRequests: PullRequest[] = [
  {
    id: "1",
    description: "Initial PR",
    sourceCommit: "123abc",
    branchTarget: "main",
    status: "pending",
    comments: [],
    changedFiles: ["file1.js", "file2.js"],
  },
  {
    id: "2",
    description: "Another PR",
    sourceCommit: "456def",
    branchTarget: "develop",
    status: "merge conflict",
    comments: [
      {
        id: "c1",
        type: "general",
        content: "This is a general comment",
        reactions: [
          { id: "r1", type: "+1", count: 2 },
        ],
      },
    ],
    changedFiles: ["file3.js"],
  },
];

export const generateId = (): string => Math.random().toString(36).substring(7);
