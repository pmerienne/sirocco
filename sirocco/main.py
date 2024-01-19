import uvicorn
from loguru import logger


if __name__ == '__main__':
    port = 5000
    logger.info(f'Starting API on port {port}')
    uvicorn.run('api:api', reload=True, port=port)

