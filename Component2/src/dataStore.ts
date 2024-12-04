import { Commit, PullRequest } from "./types";

// Mock commits with ancestors
export const mockCommits: Commit[] = [
  { id: "1", message: "Initial commit", ancestors: [] },
  { id: "2", message: "Second commit", ancestors: ["1"] },
  { id: "3", message: "Feature branch commit", ancestors: ["1", "2"] },
  { id: "4", message: "Hotfix branch commit", ancestors: ["1", "2"] },
  { id: "5", message: "Bugfix commit on feature branch", ancestors: ["1", "2", "3"] },
  { id: "6", message: "Another feature branch commit", ancestors: ["1", "2", "3"] },
  { id: "7", message: "Experimental branch commit", ancestors: ["1", "2"] },
  { id: "8", message: "Main branch commit after feature merge", ancestors: ["1", "2", "3"] },
  { id: "9", message: "Main branch commit after hotfix merge", ancestors: ["1", "2", "4"] },
];

// Mock pull requests
export const mockPullRequests: PullRequest[] = [
  {
    id: "1",
    description: "Merge feature branch into main",
    sourceCommit: mockCommits[2], // Commit ID "3"
    branchTarget: mockCommits[1], // Commit ID "2"
    status: "merged",
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
    changedFiles: ["feature1.js", "feature2.js"],
  },
  {
    id: "2",
    description: "Hotfix: Patch critical bug in production",
    sourceCommit: mockCommits[3], // Commit ID "4"
    branchTarget: mockCommits[1], // Commit ID "2"
    status: "pending",
    comments: [],
    changedFiles: ["hotfix.js"],
  },
  {
    id: "3",
    description: "Experimental branch: Add new prototype features",
    sourceCommit: mockCommits[6], // Commit ID "7"
    branchTarget: mockCommits[1], // Commit ID "2"
    status: "rejected",
    comments: [
      {
        id: "c2",
        type: "general",
        content: "This feature is not ready for production.",
        reactions: [{ id: "r3", type: "👎", count: 2 }],
      },
    ],
    changedFiles: ["experiment1.js", "experiment2.js"],
  },
  {
    id: "4",
    description: "Bugfix on feature branch",
    sourceCommit: mockCommits[4], // Commit ID "5"
    branchTarget: mockCommits[2], // Commit ID "3"
    status: "pending",
    comments: [],
    changedFiles: ["bugfix.js"],
  },
];

// Helper function to generate unique IDs
export const generateId = (): string => Math.random().toString(36).substring(7);
