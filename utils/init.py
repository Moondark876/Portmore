import motor.motor_asyncio
import os
import dotenv

dotenv.load_dotenv()

cluster = motor.motor_asyncio.AsyncIOMotorClient(os.environ['MONGOKEY'])
