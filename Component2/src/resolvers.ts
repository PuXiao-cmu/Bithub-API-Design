import { getPullRequests, getPullRequestById, addPullRequest } from "./dataStore";
import { Status } from "./models";

export const resolvers = {
  Query: {
    pullRequests: (_: any, args: { status?: string }) =>
      getPullRequests(args.status as Status | undefined),
    pullRequest: (_: any, args: { id: number }) =>
      getPullRequestById(args.id),
  },
  Mutation: {
    createPullRequest: (
      _: any,
      args: { description: string; sourceCommit: string; branchTarget: string }
    ) => addPullRequest(args.description, args.sourceCommit, args.branchTarget),
  },
};
