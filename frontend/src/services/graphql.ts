// src/services/graphql.ts
export interface GraphQLErrorPayload {
  message: string;
  extensions?: {
    code?: string;
    [key: string]: unknown;
  };
}

export class GraphQLRequestError extends Error {
  public code?: string;
  public rawErrors: GraphQLErrorPayload[];

  constructor(message: string, errors: GraphQLErrorPayload[]) {
    super(message);
    this.rawErrors = errors;
    this.code = errors[0]?.extensions?.code;
  }
}

const GRAPHQL_URL =
  import.meta.env.VITE_GRAPHQL_URL || "/graphql"; // e.g. "http://localhost:8000/graphql"

export async function fetchGraphQL<T>(
  query: string,
  variables?: Record<string, unknown>
): Promise<T> {
  const res = await fetch(GRAPHQL_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query, variables }),
  });

  const json = await res.json();

  if (json.errors?.length) {
    const errors: GraphQLErrorPayload[] = json.errors;
    const first = errors[0];
    throw new GraphQLRequestError(first.message || "GraphQL error", errors);
  }

  return json.data as T;
}