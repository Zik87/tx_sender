from web3 import AsyncWeb3, AsyncHTTPProvider
from aiohttp import ClientSession
from networks import Network
from utils.logger_config import logger
from web3.types import TxParams


class Wallet:
    def __init__(self, private_key: str, network: Network, proxy: None | str=None):
        self.private_key = private_key
        self.network = network
        self.proxy = proxy
        self.session = ClientSession()
        self.w3_client = None
        self.address = None



    async def __aenter__(self):
        return


    def __aexit__(self, exc_type, exc_val, exc_tb):
        return self.session.close()


    async def get_w3_client(self):
        self.private_key = await self.validate_private_key(self.private_key)
        request_kwargs = {}
        if self.proxy:
            request_kwargs = {
                'proxy': f'http://{self.proxy}'
            }
        try:
            logger.debug(f"Trying to connect to RPC - {self.network.rpc_url}")
            self.w3_client = AsyncWeb3(AsyncHTTPProvider(endpoint_uri=self.network.rpc_url, request_kwargs=request_kwargs))
            if await self.w3_client.is_connected():
                logger.info("Connected successfully!")
                self.address = self.w3_client.to_checksum_address(self.w3_client.eth.account.from_key(self.private_key))
            else:
                logger.error(f"Couldn't connect to RPC! RPC URL {self.network.rpc_url}")
                raise KeyError(f"Couldn't connect to RPC! RPC URL {self.network.rpc_url}")
        except Exception as error:
            print(f"Error: {error}")


    async def validate_private_key(self, private_key: str) -> str:
        if len(private_key) != 64 or not private_key.lower().startswith("0x"):
            logger.error("Invalid private key. Please provide a valid private key and restart the soft.")
            raise KeyError()
        return private_key.lower()


    async def prepare_native_transfer_tx(self, recipient: str, amount: float) -> TxParams:
        if not self.w3_client:
            logger.error("Web3 client wasn't connected!")
            raise KeyError

        tx_params = TxParams(
            to=self.w3_client.to_checksum_address(recipient),
            value=self.w3_client.to_wei(amount, 'ether'),
            nonce=await self.w3_client.eth.get_transaction_count(self.address),
            chain_id=self.network.chain_id
        )

        if not self.network.eip1559_support:
            tx_params['gasPrice'] = self.w3_client.to_wei(int(await self.w3_client.eth.gas_price * 1.15), 'wei')
        else:
            base_fee = await self.w3_client.eth.gas_price
            max_priority_fee_per_gas = await self.w3_client.eth.max_priority_fee

            max_fee_per_gas = self.w3_client.to_wei(int(base_fee * 1.15 + max_priority_fee_per_gas), 'wei')

            tx_params['maxFeePerGas'] = max_fee_per_gas
            tx_params['maxPriorityFeePerGas'] = max_priority_fee_per_gas
            tx_params['type'] = 2

        logger.debug(f"Tx Params: {tx_params}")
        logger.info("Transaction was prepared successfully!")
        return tx_params


    async def sign_and_send_tx(self, tx_params: TxParams) -> None:
        try:
            tx_params['gas'] = int((await self.w3_client.eth.estimate_gas(tx_params)) * 1.15)
            logger.info(f"Transaction was simulated without errors. Predicted gas: {tx_params['gas']}")
        except Exception as error:
            logger.error(f" Unexpected error occurred while was simulating the tx {error}")
            raise KeyError()

        try:
            signed_tx = await self.w3_client.eth.account.sign_transaction(tx=tx_params, private_key=self.private_key)
            tx_hash = await self.w3_client.eth.send_raw_transaction(signed_tx.rawTransaction)
            logger.info(f"Transaction was send successfully!. Waiting the confirmation.")
            tx_receipt = self.w3_client.eth.wait_for_transaction_receipt(tx_hash, timeout=300, pool_latency=2)
            logger.info(f"Transaction was mined! Check: {self.network.explorer_url}/tx/{tx_hash.hex()}")
        except Exception as error:
            logger.error(f"Unexpected error occurred while was signing/sending the tx {error}")















