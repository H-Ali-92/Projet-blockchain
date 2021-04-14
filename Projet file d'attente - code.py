from hashlib import sha256
from datetime import datetime
import random

valeur_offres = [random.randint(1,10) for i in range(random.randint(1,15))]
print(valeur_offres)

#Tri qui permet de classer les valeurs des offres dans l'ordre décroissant (afin de ne pas laisser dépasser une personne qui a une offre plus élevée que la sienne)
N=len(valeur_offres)
for i in range(N):
    minimum = valeur_offres[i]
    i_min = i
    for j in range(i,N):
        while valeur_offres[j] > minimum:
            minimum = valeur_offres[j]
            i_min = j
    tmp = valeur_offres[i]
    valeur_offres[i] = minimum
    valeur_offres[i_min] = tmp
print("\nListe triée :")
print(valeur_offres)
print("\n")

#--------------------------------------------------------------------------------#

def calculateHash(block):
    bloc = str(block.index) + str(block.previousHash) + str(block.timestamp) + str(block.payeur) + str(block.receveur) + str(block.offre_du_payeur) + str(block.offre_du_receveur) + str(block.différence_de_place_dans_la_file) + str(block.valeur_transaction) + str(block.nonce)
    return(sha256(bloc.encode('utf-8')).hexdigest())

def repeat(string, length):
    return(string * (int(length/len(string))+1))[:length]


class Block(object):
    def __init__(self, index, previousHash, timestamp, payeur, receveur, offre_du_payeur, offre_du_receveur, différence_de_place_dans_la_file, valeur_transaction):
        self.index = index
        self.previousHash = previousHash
        self.timestamp = timestamp
        self.payeur = payeur
        self.receveur = receveur
        self.offre_du_payeur = offre_du_payeur
        self.offre_du_receveur = offre_du_receveur
        self.différence_de_place_dans_la_file = différence_de_place_dans_la_file
        self.valeur_transaction = valeur_transaction
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

        genesisBlock = Block(0, None, datetime.now(), "genesis block", "receveur", "offre_du_payeur", "offre_du_receveur", "différence_de_place_dans_la_file", "valeur_transaction")
        genesisBlock.mineBlock(self.difficulty)
        self.blocks.append(genesisBlock)

    def newBlock(self, payeur, receveur, offre_du_payeur, offre_du_receveur, différence_de_place_dans_la_file, valeur_transaction):
        latestBlock = self.blocks[-1]
        return(Block(latestBlock.index + 1, latestBlock.hash, datetime.now(), payeur, receveur, offre_du_payeur, offre_du_receveur, différence_de_place_dans_la_file, valeur_transaction))

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

    def isBlockchainValid(self):
        if not self.isFirstBlockValid():
            return False
        for i in range(1, len(self.blocks)):
            previousBlock = self.blocks[i-1]
            block = self.blocks[i]
            if not self.isValidBlock(block, previousBlock):
                return False

        return True

    def display(self):
        for block in self.blocks:
            chain = "Block #"+str(block.index)+" ["+"\n\tindex: "+str(block.index)+"\n\tprevious hash: "+str(block.previousHash)+"\n\ttimestamp: "+str(block.timestamp)+"\n\tpayeur: "+str(block.payeur)+"\n\treceveur: "+str(block.receveur)+"\n\toffre_du_payeur: "+str(block.offre_du_payeur)+"\n\toffre_du_receveur: "+str(block.offre_du_receveur)+"\n\tdifférence_de_place_dans_la_file: "+str(block.différence_de_place_dans_la_file)+"\n\tvaleur_transaction: "+str(block.valeur_transaction)+"\n\thash: "+str(block.hash)+"\n\tnonce: "+str(block.nonce)+"\n]\n"
            print(str(chain))


bchain = Blockchain(3)

blockn1 = bchain.newBlock("A", "B", "8", "6", "1", "6 euros")
bchain.addBlock(blockn1)

blockn2 = bchain.newBlock("C", "D", "11", "8", "2", "16 euros")
bchain.addBlock(blockn2)

print("Blockchain validity:", bchain.isBlockchainValid())

bchain.display()
