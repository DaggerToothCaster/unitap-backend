bright_id_user_registry_abi = [
    {
        "inputs": [
            {"internalType": "bytes32", "name": "_context", "type": "bytes32"},
            {"internalType": "address", "name": "_verifier", "type": "address"},
            {"internalType": "address", "name": "_sponsor", "type": "address"},
        ],
        "stateMutability": "nonpayable",
        "type": "constructor",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "previousOwner",
                "type": "address",
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "newOwner",
                "type": "address",
            },
        ],
        "name": "OwnershipTransferred",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "addr",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "timestamp",
                "type": "uint256",
            },
        ],
        "name": "Registered",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "bytes32",
                "name": "context",
                "type": "bytes32",
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "verifier",
                "type": "address",
            },
        ],
        "name": "SetBrightIdSettings",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "sponsor",
                "type": "address",
            }
        ],
        "name": "SponsorChanged",
        "type": "event",
    },
    {
        "inputs": [],
        "name": "brightIdSponsor",
        "outputs": [
            {"internalType": "contract BrightIdSponsor", "name": "", "type": "address"}
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "context",
        "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "address", "name": "_user", "type": "address"}],
        "name": "isVerifiedUser",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "owner",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "bytes32", "name": "_context", "type": "bytes32"},
            {"internalType": "address", "name": "_addr", "type": "address"},
            {"internalType": "bytes32", "name": "_verificationHash", "type": "bytes32"},
            {"internalType": "uint256", "name": "_timestamp", "type": "uint256"},
            {"internalType": "uint8", "name": "_v", "type": "uint8"},
            {"internalType": "bytes32", "name": "_r", "type": "bytes32"},
            {"internalType": "bytes32", "name": "_s", "type": "bytes32"},
        ],
        "name": "register",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "renounceOwnership",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "bytes32", "name": "_context", "type": "bytes32"},
            {"internalType": "address", "name": "_verifier", "type": "address"},
        ],
        "name": "setSettings",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "address", "name": "_sponsor", "type": "address"}],
        "name": "setSponsor",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "address", "name": "addr", "type": "address"}],
        "name": "sponsor",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "address", "name": "newOwner", "type": "address"}],
        "name": "transferOwnership",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "address", "name": "", "type": "address"}],
        "name": "verifications",
        "outputs": [{"internalType": "uint256", "name": "time", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "verifier",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    },
]
