import { Commit, PullRequest, PullRequestStatus } from "./types";

export const mockCommits: Commit[] = [
  {
    id: "1",
    message: "Initial commit",
    ancestors: [],
    changedFiles: [],
  },
  {
    id: "2",
    message: "Second commit",
    ancestors: ["1"],
    changedFiles: [],
  },
  {
    id: "3",
    message: "Feature branch commit",
    ancestors: ["1", "2"],
    changedFiles: [
      {
        fileName: "feature1.js",
        changedLines: [
          { lineNumber: 10, content: "const feature = () => {};" },
          { lineNumber: 20, content: "return feature;" },
        ],
      },
      {
        fileName: "feature2.js",
        changedLines: [
          { lineNumber: 5, content: "let unusedVar = true;" },
        ],
      },
    ],
  },
  {
    id: "4",
    message: "Hotfix branch commit",
    ancestors: ["1", "2"],
    changedFiles: [
      {
        fileName: "hotfix.js",
        changedLines: [
          { lineNumber: 15, content: "if (bugFixed) return true;" },
        ],
      },
    ],
  },
  {
    id: "5",
    message: "Bugfix commit on feature branch",
    ancestors: ["1", "2", "3"],
    changedFiles: [
      {
        fileName: "bugfix.js",
        changedLines: [
          { lineNumber: 25, content: "fixBug();" },
        ],
      },
    ],
  },
];

export const mockPullRequests: PullRequest[] = [
  {
    id: "1",
    description: "Merge feature branch into main",
    sourceCommit: mockCommits[2],
    branchTarget: mockCommits[1],
    status: PullRequestStatus.MERGED,
    comments: [
      {
        id: "c1",
        type: "general",
        content: "Looks good to me!",
        reactions: [
          { id: "r1", type: "+1", count: 3 },
          { id: "r2", type: "❤️", count: 1 },
        ],
      },
    ],
  },
  {
    id: "2",
    description: "Hotfix: Patch critical bug in production",
    sourceCommit: mockCommits[3],
    branchTarget: mockCommits[1],
    status: PullRequestStatus.PENDING,
    comments: [],
  },
  {
    id: "3",
    description: "Experimental branch: Add new prototype features",
    sourceCommit: mockCommits[6],
    branchTarget: mockCommits[1],
    status: PullRequestStatus.REJECTED,
    comments: [
      {
        id: "c2",
        type: "general",
        content: "This feature is not ready for production.",
        reactions: [{ id: "r3", type: "👎", count: 2 }],
      },
    ],
  },
];

export const generateId = (): string => Math.random().toString(36).substring(7);
