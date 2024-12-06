import { Commit, Comment, PullRequest, PullRequestStatus } from "./types";

export const mockComments: Comment[] = [
  {
    id: "c1",
    type: "general",
    content: "Looks good to me!",
    reactions: [
      { id: "r1", type: "+1", count: 3 },
      { id: "r2", type: "❤️", count: 1 },
    ],
  },
  {
    id: "c2",
    type: "inline",
    file: "feature1.js",
    line: 10,
    content: "This is an inline comment.",
    reactions: [{ id: "ir1", type: "❤️", count: 2 }],
  },
  {
    id: "c3",
    type: "general",
    content: "This feature is not ready for production.",
    reactions: [{ id: "r3", type: "👎", count: 2 }],
  },
];

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
          { lineNumber: 10, content: "const feature = () => {};", inlineComments: [mockComments[1],] },
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
          { lineNumber: 15, content: "if (bugFixed) return true;", 
            inlineComments: [
              {
                id: "ic1",
                type: "inline",
                line: 10,
                content: "Consider renaming this function.",
                reactions: [
                  { id: "r1", type: "+1", count: 3 },
                ],
              },
            ],
          },
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
  {
    id: "6",
    message: "New commit",
    ancestors: ["1", "2", "4"],
    changedFiles: [
      {
        fileName: "newFile.js",
        changedLines: [
          { lineNumber: 35, content: "return newContent;" },
        ],
      },
    ],
  },
  {
    id: "7",
    message: "New commit with a new ancestor",
    ancestors: ["999"],
    changedFiles: [
      {
        fileName: "newFile.js",
        changedLines: [
          { lineNumber: 35, content: "return newContent;" },
        ],
      },
    ],
  },
  {
    id: "007",
    message: "New commit start with 0",
    ancestors: ["1", "2", "4"],
    changedFiles: [
      {
        fileName: "newFile.js",
        changedLines: [
          { lineNumber: 35, content: "return newContent;" },
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
    comments: [ mockComments[0], ],
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
    sourceCommit: mockCommits[4],
    branchTarget: mockCommits[1],
    status: PullRequestStatus.REJECTED,
    comments: [ mockComments[2], ],
  },
];

export const generateId = (): string => Math.random().toString(36).substring(7);
