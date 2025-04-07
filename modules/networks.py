from dataclasses import dataclass


@dataclass
class Network:
    chain_name: str
    rpc_url: str
    chain_id: int
    explorer_url: str
    eip1559_support: bool


ARBITRUM_NETWORK = Network(
    chain_name="Arbitrum One",
    chain_id=42161,
    rpc_url='https://arbitrum.llamarpc.com',
    explorer_url='https://arbiscan.io/',
    eip1559_support=True
)