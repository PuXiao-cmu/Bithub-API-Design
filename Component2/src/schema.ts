import { gql } from "apollo-server";

export const typeDefs = gql`
  enum PullRequestStatus {
    PENDING
    MERGED
    REJECTED
    CONFLICT
  }

  type PullRequest {
    id: ID!
    description: String!
    sourceCommit: Commit!
    branchTarget: Commit!
    status: PullRequestStatus!
    comments: [Comment!]!
    changedFiles: [String!]!
  }

  type Commit {
    id: ID!
    message: String!
    ancestors: [ID!]!
  }

  type Comment {
    id: ID!
    type: String!
    line: Int
    content: String!
    reactions: [Reaction!]!
  }

  type Reaction {
    id: ID!
    type: String!
    count: Int!
  }

  type Query {
    pullRequests(status: PullRequestStatus, page: Int, limit: Int): [PullRequest!]!
    pullRequest(id: ID!): PullRequest
  }

  type Mutation {
    createPullRequest(
      description: String!
      sourceCommitId: String!
      branchTargetId: String!
    ): PullRequest
    mergePullRequest(id: ID!): PullRequest
    rejectPullRequest(id: ID!): PullRequest
    addComment(prId: ID!, type: String!, line: Int, content: String!): Comment
    deleteComment(prId: ID!, commentId: ID!): PullRequest
    addReaction(commentId: ID!, type: String!): Comment
    removeReaction(commentId: ID!, type: String!): Comment
  }
`;
