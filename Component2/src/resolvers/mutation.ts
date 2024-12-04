import { mockPullRequests, generateId } from "../dataStore";

export const mutationResolvers = {
  Mutation: {
    createPullRequest: (
      _: any,
      args: { description: string; sourceCommit: string; branchTarget: string }
    ) => {
      if (!args.sourceCommit || args.sourceCommit.startsWith("0")) {
        throw new Error("Merge conflict: invalid sourceCommit");
      }
      const newPR = {
        id: generateId(),
        description: args.description,
        sourceCommit: args.sourceCommit,
        branchTarget: args.branchTarget,
        status: "pending",
        comments: [],
        changedFiles: [],
      };
      mockPullRequests.push(newPR);
      return newPR;
    },
    mergePullRequest: (_: any, args: { id: string }) => {
      const pr = mockPullRequests.find(pr => pr.id === args.id);
      if (!pr || pr.status === "merge conflict") {
        throw new Error("Cannot merge this PR");
      }
      pr.status = "merged";
      return pr;
    },
    rejectPullRequest: (_: any, args: { id: string }) => {
      const pr = mockPullRequests.find(pr => pr.id === args.id);
      if (!pr) {
        throw new Error("Pull Request not found");
      }
      pr.status = "rejected";
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
      comment.reactions = comment.reactions.filter(r => r.type !== args.type);
      return comment;
    },
  },
};
