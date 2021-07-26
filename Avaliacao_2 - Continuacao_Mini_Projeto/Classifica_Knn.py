class Knn():
    '''
    Classe que identifica perfil de investimento para novos clientes com base em critérios existentes.
    ----------
    Atributos:
    k --> quantidade de pontos mais próximos a serem comparados
    bd_cliente --> base de dados existente dos clientes com perfil já identificado 
    bd_novo_cliente --> base de dados dos novos clientes a serem identificados
    dicionario --> dicionário para armazenar CPF clientes não classificados, e distancia e cpf clientes classificados
    '''

    # método construtor da classe

    def __init__(self, k, bd_cliente, bd_novo_cliente, dicionario, perfil_classificado):
        self.k = k
        self.bd_cliente = bd_cliente
        self.bd_novo_cliente = bd_novo_cliente
        self.dicionario = dicionario
        self.perfil_classificado = perfil_classificado

    # demais métodos da classe
    def calc_dist(self, novo_cliente, cliente):
        '''
        Cálculo da distância euclidiana entre os pontos de interesse para classificação
        ----------
        Argumentos:
        novo_cliente (list) --> valores da carteira de investimentos do novo cliente
        cliente (list) --> valores da carteira de investimentos do cliente existente
        ----------
        Retorno:
        d (float) --> valor correspondente a distância dos pontos de interesse entre
        o cliente novo e o cliente existente
        '''
        d = (sum([(x - y)**2 for x, y in zip(novo_cliente, cliente)]))**0.5

        return d

    def associa(self, cliente_novo):
        '''
        Cria um dicionário para associar CPF de novos clientes com distância e CPF de 
        clientes existentes
        ----------
        Argumentos:
        cliente_novo (list) --> lista contendo informações do novo cliente
        ----------
        Retorno:
        dicionario (dict) --> dicionário no seguinte padrão 
        {cpf_cliente_novo : {distancia_entre_clientes : cpf_cliente_existente}}
        '''
        self.dicionario[cliente_novo[0]] = {}

        for cliente_class in self.bd_cliente:
            self.dicionario[cliente_novo[0]][self.calc_dist(cliente_novo[2], cliente_class[2])] = cliente_class[0]

        return self.dicionario

    def menor_dist(self, cliente_novo):
        '''
        Verifica quais as k menores distâncias entre os clientes
        ----------
        Argumentos:
        cliente_novo (list) --> lista contendo informações do novo cliente
        ----------
        Retorno:
        d_menor (list) --> lista contendo as k menores distâncias
        '''
        dist = list(self.dicionario[cliente_novo[0]].keys())
        dist.sort()
        d_menor = dist[:self.k]
        
        return d_menor

    def cpf_perfil(self):
        '''
        Cria um dicionário para associar CPF e perfil dos clientes existentes
        ----------
        Argumentos: 
        nenhum (usada apenas internamente na classe)
        ----------
        Retorno:
        dic_aux (dict) --> dicinário no seguinte padrão: 
        {cpf_cliente_existente : perfil_cliente_existente}
        '''
        dic_aux = {}
        
        for cliente in self.bd_cliente:
            dic_aux[cliente[0]] = cliente[1]

        return dic_aux

    def perfil_cliente(self, menor_dist, cliente_novo):
        '''
        Obtém os perfis dos vizinhos mais próximos
        ----------
        Argumentos:
        menor_dist (list) --> lista contendo as k menores distâncias
        cliente_novo (list) --> lista contendo informações do novo cliente
        ----------
        Retorno:
        vizinho (list) --> lista contendo os perfis dos k vizinhos mais próximos
        '''
        vizinho = []
        dic_cpf_perfil = self.cpf_perfil()
        
        for dist in menor_dist:
            vizinho.append(dic_cpf_perfil.get(self.dicionario[cliente_novo[0]].get(dist)))

        return vizinho
    
    def moda (self, vizinho, cliente_novo):
        '''
        Obtém o perfil de maior frequência dentre os k vizinhos mais próximos
        ----------
        Argumentos:
        vizinho (list) --> lista contendo os perfis dos k vizinhos mais próximos
        cliente_novo (list) --> lista contendo informações do novo cliente
        ----------
        Retorno:
        perfil_classificado (dict) --> dicionário contendo a classificação do
        cliente novo
        '''
        count = 0
        for perfil in vizinho:       
            if count < vizinho.count(perfil):            
                count = vizinho.count(perfil)
                self.perfil_classificado[cliente_novo[0]] = perfil   
        return self.perfil_classificado
    
    def imprime_clientes(self):
        '''
        Imprime o dicionário de novos clientes classificados de uma maneira melhor
        para vizualização
        ----------
        Argumentos:
        nenhum (usada apenas internamente na classe)
        ----------
        Retorno:
        impressão do dicionário de novos clientes classificados
        '''
        print('Perfis estimados para a base de dados no_class:\n')
                
        for cliente, perfil in self.perfil_classificado.items():
            print(f'{cliente} : {perfil}')