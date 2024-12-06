export enum PullRequestStatus {
  PENDING = "PENDING",
  CONFLICT = "CONFLICT",
  MERGED = "MERGED",
  REJECTED = "REJECTED",
}

export interface PullRequest {
  id: string;
  description: string;
  sourceCommit: Commit;
  branchTarget: Commit;
  status: PullRequestStatus;
  comments: Comment[];
}

export interface Commit {
  id: string;
  message: string;
  ancestors: string[];
  changedFiles: FileChange[];
}

export interface Comment {
  id: string;
  type: string;
  file?: string;
  line?: number;
  content: string;
  reactions: Reaction[];
}

export interface Reaction {
  id: string;
  type: string;
  count: number;
}

export interface FileChange {
  fileName: string;
  changedLines: ChangedLine[];
}

export interface ChangedLine {
  lineNumber: number;
  content: string;
  inlineComments?: Comment[];
}
  