import logging

from log4mongo.handlers import MongoHandler, MongoFormatter

import configs

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(
    MongoHandler(
        level=logging.INFO,
        host=configs.LOGGER_MONGO_HOST,
        port=configs.LOGGER_MONGO_PORT,
        username=configs.LOGGER_MONGO_USER,
        password=configs.LOGGER_MONGO_PASS,
        database_name=configs.LOGGER_MONGO_DB,
        collection=configs.LOGGER_MONGO_COLLECTION,
        formatter=MongoFormatter(),
    ),
)
