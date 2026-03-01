---
name: edge-function
description: Scaffold a new Supabase Edge Function with auth, CORS, Zod validation, and error handling following 120 Ventures conventions
argument-hint: [function-name]
---

# Create Supabase Edge Function

Generate a new Supabase Edge Function named `$ARGUMENTS` following the project's security rules and architecture.

## Steps

1. **Create the function file** at `supabase/functions/$ARGUMENTS/index.ts`
2. **Follow this exact template structure:**

```typescript
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { z } from "https://deno.land/x/zod/mod.ts";

const corsHeaders = {
  "Access-Control-Allow-Origin": Deno.env.get("ALLOWED_ORIGIN") ?? "",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Access-Control-Allow-Headers": "authorization, content-type, x-client-info, apikey",
};

// Define input schema with Zod
const RequestSchema = z.object({
  // TODO: define fields based on function purpose
});

Deno.serve(async (req) => {
  // Handle CORS preflight
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders });
  }

  try {
    // 1. Authenticate
    const authHeader = req.headers.get("Authorization");
    if (!authHeader) {
      return new Response(
        JSON.stringify({ error: "Missing authorization" }),
        { status: 401, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    // 2. Init Supabase client
    const supabase = createClient(
      Deno.env.get("SUPABASE_URL")!,
      Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!
    );

    // 3. Verify user
    const token = authHeader.replace("Bearer ", "");
    const { data: { user }, error: authError } = await supabase.auth.getUser(token);
    if (authError || !user) {
      return new Response(
        JSON.stringify({ error: "Unauthorized" }),
        { status: 401, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    // 4. Validate input
    const body = await req.json();
    const parsed = RequestSchema.safeParse(body);
    if (!parsed.success) {
      return new Response(
        JSON.stringify({ error: "Invalid input", details: parsed.error.flatten() }),
        { status: 400, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    // 5. Business logic
    // TODO: implement

    // 6. Return response
    return new Response(
      JSON.stringify({ success: true }),
      { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  } catch (error) {
    console.error(`[${new Date().toISOString()}] $ARGUMENTS error:`, error);
    return new Response(
      JSON.stringify({ error: "Internal server error" }),
      { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  }
});
```

## Rules (from SECURITY_RULES.md)

- **One function = one atomic operation** — never combine multiple actions
- **Always authenticate** — verify JWT before any DB operation
- **Validate all input** with Zod — never trust client data
- **Never leak internals** — generic error messages to client, details only in console.error
- **CORS restricted** — use ALLOWED_ORIGIN env var, never `*`
- **No direct DB access patterns** — use service_role only server-side
- **Parameterized queries only** — no string concatenation for SQL

## After scaffolding

- Add the Zod schema fields based on the function's purpose
- Implement the business logic in section 5
- Add the function name to the deploy workflow if needed
- Test locally with `supabase functions serve $ARGUMENTS`
