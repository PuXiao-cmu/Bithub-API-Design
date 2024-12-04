export interface PullRequest {
    id: string;
    description: string;
    sourceCommit: string;
    branchTarget: string;
    status: string;
    comments: Comment[];
    changedFiles: string[];
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
  