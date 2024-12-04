export enum PullRequestStatus {
  PENDING = "pending",
  CONFLICT = "conflict",
  MERGED = "merged",
  REJECTED = "rejected",
}

export interface PullRequest {
  id: string;
  description: string;
  sourceCommit: Commit;
  branchTarget: Commit;
  status: PullRequestStatus;
  comments: Comment[];
  changedFiles: string[];
}

export interface Commit {
  id: string;
  message: string;
  ancestors: string[];
}

export interface Comment {
  id: string;
  type: string;
  line?: number;
  content: string;
  reactions: Reaction[];
}

export interface Reaction {
  id: string;
  type: string;
  count: number;
}
  