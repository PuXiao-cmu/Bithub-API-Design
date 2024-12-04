export enum Status {
    PENDING = "Pending",
    MERGED = "Merged",
    REJECTED = "Rejected",
    CONFLICT = "Conflict",
  }
  
  export interface User {
    id: number;
    name: string;
  }
  
  export interface Comment {
    id: number;
    text: string;
    userId: number;
    inline: boolean;
    reactions: string[];
  }
  
  export interface PullRequest {
    id: number;
    description: string;
    sourceCommit: string;
    branchTarget: string;
    status: Status;
    comments: Comment[];
  }
  