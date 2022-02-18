from hashlib import sha256 #Depuis la librairie d'algorithmes hashlib, j'importe l'algorithme sha256 afin de pouvoir crypter les données de mes blocs
from datetime import datetime #J'importe la date et l'heure

##

#Cette fonction sert à calculer le hash de chacun de mes blocs en prenant en compte tous les éléments qui sont à l'intérieur de chacun d'entre eux
def calculateHash(block):
    bloc = str(block.index) + str(block.previousHash) + str(block.timestamp) + str(block.produit) + str(block.origine) + str(block.traitements) + str(block.transport) + str(block.prix) + str(block.nonce)
    return(sha256(bloc.encode('utf-8')).hexdigest())

#Cette fonction servira à répéter le nombre de 0 nécessaire à la difficulté du minage de mes blocs
def repeat(string, length):
    return (string * length)

##

#Ma classe Block qui prend en entrée l'index, le previousHash, le temps et toute la data
class Block:
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

    #Cette fonction sert à déterminer le nonce de chaque bloc, c-à-d le nombre de tentatives de calcul de l'ordinateur avant de trouver un hash correspondant à la difficulté que l'on a mis
    def mineBlock(self, difficulty):
        zeros = repeat("0", difficulty)
        self.nonce = 0
        while self.hash[0:difficulty] != zeros:
            self.nonce += 1
            self.hash = calculateHash(self)

##

#Ma classe Blockchain qui va me permettre de créer le bloc de génèse (le tout premier bloc de ma chaîne) afin de faire fonctionner correctement ma blockchain, de définir comment créer les nouveaux blocs de la chaîne, et enfin de vérifier si ma blockchain est valide
class Blockchain:
    #Ma blockchain est une liste de blocs, et mon constructeur prend comme unique argument la “difficulté”
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.blocks = []

        #Je défini mon bloc de génèse selon les caractéristiques suivantes : un index de "0", un préviousHash nul, la date et l'heure actuelle, et les données que j'ai arbitrairement laissé nuls
        genesisBlock = Block(0, None, datetime.now(), None, None, None, None, None)
        #A partir de ce bloc Genesis, je mine un bloc valide qui lui sera le premier de ma chaine
        genesisBlock.mineBlock(self.difficulty)
        #Puis j’ajoute le bloc résultant comme premier bloc de ma blockchain
        self.blocks.append(genesisBlock)

    #La fonction newBlock (qui prend en entrée toutes le données que je veux mettre) permet de définir automatiquement l'index, le previousHash et la date et l'heure de chaque nouveau bloc
    def newBlock(self, produit, origine, traitements, transport, prix):
        latestBlock = self.blocks[-1]
        return(Block(latestBlock.index + 1, latestBlock.hash, datetime.now(), produit, origine, traitements, transport, prix))

    #Il est nécessaire de miner ce bloc en fonction des données du bloc précédent afin de lui donner un hash valide et donc une intégrité vis-à-vis du reste de la blockchain, ce qui m’amène à la méthode addBlock. Je mine mon bloc et l’ajoute à la suite de la liste qui représente ma blockchain
    def addBlock(self, block):
        block.mineBlock(self.difficulty)
        self.blocks.append(block)

    #La fonction isFirstBlockValid permet de savoir si mon bloc de génèse est valide, c-à-d qu'il doit respecter certaines conditions avant de pouvoir l'être. Ces conditions sont : l'index du bloc doit être égal à 0, son previousHash doit être nul et son hash ne doit ni être nul ni différent du hash qui lui a été attribué.
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

    #La fonction isValidBlock permet de savoir si chaque bloc après le genesisBlock est valide. Comme avec le genesisBlock, les autres blocs doivent respecter certaines condition afin d'être valide. Ces conditions sont : l'index du bloc n doit être égal à l'index du bloc précédent+1, son previousHash doit être le Hash du bloc précédent et son hash ne doit ni être nul ni différent du hash qui lui a été attribué
    def isValidBlock(self, block, previousBlock):
        if previousBlock.index+1 != block.index:
            return False
        if (block.previousHash is None or block.previousHash != previousBlock.hash):
            return False
        if (block.hash is None or calculateHash(block) != block.hash):
            return False
        return True

        #La fonction isBlockchainValid permet de savoir si notre blockchain entière est valide. Pour cela, notre blockchain est valide si et seulement si : le premier bloc est valide et si tous ses blocs sont valides
    def isBlockchainValid(self):
        if not self.isFirstBlockValid():
            return False

        #Pour vérifier les blocs, il faut partir de l’index 1 et non 0, le premier bloc ne pouvant être validé par les mêmes conditions que les blocs suivants
        #Cette boucle valide donc le premier bloc, puis boucle sur l’ensemble de la liste des blocs formant la blockchain afin de les valider un par un
        for i in range(1, len(self.blocks)):
            previousBlock = self.blocks[i-1]
            block = self.blocks[i]
            if not self.isValidBlock(block, previousBlock):
                return False
        return True

    #Cette fonction permet d'afficher ma blockchain
    def afficher(self):
        for block in self.blocks:
            chain = "Block #"+str(block.index)+" ["+"\n\tindex: "+str(block.index)+"\n\tprevious hash: "+str(block.previousHash)+"\n\ttimestamp: "+str(block.timestamp)+"\n\tproduit: "+str(block.produit)+"\n\torigine: "+str(block.origine)+"\n\ttraitements: "+str(block.traitements)+"\n\ttransport: "+str(block.transport)+"\n\tprix: "+str(block.prix)+"\n\thash: "+str(block.hash)+"\n\tnonce: "+str(block.nonce)+"\n]\n"
            print(str(chain))

##

#Je défini la difficulté du minage (ici 3)
bchain = Blockchain(3)

#Je crée plusieurs blocs pour tester ma blockchain, pour cela je défini leurs données (produit, origine, traitements, transport et prix)
blockn1 = bchain.newBlock("Produit0", "Origine0", "Traitements0", "Transport0", "Prix0")
#Ensuite je mine ce bloc pour qu'il soit correctement inclu dans ma blockchain (en utilisant la fonction addBlock)
bchain.addBlock(blockn1)

#Je fais de même pour les autres blocs
blockn2 = bchain.newBlock("Produit1", "Origine1", "Traitements1", "Transport1", "Prix1")
bchain.addBlock(blockn2)
blockn3 = bchain.newBlock("Produit2", "Origine2", "Traitements2", "Transport2", "Prix2")
bchain.addBlock(blockn3)
blockn4 = bchain.newBlock("Produit3", "Origine3", "Traitements3", "Transport3", "Prix3")
bchain.addBlock(blockn4)

#J'affiche la validité de ma blockchain pour savoir s'il y a une erreur quelque part
print("Blockchain validity:", bchain.isBlockchainValid())

#J'affiche ma blockchain
bchain.afficher()
