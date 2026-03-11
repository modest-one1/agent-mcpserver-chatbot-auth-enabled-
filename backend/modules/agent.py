from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import AzureChatOpenAI
from langchain.agents import create_agent
from modules.config import Config

async def build_agent(access_token=None):
    client_config = {
        "email_server": {
            "url": Config.EMAIL_SERVER_URL,
            "transport": Config.EMAIL_TRANSPORT,
        },
        "math_server": {
            "url": Config.MATH_SERVER_URL,
            "transport": Config.MATH_TRANSPORT,
        }

    }
    if access_token:
        client_config["email_server"]["headers"] = {"Authorization": f"Bearer {access_token}"}
        client_config["math_server"]["headers"] = {"Authorization": f"Bearer {access_token}"}
    client = MultiServerMCPClient(client_config)
    tools = await client.get_tools()
    print("Azure OpenAI Endpoint:", Config.AZURE_OPENAI_ENDPOINT)
    print("Azure OpenAI Deployment:", Config.AZURE_OPENAI_DEPLOYMENT)
    print("Azure OpenAI API Version:", Config.AZURE_OPENAI_API_VERSION)
    model = AzureChatOpenAI(
        azure_endpoint=Config.AZURE_OPENAI_ENDPOINT,
        api_version=Config.AZURE_OPENAI_API_VERSION,
        name=Config.AZURE_OPENAI_DEPLOYMENT,
        top_p=1,
        max_tokens=100
    )
    print("Creating agent with tools:", [tool.name for tool in tools])

    agent = create_agent(model, tools)
    return agent, tools
