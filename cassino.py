from random import random
import matplotlib.pyplot as plt

NUMERO_JOGOS = 10_000
NUMERO_JOGADORES = 100
PORCENTAGEM_JOGADOR_GANHAR = 0.5

SALDO_INICIAL = 1000
CUSTO_RODADA = 10
GANHO_RODADA = 2


class Jogador:
    def __init__(
            self, 
            saldo_inicial: int   = SALDO_INICIAL, 
            custo_rodada:  int   = CUSTO_RODADA, 
            ganho_rodada:  float = GANHO_RODADA
            ):

        self.saldo = saldo_inicial
        self.custo = custo_rodada
        self.ganho = custo_rodada * ganho_rodada
        self.falido = False
        self.historico = [saldo_inicial]

    def jogar(self) -> None:
        if not self.falido:
            self.saldo -= self.custo
            if random() < PORCENTAGEM_JOGADOR_GANHAR:
                self.saldo += self.ganho

            if self.saldo <= 0:
                self.saldo = 0
                self.falido = True

        self.historico.append(self.saldo)


class Simulador:
    def __init__(
            self, 
            jogadores: list[Jogador],
            num_jogos: int = NUMERO_JOGOS
            ):
        self.jogadores = jogadores
        self.num_jogos = num_jogos

    def run(self):
        for _ in range(self.num_jogos):
            for jogador in self.jogadores:
                jogador.jogar()

    def plotar(self):
        plt.figure(figsize=(12, 6))

        for jogador in self.jogadores:
            plt.plot(jogador.historico, linewidth=0.7, alpha=0.6)

        plt.axhline(y=SALDO_INICIAL, color='black', linestyle='--', linewidth=1)

        n_falidos = sum(1 for j in self.jogadores if j.falido)
        n_prejuizo = sum(1 for j in self.jogadores if not j.falido and j.saldo < SALDO_INICIAL)
        n_lucro = sum(1 for j in self.jogadores if not j.falido and j.saldo > SALDO_INICIAL)

        texto = (
            f'% para vitória: {PORCENTAGEM_JOGADOR_GANHAR * 100:.2f}%\n'
            f'Odd: {GANHO_RODADA:.2f}\n'
            f'Falidos: {n_falidos}\n'
            f'Com prejuízo: {n_prejuizo}\n'
            f'Com lucro: {n_lucro}'
        )
        plt.gca().text(
            0.02, 0.02, texto,
            transform=plt.gca().transAxes,
            fontsize=10,
            verticalalignment='bottom',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8)
        )

        plt.title('Evolução do saldo dos jogadores')
        plt.xlabel('Número de jogos')
        plt.ylabel('Saldo')
        plt.tight_layout()
        plt.show()


if __name__ == '__main__':
    jogadores = [Jogador() for _ in range(NUMERO_JOGADORES)]
    simulador = Simulador(jogadores)

    simulador.run()
    simulador.plotar()