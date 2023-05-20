from app.LandAPI import get_app
from app.LandAPI.context import AppContext


async def get_context():
    app = get_app()
    if type(app) is None:
        raise NotImplementedError("app not configured")

    ctx = AppContext(app)
    try:
        yield ctx
    finally:
        await ctx.close()
