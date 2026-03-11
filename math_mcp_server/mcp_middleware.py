from fastmcp.server.middleware import Middleware, MiddlewareContext
import jwt  # pyjwt
from mcp.types import CallToolRequestParams, ListToolsRequest
from fastmcp.tools.tool import Tool, ToolResult

# Role -> allowed tool names
ROLE_USER_ALLOWLIST = {
    "Mcp.Reader": {"alice", "bob"}
}


class ListingFilterMiddleware(Middleware):
    def _extract_roles(self, context: MiddlewareContext) -> set[str]:
        roles: set[str] = set()

        try:
            req = context.fastmcp_context.request_context.request if context.fastmcp_context else None
            headers = getattr(req, "_headers", None)
            if not headers:
                return roles

            auth_header = headers.get("authorization") or headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return roles

            token = auth_header.split(" ", 1)[1].strip()
            claims = jwt.decode(token, options={"verify_signature": False}) or {}

            claim_val = claims.get("roles") or claims.get("role")
            if isinstance(claim_val, (list, tuple, set)):
                roles.update(str(r) for r in claim_val)
            elif isinstance(claim_val, str):
                roles.add(claim_val)
        except Exception:
            # On parse failures, default deny by returning no roles.
            return set()

        return roles

    def _allowed_tools_for_roles(self, roles: set[str]) -> set[str]:
        allowed_tools: set[str] = set()
        for role in roles:
            allowed_tools.update(ROLE_USER_ALLOWLIST.get(role, set()))
        return allowed_tools

    async def on_list_tools(
        self,
        context: MiddlewareContext[ListToolsRequest],
        call_next,
    ):
        tools = await call_next(context)

        roles = self._extract_roles(context)
        print(f"Extracted roles from token: {roles}")

        # Collect allowed tools from all roles in token.
        allowed_tools = self._allowed_tools_for_roles(roles)

        # No matching role => no tools.
        if not allowed_tools:
            return []

        # Return only tools explicitly allowed for the role(s).
        filtered: list[Tool] = []
        for t in tools:
            tool_name = getattr(t, "name", None) or getattr(t, "__name__", None)
            if tool_name in allowed_tools:
                filtered.append(t)

        return filtered

    async def on_call_tool(
        self,
        context: MiddlewareContext[CallToolRequestParams],
        call_next,
    ) -> ToolResult:
        roles = self._extract_roles(context)
        allowed_tools = self._allowed_tools_for_roles(roles)

        # Enforce allowlist at execution time so direct calls are also blocked.
        if context.message.name not in allowed_tools:
            raise PermissionError(
                f"Tool '{context.message.name}' is not allowed for roles: {sorted(roles)}"
            )

        return await call_next(context)