from hashlib import sha256
from datetime import datetime

def calculateHash(block):
    bloc = str(block.index) + str(block.previousHash) + str(block.timestamp) + str(block.produit) + str(block.origine) + str(block.traitements) + str(block.transport) + str(block.prix) + str(block.nonce)
    return(sha256(bloc.encode('utf-8')).hexdigest())


def repeat(string, length):
    return(string * (int(length/len(string))+1))[:length]

class Block(object):
    def __init__(self, index, previousHash, timestamp, produit, origine, traitements, transport, prix):
        self.index = index
        self.previousHash = previousHash
        self.timestamp = timestamp
        self.produit = produit
        self.origine = origine
        self.traitements = traitements
        self.transport = transport
        self.prix = prix
        self.nonce = 0
        self.hash = calculateHash(self)

    def mineBlock(self, difficulty):
        zeros = repeat("0", difficulty)
        self.nonce = 0
        while self.hash[0:difficulty] != zeros:
            self.nonce += 1
            self.hash = calculateHash(self)

class Blockchain(object):
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.blocks = []

        genesisBlock = Block(0, None, datetime.now(), "genesis block", "origine", "traitements", "transport", "prix")
        genesisBlock.mineBlock(self.difficulty)
        self.blocks.append(genesisBlock)

    def newBlock(self, produit, origine, traitements, transport, prix):
        latestBlock = self.blocks[-1]
        return(Block(latestBlock.index + 1, latestBlock.hash, datetime.now(), produit, origine, traitements, transport, prix))

    def addBlock(self, block):
        block.mineBlock(self.difficulty)
        self.blocks.append(block)

    def isFirstBlockValid(self):
        firstBlock = self.blocks[0]

        if firstBlock.index != 0:
            return False

        if firstBlock.previousHash is not None:
            return False

        if (firstBlock.hash is None or calculateHash(firstBlock) != firstBlock.hash):
            return False

        return True

    def isValidBlock(self, block, previousBlock):
        if previousBlock.index+1 != block.index:
            return False

        if (block.previousHash is None or block.previousHash != previousBlock.hash):
            return False

        if (block.hash is None or calculateHash(block) != block.hash):
            return False

        return True

