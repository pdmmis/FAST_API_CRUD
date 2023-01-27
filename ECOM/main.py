from fastapi import FastAPI
from admin.apis import routes as AdminRoute
from tortoise.contrib.fastapi import register_tortoise
from configs.connection import DATABASE_URL

db_url=DATABASE_URL()
app=FastAPI()
app.include_router(AdminRoute.router,tags=["Admin"])

register_tortoise(
    app,
    db_url=db_url,
    modules={'models':['admin.apis.models']},
    generate_schemas  = True,
    add_exception_handlers =True
)
