try:
    from fastmcp import FastMCP
except ImportError:
    from mcp.server.fastmcp import FastMCP
import httpx
import os
import json
import logging
from typing import Optional, Dict, Any, List
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route, Mount

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Swaggertesr")

mcp = FastMCP("Swaggertesr")
BASE_URL = "https://petstore.swagger.io/v2"

AUTH_HEADERS = { "api_key": os.environ.get("API_KEY", "") }

async def make_request(method: str, path: str, query_params: Optional[Dict] = None, body: Any = None, content_type: str = "application/json", extra_headers: Optional[Dict] = None):
    url = f"{BASE_URL}{path}"
    headers = AUTH_HEADERS.copy()
    if extra_headers:
        headers.update(extra_headers)

    logger.info(f"Making {method} request to {url}")

    async with httpx.AsyncClient(timeout=30.0) as client:
        kwargs = {"headers": headers, "params": query_params}

        if body and method.upper() not in ["GET", "DELETE"]:
            if content_type == "multipart/form-data":
                kwargs["data"] = body
            else:
                kwargs["json"] = body

        try:
            response = await client.request(method, url, **kwargs)
            response.raise_for_status()

            try:
                return response.json()
            except:
                return response.text
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error: {e.response.status_code} - {e.response.text}")
            return {"error": f"API returned {e.response.status_code}", "details": e.response.text}
        except Exception as e:
            logger.error(f"Request failed: {str(e)}")
            return {"error": str(e)}


@mcp.tool(name="uploadFile")
async def uploadFile(petId: int, additionalMetadata: Optional[str] = None, file: Optional[str] = None):
    "uploads an image"
    return await make_request(
        "POST",
        f"/pet/{petId}/uploadImage",
        query_params=None,
        body={ "additionalMetadata": additionalMetadata, "file": file },
        content_type="multipart/form-data",
        extra_headers={}
    )

@mcp.tool(name="addPet")
async def addPet(id: Optional[int] = None, category: Optional[Dict[str, Any]] = None, name: Optional[str] = None, photoUrls: Optional[List[Any]] = None, tags: Optional[List[Any]] = None, status: Optional[str] = None):
    "Add a new pet to the store"
    return await make_request(
        "POST",
        f"/pet",
        query_params=None,
        body={ "id": id, "category": category, "name": name, "photoUrls": photoUrls, "tags": tags, "status": status },
        content_type="application/json",
        extra_headers={}
    )

@mcp.tool(name="updatePet")
async def updatePet(id: Optional[int] = None, category: Optional[Dict[str, Any]] = None, name: Optional[str] = None, photoUrls: Optional[List[Any]] = None, tags: Optional[List[Any]] = None, status: Optional[str] = None):
    "Update an existing pet"
    return await make_request(
        "PUT",
        f"/pet",
        query_params=None,
        body={ "id": id, "category": category, "name": name, "photoUrls": photoUrls, "tags": tags, "status": status },
        content_type="application/json",
        extra_headers={}
    )

@mcp.tool(name="findPetsByStatus")
async def findPetsByStatus(status: str):
    "Multiple status values can be provided with comma separated strings"
    return await make_request(
        "GET",
        f"/pet/findByStatus",
        query_params={ "status": status },
        body=None,
        content_type="application/json",
        extra_headers={}
    )

@mcp.tool(name="findPetsByTags")
async def findPetsByTags(tags: str):
    "Multiple tags can be provided with comma separated strings. Use tag1, tag2, tag3 for testing."
    return await make_request(
        "GET",
        f"/pet/findByTags",
        query_params={ "tags": tags },
        body=None,
        content_type="application/json",
        extra_headers={}
    )

@mcp.tool(name="getPetById")
async def getPetById(petId: int):
    "Returns a single pet"
    return await make_request(
        "GET",
        f"/pet/{petId}",
        query_params=None,
        body=None,
        content_type="application/json",
        extra_headers={}
    )

@mcp.tool(name="updatePetWithForm")
async def updatePetWithForm(petId: int, name: Optional[str] = None, status: Optional[str] = None):
    "Updates a pet in the store with form data"
    return await make_request(
        "POST",
        f"/pet/{petId}",
        query_params=None,
        body={ "name": name, "status": status },
        content_type="multipart/form-data",
        extra_headers={}
    )

@mcp.tool(name="deletePet")
async def deletePet(petId: int):
    "Deletes a pet"
    return await make_request(
        "DELETE",
        f"/pet/{petId}",
        query_params=None,
        body=None,
        content_type="application/json",
        extra_headers={}
    )

@mcp.tool(name="getInventory")
async def getInventory():
    "Returns a map of status codes to quantities"
    return await make_request(
        "GET",
        f"/store/inventory",
        query_params=None,
        body=None,
        content_type="application/json",
        extra_headers={}
    )

@mcp.tool(name="placeOrder")
async def placeOrder(id: Optional[int] = None, petId: Optional[int] = None, quantity: Optional[int] = None, shipDate: Optional[str] = None, status: Optional[str] = None, complete: Optional[bool] = None):
    "Place an order for a pet"
    return await make_request(
        "POST",
        f"/store/order",
        query_params=None,
        body={ "id": id, "petId": petId, "quantity": quantity, "shipDate": shipDate, "status": status, "complete": complete },
        content_type="application/json",
        extra_headers={}
    )

@mcp.tool(name="getOrderById")
async def getOrderById(orderId: int):
    "For valid response try integer IDs with value >= 1 and <= 10. Other values will generated exceptions"
    return await make_request(
        "GET",
        f"/store/order/{orderId}",
        query_params=None,
        body=None,
        content_type="application/json",
        extra_headers={}
    )

@mcp.tool(name="deleteOrder")
async def deleteOrder(orderId: int):
    "For valid response try integer IDs with positive integer value. Negative or non-integer values will generate API errors"
    return await make_request(
        "DELETE",
        f"/store/order/{orderId}",
        query_params=None,
        body=None,
        content_type="application/json",
        extra_headers={}
    )

@mcp.tool(name="createUsersWithListInput")
async def createUsersWithListInput():
    "Creates list of users with given input array"
    return await make_request(
        "POST",
        f"/user/createWithList",
        query_params=None,
        body=None,
        content_type="application/json",
        extra_headers={}
    )

@mcp.tool(name="getUserByName")
async def getUserByName(username: str):
    "Get user by user name"
    return await make_request(
        "GET",
        f"/user/{username}",
        query_params=None,
        body=None,
        content_type="application/json",
        extra_headers={}
    )

@mcp.tool(name="updateUser")
async def updateUser(username: str, id: Optional[int] = None, username_body: Optional[str] = None, firstName: Optional[str] = None, lastName: Optional[str] = None, email: Optional[str] = None, password: Optional[str] = None, phone: Optional[str] = None, userStatus: Optional[int] = None):
    "This can only be done by the logged in user."
    return await make_request(
        "PUT",
        f"/user/{username}",
        query_params=None,
        body={ "id": id, "username": username_body, "firstName": firstName, "lastName": lastName, "email": email, "password": password, "phone": phone, "userStatus": userStatus },
        content_type="application/json",
        extra_headers={}
    )

@mcp.tool(name="deleteUser")
async def deleteUser(username: str):
    "This can only be done by the logged in user."
    return await make_request(
        "DELETE",
        f"/user/{username}",
        query_params=None,
        body=None,
        content_type="application/json",
        extra_headers={}
    )

@mcp.tool(name="loginUser")
async def loginUser(username: str, password: str):
    "Logs user into the system"
    return await make_request(
        "GET",
        f"/user/login",
        query_params={ "username": username, "password": password },
        body=None,
        content_type="application/json",
        extra_headers={}
    )

@mcp.tool(name="logoutUser")
async def logoutUser():
    "Logs out current logged in user session"
    return await make_request(
        "GET",
        f"/user/logout",
        query_params=None,
        body=None,
        content_type="application/json",
        extra_headers={}
    )

@mcp.tool(name="createUsersWithArrayInput")
async def createUsersWithArrayInput():
    "Creates list of users with given input array"
    return await make_request(
        "POST",
        f"/user/createWithArray",
        query_params=None,
        body=None,
        content_type="application/json",
        extra_headers={}
    )

@mcp.tool(name="createUser")
async def createUser(id: Optional[int] = None, username: Optional[str] = None, firstName: Optional[str] = None, lastName: Optional[str] = None, email: Optional[str] = None, password: Optional[str] = None, phone: Optional[str] = None, userStatus: Optional[int] = None):
    "This can only be done by the logged in user."
    return await make_request(
        "POST",
        f"/user",
        query_params=None,
        body={ "id": id, "username": username, "firstName": firstName, "lastName": lastName, "email": email, "password": password, "phone": phone, "userStatus": userStatus },
        content_type="application/json",
        extra_headers={}
    )

async def _root(request):
    try:
        server_name = getattr(mcp, "name", "mcp-server")
        tools_list = []
        try:
            tools_list = [t.name for t in getattr(mcp, "_tools", {}).values()]
        except:
            pass
        return JSONResponse({
            "status": "ready", 
            "server": server_name,
            "tools": tools_list,
            "transport": "sse"
        })
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

# Expose ASGI app for Vercel Python runtime
mcp_handler = None
if hasattr(mcp, "http_app"):
    try:
        mcp_handler = mcp.http_app(transport="sse")
    except:
        try:
            mcp_handler = mcp.http_app()
        except Exception as e:
            logger.error(f"Failed to create http_app: {e}")

if mcp_handler:
    app = Starlette(routes=[
        Route("/", _root),
        Mount("/", app=mcp_handler)
    ])
else:
    # Fallback for official mcp SDK or broken FastMCP
    try:
        from mcp.server.sse import SseServerTransport
        transport = SseServerTransport("/sse")
        
        async def handle_sse(request):
            async with transport.connect_scope(request.scope, request.receive, request.send):
                server = getattr(mcp, "server", mcp)
                await server.run(
                    transport,
                    transport.get_initialization_options(),
                    raise_exceptions=True
                )
        
        async def handle_messages(request):
            await transport.handle_post_bundle(request.scope, request.receive, request.send)

        app = Starlette(routes=[
            Route("/", _root),
            Route("/sse", handle_sse),
            Route("/messages/(.*)", handle_messages, methods=["POST"]),
            Route("/(.*)", _root),
        ])
    except Exception as e:
        logger.error(f"Fallback ASGI setup failed: {e}")
        app = Starlette(routes=[
            Route("/", _root),
            Route("/(.*)", _root)
        ])
