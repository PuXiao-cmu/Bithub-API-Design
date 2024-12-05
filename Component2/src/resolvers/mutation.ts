import { mockPullRequests, mockCommits, generateId } from "../dataStore";
import { PullRequestStatus, Commit } from "../types";

// Helper function to check for a common ancestor
function hasCommonAncestorOptimized(commit1: Commit | null, commit2: Commit | null): boolean {
  if (!commit1 || !commit2) return false;

  const ancestors1 = new Set(commit1.ancestors);
  for (const ancestor of commit2.ancestors) {
    if (ancestors1.has(ancestor)) {
      return true;
    }
  }
  return false;
}

export const mutationResolvers = {
  Mutation: {
    createPullRequest: (
      _: any,
      args: { description: string; sourceCommitId: string; branchTargetId: string }
    ) => {
      // Find sourceCommit and branchTarget in mockCommits
      const sourceCommit = mockCommits.find(commit => commit.id === args.sourceCommitId);
      const branchTarget = mockCommits.find(commit => commit.id === args.branchTargetId);

      if (!sourceCommit || !branchTarget) {
        throw new Error("Source commit or branch target not found");
      }
      if (!hasCommonAncestorOptimized(sourceCommit, branchTarget)) {
        throw new Error("Source commit and branch target have no common ancestor");
      }
      const newPR = {
        id: generateId(),
        description: args.description,
        sourceCommit: sourceCommit,
        branchTarget: branchTarget,
        status: PullRequestStatus.PENDING,
        comments: [],
      };
      if (sourceCommit.id.startsWith("0")) {
        newPR.status = PullRequestStatus.CONFLICT;
      }
      mockPullRequests.push(newPR);
      return newPR;
    },
    mergePullRequest: (_: any, args: { id: string }) => {
      const pr = mockPullRequests.find(pr => pr.id === args.id);
      if (!pr || pr.status !== PullRequestStatus.PENDING) {
        throw new Error("Cannot merge this PR");
      }
      pr.status = PullRequestStatus.MERGED;
      return pr;
    },
    rejectPullRequest: (_: any, args: { id: string }) => {
      const pr = mockPullRequests.find(pr => pr.id === args.id);
      if (!pr || pr.status === PullRequestStatus.MERGED || pr.status === PullRequestStatus.REJECTED) {
        throw new Error("Cannot reject this PR");
      }
      pr.status = PullRequestStatus.REJECTED;
      return pr;
    },
    addComment: (
      _: any,
      args: { prId: string; type: string; line?: number; content: string }
    ) => {
      const pr = mockPullRequests.find(pr => pr.id === args.prId);
      if (!pr) {
        throw new Error("Pull Request not found");
      }

      const newComment = {
        id: generateId(),
        type: args.type,
        line: args.line,
        content: args.content,
        reactions: [],
      };
      pr.comments.push(newComment);
      return newComment;
    },
    deleteComment: (_: any, args: { prId: string; commentId: string }) => {
      const pr = mockPullRequests.find(pr => pr.id === args.prId);
      if (!pr) {
        throw new Error("Pull Request not found");
      }
      pr.comments = pr.comments.filter(comment => comment.id !== args.commentId);
      return pr;
    },
    addReaction: (_: any, args: { commentId: string; type: string }) => {
      const comment = mockPullRequests.flatMap(pr => pr.comments).find(c => c.id === args.commentId);
      if (!comment) {
        throw new Error("Comment not found");
      }
      const reaction = comment.reactions.find(r => r.type === args.type);
      if (reaction) {
        reaction.count += 1;
      } else {
        comment.reactions.push({ id: generateId(), type: args.type, count: 1 });
      }
      return comment;
    },
    removeReaction: (_: any, args: { commentId: string; type: string }) => {
      const comment = mockPullRequests.flatMap(pr => pr.comments).find(c => c.id === args.commentId);
      if (!comment) {
        throw new Error("Comment not found");
      }

      const reaction = comment.reactions.find(r => r.type === args.type);
      if (!reaction) {
        throw new Error("Reaction not found");
      }

      if (reaction.count > 1) {
        reaction.count -= 1;
      } else {
        comment.reactions = comment.reactions.filter(r => r.type !== args.type);
      }

      return comment;
    },
  },
};
