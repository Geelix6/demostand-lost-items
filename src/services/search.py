from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.item import Item

async def semantic_search(
    session: AsyncSession,
    query_embedding: list[float],
    limit: int = 5
) -> list[Item]:
    stmt = (
        select(Item)
        .order_by(Item.embedding.cosine_distance(query_embedding))
        .limit(limit)
    )
    result = await session.execute(stmt)
    return result.scalars().all()
