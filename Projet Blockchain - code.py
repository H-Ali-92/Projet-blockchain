from hashlib import sha256 #J'importe hashlib avec l'algorithme sha256 afin de pouvoir crypter les données de mes blocs
from datetime import datetime #J'importe la date et l'heure

#Cette fonction sert à calculer le hash de chacun de mes blocs et de le renvoyeren 64 termes hexadécimaux
def calculateHash(block):
    bloc = str(block.index) + str(block.previousHash) + str(block.timestamp) + str(block.produit) + str(block.origine) + str(block.traitements) + str(block.transport) + str(block.prix) + str(block.nonce)
    return(sha256(bloc.encode('utf-8')).hexdigest())

#Cette fonction servira à répéter le nombre de 0 nécessaire à la difficulté du minage de mes blocs
def repeat(string, length):
    return(string * (int(length/len(string))+1))[:length]

#Ma classe Block qui prend en compte l'index, le previousHash, le temps et toute la data
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

    #cette fonction sert à déterminer le nonce de chaque bloc, c-à-d le nombre de tentatives de calcul de l'ordinateur avant de trouver un hash correspondant à la difficulté que l'on a mis
    def mineBlock(self, difficulty):
        zeros = repeat("0", difficulty)
        self.nonce = 0
        while self.hash[0:difficulty] != zeros:
            self.nonce += 1
            self.hash = calculateHash(self)

#Ma classe Blockchain qui va me permettre d'inplémenter la difficulté, de créer le bloc de génèse (le tout premier bloc de ma chaîne) afin de faire fonctionner correctement ma blockchain, de définir comment créer les nouveaux blocs de la chaîne, et enfin de vérifier si ma blockchain est valide
class Blockchain(object):
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.blocks = []

        #Je défini mon bloc de génèse selon les caractéristiques suivantes : un index de "0", un préviousHash inexistant, la date et l'heure actuelle, et les données que j'ai arbitrairement laissé comme tel
        genesisBlock = Block(0, None, datetime.now(), "genesis block", "origine", "traitements", "transport", "prix")
        genesisBlock.mineBlock(self.difficulty)
        self.blocks.append(genesisBlock)

    #La fonction newBlock (qui prend en entrée toutes le données que je veux mettre) permet de définir automatiquement l'index, le previousHash et la date et l'heure de chaque nouveau bloc
    def newBlock(self, produit, origine, traitements, transport, prix):
        latestBlock = self.blocks[-1]
        return(Block(latestBlock.index + 1, latestBlock.hash, datetime.now(), produit, origine, traitements, transport, prix))


    def addBlock(self, block):
        block.mineBlock(self.difficulty)
        self.blocks.append(block)

    #La fonction isFirstBlockValid permet de savoir si mon bloc de génèse est valide, c-à-d qu'il doit respecter certaines conditions avant de pouvoir l'être. Ces conditions sont : l'index du bloc doit être égal à 0, son previousHash ne doit pas être inexistant et son hash ne doit ni être inexistant ni différent du hash qui lui a été attribué.
    #Si toutes ces conditions sont vérifiées, le premier bloc est donc valide
    def isFirstBlockValid(self):
        firstBlock = self.blocks[0]

        if firstBlock.index != 0:
            return False

        if firstBlock.previousHash is not None:
            return False

        if (firstBlock.hash is None or calculateHash(firstBlock) != firstBlock.hash):
            return False

        return True

    #La fonction isValidBlock permet de savoir si chaque bloc après le genesisBlock est valide. Comme avec le genesisBlock, les autres blocs doivent respecter certaines condition afin de d'être valide. Ces conditions sont : l'index du bloc n doit être égal à l'index du bloc précédent+1, son previousHash doit être le Hash du bloc précédent et son hash ne doit ni être inexistant ni différent du hash qui lui a été attribué
    def isValidBlock(self, block, previousBlock):
        if previousBlock.index+1 != block.index:
            return False

        if (block.previousHash is None or block.previousHash != previousBlock.hash):
            return False

        if (block.hash is None or calculateHash(block) != block.hash):
            return False

        return True

#Work in progress...
