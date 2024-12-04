import { mockPullRequests } from "../dataStore";

export const queryResolvers = {
  Query: {
    pullRequests: (_: any, args: { status?: string; page?: number; limit?: number }) => {
      let filtered = mockPullRequests;
      if (args.status) {
        filtered = filtered.filter(pr => pr.status === args.status);
      }
      const start = ((args.page || 1) - 1) * (args.limit || 10);
      return filtered.slice(start, start + (args.limit || 10));
    },
    pullRequest: (_: any, args: { id: string }) => {
      return mockPullRequests.find(pr => pr.id === args.id);
    },
  },
};
