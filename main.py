import asyncio
import platform
from utils.logger_config import logger
from modules.networks import ARBITRUM_NETWORK
from modules.wallet import Wallet
from dotenv import load_dotenv
import os

if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

load_dotenv()


async def main():
    PRIVATE_KEY = os.getenv('PRIVATE_KEY')
    PROXY = os.getenv('PROXY')
    sender = Wallet(private_key=PRIVATE_KEY, network=ARBITRUM_NETWORK, proxy=PROXY)
    to_address = '0x4a6DfABd569eDf21AaEC508d7BEdc84fA8ef2A76'
    await sender.get_w3_client()
    try:
        tx_data = await sender.prepare_native_transfer_tx(recipient=to_address, amount=0.0005)
        await sender.sign_and_send_tx(tx_params=tx_data)
    except Exception as error:
        logger.error("Unexpected error occurred!")
        raise ValueError

asyncio.run(main())